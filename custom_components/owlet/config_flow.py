"""Config flow for Owlet Smart Sock integration."""
from __future__ import annotations

import logging
from typing import Any

from pyowletapi.owlet import Owlet
from pyowletapi.exceptions import (
    OwletConnectionError,
    OwletAuthenticationError,
    OwletDevicesError,
)

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    CONF_OWLET_REGION,
    CONF_OWLET_USERNAME,
    CONF_OWLET_PASSWORD,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_OWLET_REGION): vol.In(["europe", "world"]),
        vol.Required(CONF_OWLET_USERNAME): str,
        vol.Required(CONF_OWLET_PASSWORD): str,
    }
)


class OwletConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Owlet Smart Sock."""

    VERSION = 1

    def __init__(self) -> None:
        self._entry: ConfigEntry
        self._region: str
        self._username: str
        self._password: str

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            self._region = user_input[CONF_OWLET_REGION]
            self._username = user_input[CONF_OWLET_USERNAME]
            self._password = user_input[CONF_OWLET_PASSWORD]

            owlet = Owlet(
                self._region,
                self._username,
                self._password,
                session=async_get_clientsession(self.hass),
            )

            await self.async_set_unique_id(self._username.lower())
            self._abort_if_unique_id_configured()

            try:
                await owlet.authenticate()
                try:
                    devices = await owlet.get_devices()
                except OwletDevicesError:
                    errors["base"] = "no_devices"

            except OwletConnectionError:
                errors["base"] = "cannot_connect"
            except OwletAuthenticationError:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title="Owlet",
                    data={
                        CONF_OWLET_REGION: self._region,
                        CONF_OWLET_USERNAME: self._username,
                        CONF_OWLET_PASSWORD: self._password,
                        "devices": list(devices.keys()),
                    },
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
