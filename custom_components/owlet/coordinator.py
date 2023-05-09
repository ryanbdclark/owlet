"""Owlet integration."""
from __future__ import annotations

from datetime import timedelta
import logging

from pyowletapi.sock import Sock
from pyowletapi.exceptions import OwletError

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    MANUFACTURER,
)

_LOGGER = logging.getLogger(__name__)


class OwletCoordinator(DataUpdateCoordinator):
    """Coordinator is responsible for querying the device at a specified route."""

    def __init__(self, hass: HomeAssistant, sock: Sock, interval: int) -> None:
        """Initialise a custom coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=interval),
        )
        assert self.config_entry is not None
        self._device_unique_id = sock.serial
        self._model = sock.model
        self._sw_version = sock.sw_version
        self._hw_version = sock.version
        self.sock = sock
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_unique_id)},
            name="Owlet Baby Care Sock",
            manufacturer=MANUFACTURER,
            model=self._model,
            sw_version=self._sw_version,
            hw_version=self._hw_version,
        )

    async def _async_update_data(self) -> None:
        """Fetch the data from the device."""
        try:
            await self.sock.update_properties()
        except OwletError as err:
            raise UpdateFailed(err) from err
