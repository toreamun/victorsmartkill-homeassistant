"""Adds config flow for Victor Smart-Kill."""
import logging
from typing import Any, Dict, Optional

from homeassistant.config_entries import (
    CONN_CLASS_CLOUD_POLL,
    ConfigEntry,
    ConfigFlow,
    OptionsFlow,
)
from homeassistant.const import CONF_PASSWORD, CONF_SCAN_INTERVAL, CONF_USERNAME
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from httpx import HTTPStatusError
from victor_smart_kill import VictorAsyncClient
import voluptuous as vol  # type: ignore

from custom_components.victorsmartkill.const import (  # pylint: disable=unused-import
    BINARY_SENSOR,
    DEFAULT_UPDATE_INTERVAL_MINUTES,
    DOMAIN,
    SENSOR,
)

_LOGGER = logging.getLogger(__name__)


class VictorSmartKillFlowHandler(ConfigFlow, domain=DOMAIN):  # type: ignore
    """Config flow for Victor Smart-Kill."""

    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle a flow initiated by the user."""
        self._errors = {}

        if user_input is not None:
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
            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> "OptionsFlow":
        """Get the options flow for this handler."""
        return VictorSmartKillOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str}
            ),
            errors=self._errors,
        )

    async def _test_credentials(self, username, password):
        """Return true if credentials is valid."""
        try:
            async with VictorAsyncClient(username, password) as client:
                _LOGGER.debug(
                    "Fetch API-token for user '%s' to test for correct username and password.",
                    username,
                )
                await client.fetch_token()
        except HTTPStatusError as ex:
            if ex.response.status_code == 400 or ex.response.status_code == 401:
                _LOGGER.debug(
                    "HTTP status %d: %s", ex.response.status_code, ex.response.text
                )
                return False
            raise
        except Exception:
            _LOGGER.debug(
                "Unexpected error from Victor Smart-Kill API when fetching API-token.",
                exc_info=True,
            )
            raise

        return True


class VictorSmartKillOptionsFlowHandler(OptionsFlow):
    """Victor Smart-Kill config flow options handler."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        options = {
            vol.Required(
                BINARY_SENSOR, default=self.options.get(BINARY_SENSOR, True)
            ): bool,
            vol.Required(SENSOR, default=self.options.get(SENSOR, True)): bool,
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

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_USERNAME), data=self.options
        )
