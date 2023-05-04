"""The Owlet Smart Sock integration."""
from __future__ import annotations

import logging

from pyowletapi.owlet import Owlet
from pyowletapi.exceptions import OwletAuthenticationError, OwletDevicesError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, CONF_OWLET_REGION, CONF_OWLET_USERNAME, CONF_OWLET_PASSWORD
from .coordinator import OwletCoordinator

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Owlet Smart Sock from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    owlet = Owlet(
        entry.data[CONF_OWLET_REGION],
        entry.data[CONF_OWLET_USERNAME],
        entry.data[CONF_OWLET_PASSWORD],
        async_get_clientsession(hass),
    )

    try:
        await owlet.authenticate()
    except OwletAuthenticationError as err:
        _LOGGER.error("Login failed %s", err)
        return False

    existing_socks = entry.data["devices"]
    new_socks = []
    try:
        socks = await owlet.get_devices()
    except OwletDevicesError:
        pass

    [new_socks.append(sock) for sock in socks if sock not in existing_socks]

    if new_socks:
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, **{"devices": socks}}
        )

    coordinators = [OwletCoordinator(hass, sock) for sock in socks.values()]

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
