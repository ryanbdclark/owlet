"""Support for Owlet switches."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import OwletCoordinator
from .entity import OwletBaseEntity

SCAN_INTERVAL = timedelta(seconds=5)
PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Owlet switch based on a config entry."""
    coordinators: OwletCoordinator = hass.data[DOMAIN][config_entry.entry_id].values()

    switches = []
    for coordinator in coordinators:
        switches.append(OwletBaseSwitch(coordinator))
    async_add_entities(switches)


class OwletBaseSwitch(OwletBaseEntity, SwitchEntity):
    """Defines a Owlet switch."""

    _attr_has_entity_name = True
    _attr_translation_key = "base_on"

    def __init__(self, coordinator: OwletCoordinator) -> None:
        """Initialize ecobee ventilator platform."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{self.sock.serial}-base_station_on"
        self._attr_is_on = False

    @property
    def is_on(self):
        return self.sock.properties["base_station_on"]

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch."""
        await self.sock.control_base_station(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        await self.sock.control_base_station(False)
