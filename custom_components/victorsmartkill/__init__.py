"""Custom integration to integrate victorsmartkill with Home Assistant."""

from __future__ import annotations

import dataclasses as dc
import datetime as dt
import logging
from math import e
from typing import Any, Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
    Platform,
)
from homeassistant.core import CALLBACK_TYPE, callback, Event, HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import victor_smart_kill as victor

from custom_components.victorsmartkill.const import (
    DEFAULT_UPDATE_INTERVAL_MINUTES,
    DOMAIN,
    EVENT_TRAP_LIST_CHANGED,
    STARTUP_MESSAGE,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]

type VictorSmartKillConfigEntry = ConfigEntry[IntegrationContext]


@dc.dataclass(frozen=True)
class IntegrationContext:
    """Integration context needed by platforms and/or unload."""

    coordinator: DataUpdateCoordinator
    unsubscribe_list: list[CALLBACK_TYPE] = dc.field(default_factory=list)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up this integration using YAML is not supported."""
    # pylint: disable=unused-argument
    return True


async def async_setup_entry(
    hass: HomeAssistant, entry: VictorSmartKillConfigEntry
) -> bool:
    """Set up this integration using UI."""
    _LOGGER.debug("async_setup_entry %s.", entry.title)

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    if not entry.data[CONF_PASSWORD]:
        raise ConfigEntryAuthFailed("Please re-authenticate")

    coordinator = await _async_initialize_coordinator(hass, entry)
    entry.runtime_data = IntegrationContext(coordinator=coordinator)

    await hass.config_entries.async_forward_entry_setups(entry, coordinator.platforms)

    _setup_reload(hass, entry)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: VictorSmartKillConfigEntry):
    """Handle removal of an entry."""
    _LOGGER.debug("async_unload_entry %s.", entry.title)

    context: IntegrationContext = entry.runtime_data
    is_unloaded = await hass.config_entries.async_unload_platforms(
        entry, context.coordinator.platforms
    )

    if is_unloaded:
        await context.coordinator.async_close()
        for unsubscribe in context.unsubscribe_list:
            unsubscribe()

    return is_unloaded


class VictorSmartKillDataUpdateCoordinator(DataUpdateCoordinator[list[victor.Trap]]):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        update_interval: dt.timedelta,
        username: str,
        password: str,
        platforms: list[Platform],
    ) -> None:
        """Initialize."""
        self.platforms: list[Platform] = platforms
        self._client = victor.VictorAsyncClient(username, password)
        self._api = victor.VictorApi(self._client)
        self._close = False

        super().__init__(
            hass,
            logger,
            update_method=self.async_update_data,
            name=DOMAIN,
            update_interval=update_interval,
        )

        logger.info(
            (
                "Data update coordinator for Victor Smart-Kill "
                "initialized with %s platforms and update interval %s."
            ),
            platforms,
            update_interval,
        )

    async def async_update_data(self) -> list[victor.Trap]:
        """Update data via Victor Smart-Kill API."""
        try:
            if not self.data:
                traps = await self._get_traps()
            else:
                previous_trap_ids = sorted(trap.id for trap in self.data)
                traps = await self._get_traps()
                current_trap_ids = sorted(trap.id for trap in traps)
                if previous_trap_ids != current_trap_ids:
                    self.logger.debug(
                        "List of traps has changed from %s to %s.",
                        previous_trap_ids,
                        current_trap_ids,
                    )

                    self.hass.bus.async_fire(
                        EVENT_TRAP_LIST_CHANGED,
                        event_data={
                            "previous_traps": previous_trap_ids,
                            "current_traps": current_trap_ids,
                        },
                    )
            return traps
        except ConfigEntryAuthFailed:
            raise
        except Exception as exception:
            raise UpdateFailed(exception) from exception

    @callback
    def async_add_listener(
        self, update_callback: CALLBACK_TYPE, context: Any = None
    ) -> Callable[[], None]:
        """Listen for data updates. Called by CoordinatorEntity."""
        # Overrided to add debug logging
        remove_listener_callback = super().async_add_listener(update_callback, context)
        self.logger.debug("Listener %s added to coordinator.", update_callback.__name__)
        return remove_listener_callback

    async def async_refresh(self) -> None:
        """Refresh data."""
        if self._close:
            self.logger.debug("Coordinator is closed or closing. Ignore refresh.")
        else:
            await super().async_refresh()

    async def async_close(self) -> None:
        """Close resources."""
        self.logger.debug("Close API client.")
        self._close = True
        await self._client.aclose()

    async def _get_traps(self) -> list[victor.Trap]:
        """Get list of traps from API."""
        try:
            traps = await self._api.get_traps()
            self.logger.debug(
                "Received traps list %s from Victor Smart-Kill API.",
                sorted(trap.id for trap in traps),
            )
            return traps
        except victor.InvalidCredentialsError as ex:
            self.logger.debug("Invalid credentials: %s", repr(ex))
            raise ConfigEntryAuthFailed from ex
        except Exception as ex:
            self.logger.debug(
                "Error getting traps from Victor Smart-Kill API: %s",
                repr(ex),
                exc_info=True,
            )
            raise


async def _async_initialize_coordinator(
    hass: HomeAssistant, entry: VictorSmartKillConfigEntry
) -> VictorSmartKillDataUpdateCoordinator:
    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)
    enabled_platforms = [
        platform for platform in PLATFORMS if entry.options.get(platform, True)
    ]
    update_interval_minutes = entry.options.get(
        CONF_SCAN_INTERVAL, DEFAULT_UPDATE_INTERVAL_MINUTES
    )
    update_interval_minutes = (
        update_interval_minutes
        if update_interval_minutes > 0
        else DEFAULT_UPDATE_INTERVAL_MINUTES
    )
    update_interval = dt.timedelta(minutes=update_interval_minutes)

    coordinator = VictorSmartKillDataUpdateCoordinator(
        hass, _LOGGER, update_interval, username, password, enabled_platforms
    )

    # Initialize coordinator with trap data
    await coordinator.async_refresh()
    if not coordinator.last_update_success:
        await coordinator.async_close()
        raise ConfigEntryNotReady

    return coordinator


@callback
async def _async_config_entry_changed(
    hass: HomeAssistant, entry: VictorSmartKillConfigEntry
) -> None:
    _LOGGER.info("Config entry has change. Reload integration.")
    await hass.config_entries.async_reload(entry.entry_id)


def _setup_reload(hass: HomeAssistant, entry: VictorSmartKillConfigEntry) -> None:
    """Set up listeners of reload triggers."""
    # Listen for config entry changes and reload when changed.
    entry.runtime_data.unsubscribe_list.append(
        entry.add_update_listener(_async_config_entry_changed)
    )

    @callback
    async def async_trap_list_changed(event: Event) -> None:
        _LOGGER.info("Trap list hast changed (%s). Reload integration.", event.data)
        await hass.config_entries.async_reload(entry.entry_id)

    # Listen for trap list changes and reload when changed (new traps etc.)
    hass.bus.async_listen_once(EVENT_TRAP_LIST_CHANGED, async_trap_list_changed)
