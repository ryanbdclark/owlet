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


@dataclass
class OwletBinarySensorEntityMixin:
    """Owlet binary sensor element mixin"""

    element: str


@dataclass
class OwletBinarySensorEntityDescription(
    BinarySensorEntityDescription, OwletBinarySensorEntityMixin
):
    """Represent the owlet binary sensor entity description."""


SENSORS: tuple[OwletBinarySensorEntityDescription, ...] = (
    OwletBinarySensorEntityDescription(
        key="charging",
        translation_key="charging",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
        element="charging",
    ),
    OwletBinarySensorEntityDescription(
        key="highhr",
        translation_key="high_hr_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        element="high_heart_rate_alert",
    ),
    OwletBinarySensorEntityDescription(
        key="lowhr",
        translation_key="low_hr_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        element="low_heart_rate_alert",
    ),
    OwletBinarySensorEntityDescription(
        key="higho2",
        translation_key="high_ox_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        element="high_oxygen_alert",
    ),
    OwletBinarySensorEntityDescription(
        key="lowo2",
        translation_key="low_ox_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        element="low_oxygen_alert",
    ),
    OwletBinarySensorEntityDescription(
        key="lowbattery",
        translation_key="low_batt_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        element="low_battery_alert",
    ),
    OwletBinarySensorEntityDescription(
        key="lostpower",
        translation_key="lost_pwr_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        element="lost_power_alert",
    ),
    OwletBinarySensorEntityDescription(
        key="sockdisconnected",
        translation_key="sock_discon_alrt",
        device_class=BinarySensorDeviceClass.SOUND,
        element="sock_disconnected",
    ),
    OwletBinarySensorEntityDescription(
        key="sock_off",
        translation_key="sock_off",
        device_class=BinarySensorDeviceClass.POWER,
        element="sock_off",
    ),
    OwletBinarySensorEntityDescription(
        key="awake",
        translation_key="awake",
        element="sleep_state",
        icon="mdi:sleep",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the owlet sensors from config entry."""

    coordinators: OwletCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        OwletBinarySensor(coordinator, sensor)
        for coordinator in coordinators
        for sensor in SENSORS
    )


class OwletBinarySensor(OwletBaseEntity, BinarySensorEntity):
    """Representation of an Owlet binary sensor."""

    def __init__(
        self,
        coordinator: OwletCoordinator,
        sensor_description: OwletBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = sensor_description
        self._attr_unique_id = f"{self.sock.serial}-{self.entity_description.name}"

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        state = self.sock.properties[self.entity_description.element]

        if self.entity_description.element == "sleep_state":
            if self.sock.properties["charging"]:
                return None
            if state in [8, 15]:
                state = False
            else:
                state = True

        return state
