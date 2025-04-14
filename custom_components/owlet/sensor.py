"""Support for Owlet sensors."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN, SLEEP_STATES
from .coordinator import OwletCoordinator
from .entity import OwletBaseEntity


@dataclass(kw_only=True)
class OwletSensorEntityDescription(SensorEntityDescription):
    """Represent the owlet sensor entity description."""

    available_during_charging: bool


SENSORS: tuple[OwletSensorEntityDescription, ...] = (
    OwletSensorEntityDescription(
        key="battery_percentage",
        translation_key="batterypercent",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        available_during_charging=True,
    ),
    OwletSensorEntityDescription(
        key="oxygen_saturation",
        translation_key="o2saturation",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:leaf",
        available_during_charging=False,
    ),
    OwletSensorEntityDescription(
        key="heart_rate",
        translation_key="heartrate",
        native_unit_of_measurement="bpm",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:heart-pulse",
        available_during_charging=False,
    ),
    OwletSensorEntityDescription(
        key="battery_minutes",
        translation_key="batterymin",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        available_during_charging=False,
    ),
    OwletSensorEntityDescription(
        key="signal_strength",
        translation_key="signalstrength",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        available_during_charging=True,
    ),
    OwletSensorEntityDescription(
        key="skin_temperature",
        translation_key="skintemp",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        available_during_charging=False,
    ),
    OwletSensorEntityDescription(
        key="movement",
        translation_key="movement",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:cursor-move",
        entity_registry_enabled_default=False,
        available_during_charging=False,
    ),
    OwletSensorEntityDescription(
        key="movement_bucket",
        translation_key="movementbucket",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:bucket-outline",
        entity_registry_enabled_default=False,
        available_during_charging=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the owlet sensors from config entry."""

    coordinators: list[OwletCoordinator] = list(
        hass.data[DOMAIN][config_entry.entry_id].values()
    )

    sensors = []

    for coordinator in coordinators:
        sensors.extend([
            OwletSensor(coordinator, sensor)
            for sensor in SENSORS
            if sensor.key in coordinator.sock.properties
        ])

        if OwletSleepSensor.entity_description.key in coordinator.sock.properties:
            sensors.append(OwletSleepSensor(coordinator))
        if (
            OwletOxygenAverageSensor.entity_description.key
            in coordinator.sock.properties
        ):
            sensors.append(OwletOxygenAverageSensor(coordinator))

    async_add_entities(sensors)


class OwletSensor(OwletBaseEntity, SensorEntity):
    """Representation of an Owlet sensor."""

    def __init__(
        self,
        coordinator: OwletCoordinator,
        description: OwletSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description: OwletSensorEntityDescription = description
        self._attr_unique_id = f"{self.sock.serial}-{description.key}"

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and (
            not self.sock.properties["charging"]
            or self.entity_description.available_during_charging
        )

    @property
    def native_value(self) -> StateType:
        """Return sensor value."""

        return self.sock.properties[self.entity_description.key]


class OwletSleepSensor(OwletSensor):
    """Representation of an Owlet sleep sensor."""

    _attr_options = list(SLEEP_STATES.values())
    entity_description = OwletSensorEntityDescription(
        key="sleep_state",
        translation_key="sleepstate",
        device_class=SensorDeviceClass.ENUM,
        available_during_charging=False,
    )

    def __init__(
        self,
        coordinator: OwletCoordinator,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, self.entity_description)

    @property
    def native_value(self) -> StateType:
        """Return sensor value."""
        return SLEEP_STATES[self.sock.properties["sleep_state"]]


class OwletOxygenAverageSensor(OwletSensor):
    """Representation of an Owlet sleep sensor."""

    entity_description = OwletSensorEntityDescription(
        key="oxygen_10_av",
        translation_key="o2saturation10a",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:leaf",
        available_during_charging=False,
        state_class=SensorStateClass.MEASUREMENT,
    )

    def __init__(
        self,
        coordinator: OwletCoordinator,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, self.entity_description)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            super().available
            and (
                not self.sock.properties["charging"]
                or self.entity_description.available_during_charging
            )
            and (
                self.sock.properties["oxygen_10_av"] >= 0
                and self.sock.properties["oxygen_10_av"] <= 100
            )
        )
