"""Config flow for Owlet Smart Sock integration."""
from __future__ import annotations

import logging
from typing import Any

from pyowletapi.api import OwletAPI
from pyowletapi.sock import Sock
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
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_OWLET_REGION,
    CONF_OWLET_USERNAME,
    CONF_OWLET_PASSWORD,
    CONF_OWLET_POLLINTERVAL,
    CONF_OWLET_TOKEN,
    CONF_OWLET_EXPIRY,
    POLLING_INTERVAL,
    SUPPORTED_VERSIONS,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("region"): vol.In(["europe", "world"]),
        vol.Required("username"): str,
        vol.Required("password"): str,
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
        self._devices: dict[str, Sock]

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            self._region = user_input[CONF_OWLET_REGION]
            self._username = user_input[CONF_OWLET_USERNAME]
            self._password = user_input[CONF_OWLET_PASSWORD]

            owlet_api = OwletAPI(
                self._region,
                self._username,
                self._password,
                session=async_get_clientsession(self.hass),
            )

            await self.async_set_unique_id(self._username.lower())
            self._abort_if_unique_id_configured()

            try:
                token = await owlet_api.authenticate()
                try:
                    await owlet_api.get_devices(SUPPORTED_VERSIONS)
                    return self.async_create_entry(
                        title=self._username,
                        data={
                            CONF_OWLET_REGION: self._region,
                            CONF_OWLET_USERNAME: self._username,
                            CONF_OWLET_PASSWORD: self._password,
                            CONF_OWLET_TOKEN: token[CONF_OWLET_TOKEN],
                            CONF_OWLET_EXPIRY: token[CONF_OWLET_EXPIRY],
                        },
                        options={CONF_OWLET_POLLINTERVAL: POLLING_INTERVAL},
                    )
                except OwletDevicesError:
                    errors["base"] = "no_devices"

            except OwletConnectionError:
                errors["base"] = "cannot_connect"
            except OwletAuthenticationError:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a options flow for owlet"""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialise options flow"""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle options flow"""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_OWLET_POLLINTERVAL,
                    default=self.config_entry.options.get(CONF_OWLET_POLLINTERVAL),
                ): vol.All(vol.Coerce(int), vol.Range(min=10)),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
