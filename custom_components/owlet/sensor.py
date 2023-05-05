"""Support for Android IP Webcam binary sensors."""
from __future__ import annotations
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    UnitOfTime,
)

from .const import DOMAIN
from .coordinator import OwletCoordinator
from .entity import OwletBaseEntity


@dataclass
class OwletSensorEntityDescriptionMixin:
    """Owlet sensor description mix in"""

    element: str


@dataclass
class OwletSensorEntityDescription(
    SensorEntityDescription, OwletSensorEntityDescriptionMixin
):
    """Represent the owlet sensor entity description."""


SENSORS: tuple[OwletSensorEntityDescription, ...] = (
    OwletSensorEntityDescription(
        key="batterypercentage",
        name="Battery",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        element="battery_percentage",
    ),
    OwletSensorEntityDescription(
        key="oxygensaturation",
        name="O2 Saturation",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        element="oxygen_saturation",
        icon="mdi:leaf",
    ),
    OwletSensorEntityDescription(
        key="heartrate",
        name="Heart rate",
        native_unit_of_measurement="bpm",
        state_class=SensorStateClass.MEASUREMENT,
        element="heart_rate",
        icon="mdi:heart-pulse",
    ),
    OwletSensorEntityDescription(
        key="batteryminutes",
        name="Battery Remaining",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        element="battery_minutes",
    ),
    OwletSensorEntityDescription(
        key="signalstrength",
        name="Singal Strength",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        element="signal_strength",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the owlet sensors from config entry."""

    coordinator: OwletCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = [OwletSensor(coordinator, sensor) for sensor in SENSORS]

    async_add_entities(entities)


class OwletSensor(OwletBaseEntity, SensorEntity):
    """Representation of an Owlet sensor."""

    def __init__(
        self,
        coordinator: OwletCoordinator,
        sensor_description: OwletSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = sensor_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}-{self.entity_description.name}"
        )
        super().__init__(coordinator)

    @property
    def native_value(self):
        """Return sensor value"""

        if (
            self.entity_description.element
            in [
                "heart_rate",
                "battery_minutes",
                "oxygen_saturation",
            ]
            and self.sock.properties["charging"]
        ):
            return None

        return self.sock.properties[self.entity_description.element]
