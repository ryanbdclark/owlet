"""Support for Owlet binary sensors."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import OwletCoordinator
from .entity import OwletBaseEntity


@dataclass(kw_only=True)
class OwletBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Represent the owlet binary sensor entity description."""

    available_during_charging: bool


SENSORS: tuple[OwletBinarySensorEntityDescription, ...] = (
    OwletBinarySensorEntityDescription(
        key="charging",
        translation_key="charging",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
        available_during_charging=True,
    ),
    OwletBinarySensorEntityDescription(
        key="high_heart_rate_alert",
        translation_key="high_hr_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        available_during_charging=True,
    ),
    OwletBinarySensorEntityDescription(
        key="low_heart_rate_alert",
        translation_key="low_hr_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        available_during_charging=True,
    ),
    OwletBinarySensorEntityDescription(
        key="high_oxygen_alert",
        translation_key="high_ox_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        available_during_charging=True,
    ),
    OwletBinarySensorEntityDescription(
        key="low_oxygen_alert",
        translation_key="low_ox_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        available_during_charging=True,
    ),
    OwletBinarySensorEntityDescription(
        key="critical_oxygen_alert",
        translation_key="crit_ox_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        available_during_charging=True,
    ),
    OwletBinarySensorEntityDescription(
        key="low_battery_alert",
        translation_key="low_batt_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        available_during_charging=True,
    ),
    OwletBinarySensorEntityDescription(
        key="critical_battery_alert",
        translation_key="crit_batt_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        available_during_charging=True,
    ),
    OwletBinarySensorEntityDescription(
        key="lost_power_alert",
        translation_key="lost_pwr_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        available_during_charging=True,
    ),
    OwletBinarySensorEntityDescription(
        key="sock_disconnected",
        translation_key="sock_discon_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        available_during_charging=True,
    ),
    OwletBinarySensorEntityDescription(
        key="sock_off",
        translation_key="sock_off",
        device_class=BinarySensorDeviceClass.POWER,
        available_during_charging=True,
    ),
    OwletBinarySensorEntityDescription(
        key="base_station_on",
        translation_key="base_on",
        device_class=BinarySensorDeviceClass.POWER,
        available_during_charging=True,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the owlet sensors from config entry."""

    coordinators: OwletCoordinator = hass.data[DOMAIN][config_entry.entry_id].values()

    sensors = []
    for coordinator in coordinators:
        for sensor in SENSORS:
            if sensor.key in coordinator.sock.properties:
                sensors.append(OwletBinarySensor(coordinator, sensor))

        if OwletAwakeSensor.entity_description.key in coordinator.sock.properties:
            sensors.append(OwletAwakeSensor(coordinator))

    async_add_entities(sensors)


class OwletBinarySensor(OwletBaseEntity, BinarySensorEntity):
    """Representation of an Owlet binary sensor."""

    def __init__(
        self,
        coordinator: OwletCoordinator,
        description: OwletBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{self.sock.serial}-{description.key}"

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and (
            not self.sock.properties["charging"]
            or self.entity_description.available_during_charging
        )

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        if self.entity_description.key == "sleep_state":
            if self.sock.properties["charging"]:
                return None
            if state in [8, 15]:
                state = False
            else:
                state = True

        return self.sock.properties[self.entity_description.key]


class OwletAwakeSensor(OwletBinarySensor):
    """Representation of an Owlet sleep sensor."""

    entity_description = OwletBinarySensorEntityDescription(
        key="sleep_state",
        translation_key="awake",
        icon="mdi:sleep",
        available_during_charging=False,
    )

    def __init__(
        self,
        coordinator: OwletCoordinator,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, self.entity_description)

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return False if self.sock.properties[self.entity_description.key] in [8, 15] else True
