"""The Owlet Smart Sock integration."""
from __future__ import annotations

import logging

from pyowletapi.api import OwletAPI
from pyowletapi.sock import Sock
from pyowletapi.exceptions import OwletConnectionError

from homeassistant.config_entries import ConfigEntry, ConfigEntryAuthFailed
from homeassistant.const import (
    Platform,
    CONF_REGION,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_API_TOKEN,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import (
    DOMAIN,
    CONF_OWLET_EXPIRY,
    SUPPORTED_VERSIONS,
)
from .coordinator import OwletCoordinator

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Owlet Smart Sock from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    owlet_api = OwletAPI(
        entry.data[CONF_REGION],
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
        entry.data[CONF_API_TOKEN],
        entry.data[CONF_OWLET_EXPIRY],
        async_get_clientsession(hass),
    )

    try:
        token = await owlet_api.authenticate()

        if token:
            hass.config_entries.async_update_entry(entry, data={**entry.data, **token})

        socks = {
            device["device"]["dsn"]: Sock(owlet_api, device["device"])
            for device in await owlet_api.get_devices(SUPPORTED_VERSIONS)
        }

    except OwletConnectionError as err:
        _LOGGER.error("Credentials no longer valid, please setup owlet again")
        raise ConfigEntryAuthFailed(
            f"Credentials expired for {entry.data[CONF_USERNAME]}"
        ) from err

    coordinators = [
        OwletCoordinator(hass, sock, entry.options.get(CONF_SCAN_INTERVAL))
        for sock in socks.values()
    ]

    for coordinator in coordinators:
        await coordinator.async_config_entry_first_refresh()
        hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
