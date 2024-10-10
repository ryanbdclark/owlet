"""Support for Owlet switches."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from pyowletapi.sock import Sock

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import OwletCoordinator
from .entity import OwletBaseEntity

SCAN_INTERVAL = timedelta(seconds=5)
PARALLEL_UPDATES = 0


@dataclass(frozen=True, kw_only=True)
class OwletSwitchEntityDescription(SwitchEntityDescription):
    """Describes Owlet switch entity."""

    turn_on_fn: Callable[[Sock], Callable[[bool], Coroutine[Any, Any, None]]]
    turn_off_fn: Callable[[Sock], Callable[[bool], Coroutine[Any, Any, None]]]
    available_during_charging: bool


SWITCHES: tuple[OwletSwitchEntityDescription, ...] = (
    OwletSwitchEntityDescription(
        key="base_station_on",
        translation_key="base_on",
        turn_on_fn=lambda sock: (lambda state: sock.control_base_station(state)),
        turn_off_fn=lambda sock: (lambda state: sock.control_base_station(state)),
        available_during_charging=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Owlet switch based on a config entry."""
    coordinators: OwletCoordinator = hass.data[DOMAIN][config_entry.entry_id].values()

    switches = []
    for coordinator in coordinators:
        switches = [OwletBaseSwitch(coordinator, switch) for switch in SWITCHES]
    async_add_entities(switches)


class OwletBaseSwitch(OwletBaseEntity, SwitchEntity):
    """Defines a Owlet switch."""

    entity_description: OwletSwitchEntityDescription

    def __init__(
        self,
        coordinator: OwletCoordinator,
        description: OwletSwitchEntityDescription,
    ) -> None:
        """Initialize owlet switch platform."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{self.sock.serial}-{description.key}"
        self._attr_is_on = False

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and (
            not self.sock.properties["charging"]
            or self.entity_description.available_during_charging
        )

    @property
    def is_on(self) -> bool:
        """Return if switch is on or off."""
        return self.sock.properties[self.entity_description.key]

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch."""
        await self.entity_description.turn_on_fn(self.sock)(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        await self.entity_description.turn_off_fn(self.sock)(False)
