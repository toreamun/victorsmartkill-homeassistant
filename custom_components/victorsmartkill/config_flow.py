"""Adds config flow for Victor Smart-Kill."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import homeassistant.helpers.config_validation as cv
import victor_smart_kill as victor
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
    Platform,
)
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError

from custom_components.victorsmartkill.const import (  # pylint: disable=unused-import
    DEFAULT_UPDATE_INTERVAL_MINUTES,
    DOMAIN,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from homeassistant.data_entry_flow import FlowResult

    from custom_components.victorsmartkill import VictorSmartKillConfigEntry

_LOGGER = logging.getLogger(__name__)


class VictorSmartKillFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for Victor Smart-Kill."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle a flow initiated by the user."""
        self._errors = {}

        if user_input is None:
            # defaults
            user_input = {
                CONF_USERNAME: None,
                CONF_PASSWORD: None,
            }
        else:
            valid = await self._test_credentials(
                user_input[CONF_USERNAME], user_input[CONF_PASSWORD]
            )
            if valid:
                await self.async_set_unique_id(user_input[CONF_USERNAME])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )
            self._errors["base"] = "auth"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME, default=user_input[CONF_USERNAME]): str,
                    vol.Required(CONF_PASSWORD, default=user_input[CONF_PASSWORD]): str,
                }
            ),
            errors=self._errors,
        )

    async def async_step_reauth(
        self, user_input: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Perform reauth upon an API authentication error."""
        user_input_copy = dict(user_input)
        if user_input and user_input[CONF_PASSWORD]:
            # remove password to stop re-auth in async_setup_entry
            user_input_copy = dict(user_input)
            user_input_copy[CONF_PASSWORD] = None
            config_entry = self.hass.config_entries.async_get_entry(
                self.context["entry_id"]
            )
            if config_entry is not None:
                self.hass.config_entries.async_update_entry(
                    config_entry, data=user_input_copy
                )

        return await self.async_step_reauth_confirm(user_input_copy)

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Dialog that informs the user that reauth is required."""
        config_entry: VictorSmartKillConfigEntry | None
        if user_input is None:
            if (
                config_entry := self.hass.config_entries.async_get_entry(
                    self.context["entry_id"]
                )
            ) is None:
                msg = "Unknown config entry"
                raise HomeAssistantError(msg)
            user_input = dict(config_entry.data)
        elif user_input.get(CONF_PASSWORD):
            valid = await self._test_credentials(
                user_input[CONF_USERNAME], user_input[CONF_PASSWORD]
            )
            if valid:
                if (
                    config_entry := self.hass.config_entries.async_get_entry(
                        self.context["entry_id"]
                    )
                ) is None:
                    msg = "Unknown config entry"
                    raise HomeAssistantError(msg)
                data = {
                    **config_entry.data,
                    CONF_USERNAME: user_input[CONF_USERNAME],
                    CONF_PASSWORD: user_input[CONF_PASSWORD],
                }
                self.hass.config_entries.async_update_entry(config_entry, data=data)
                await self.hass.config_entries.async_reload(config_entry.entry_id)
                return self.async_abort(reason="reauth_successful")

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME, default=user_input[CONF_USERNAME]): str,
                    vol.Required(CONF_PASSWORD, default=user_input[CONF_PASSWORD]): str,
                }
            ),
            errors=self._errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: VictorSmartKillConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        return VictorSmartKillOptionsFlowHandler(config_entry)

    async def _test_credentials(self, username: str, password: str) -> bool:
        """Return true if credentials is valid."""
        try:
            async with victor.VictorAsyncClient(username, password) as client:
                _LOGGER.debug(
                    "Fetch API-token to test for correct username and password.",
                )
                await client.fetch_token()
                return True
        except victor.InvalidCredentialsError:
            return False
        except Exception:
            _LOGGER.debug(
                "Unexpected error from Victor Smart-Kill API when fetching API-token.",
                exc_info=True,
            )
            raise


class VictorSmartKillOptionsFlowHandler(OptionsFlow):
    """Victor Smart-Kill config flow options handler."""

    def __init__(self, config_entry: VictorSmartKillConfigEntry) -> None:
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,  # noqa: ARG002 Unused function argument: `user_input`
    ) -> FlowResult:
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        options = {
            vol.Required(
                str(Platform.BINARY_SENSOR),
                default=self.options.get(Platform.BINARY_SENSOR, True),
            ): bool,
            vol.Required(
                str(Platform.SENSOR), default=self.options.get(Platform.SENSOR, True)
            ): bool,
            vol.Optional(
                CONF_SCAN_INTERVAL,
                default=self.options.get(
                    CONF_SCAN_INTERVAL, DEFAULT_UPDATE_INTERVAL_MINUTES
                ),
            ): cv.positive_int,
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(options),
        )

    async def _update_options(self) -> FlowResult:
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_USERNAME), data=self.options
        )
