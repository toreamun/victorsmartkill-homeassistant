"""
Custom integration to integrate victorsmartkill with Home Assistant.

For more details about this integration, please refer to
https://github.com/toreamun/victorsmartkill-homeassistant
"""
import asyncio
from dataclasses import dataclass, field
from datetime import timedelta
import logging
from typing import Callable, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import CALLBACK_TYPE, Config, callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.typing import EventType, HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from victor_smart_kill import Trap, VictorApi, VictorAsyncClient

from custom_components.victorsmartkill.const import (
    DOMAIN,
    EVENT_TRAP_LIST_CHANGED,
    PLATFORMS,
    STARTUP_MESSAGE,
)

SCAN_INTERVAL = timedelta(minutes=10)

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class IntegrationContext:
    """Integration context needed by platforms and/or unload."""

    coordinator: DataUpdateCoordinator
    unsubscribe_list: List[CALLBACK_TYPE] = field(default_factory=list)


async def async_setup(hass: HomeAssistantType, config: Config) -> bool:
    """Set up this integration using YAML is not supported."""
    # pylint: disable=unused-argument
    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    _LOGGER.debug("async_setup_entry %s.", entry.title)

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    coordinator = await _async_initialize_coordinator(hass, entry)
    context = IntegrationContext(coordinator=coordinator)

    hass.data[DOMAIN][entry.entry_id] = context

    await _async_forward_platform_setup(hass, entry, coordinator)
    _setup_reload(hass, entry, context)

    return True


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Handle removal of an entry."""
    _LOGGER.debug("async_unload_entry %s.", entry.title)

    context: IntegrationContext = hass.data[DOMAIN][entry.entry_id]
    is_unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in context.coordinator.platforms
            ]
        )
    )

    if is_unloaded:
        for unsubscribe in context.unsubscribe_list:
            unsubscribe()
        await context.coordinator.async_close()
        hass.data[DOMAIN].pop(entry.entry_id)

    return is_unloaded


class VictorSmartKillDataUpdateCoordinator(DataUpdateCoordinator[List[Trap]]):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistantType,
        logger: logging.Logger,
        update_interval: timedelta,
        username: str,
        password: str,
        platforms: List[str],
    ) -> None:
        """Initialize."""
        self.platforms: List[str] = platforms
        self._client = VictorAsyncClient(username, password)
        self._api = VictorApi(self._client)
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
                "Data update coordinator for Victor Smart-Kill account %s "
                "initialized with %s platforms and update interval %s."
            ),
            username,
            platforms,
            update_interval,
        )

    async def async_update_data(self) -> List[Trap]:
        """Update data via Victor Smart-Kill API."""
        try:
            if not self.data:
                traps = await self._get_traps()
            else:
                previous_trap_ids = sorted([trap.id for trap in self.data])
                traps = await self._get_traps()
                current_trap_ids = sorted([trap.id for trap in traps])
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
        except Exception as exception:
            raise UpdateFailed(exception) from exception

    @callback
    def async_add_listener(
        self, update_callback: Callable[[], None]
    ) -> Callable[[], None]:
        """Listen for data updates. Called by CoordinatorEntity."""
        # Overrided to add debug logging
        remove_listener_callback = super().async_add_listener(update_callback)
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

    async def _get_traps(self) -> List[Trap]:
        """Get list of traps from API."""
        try:
            traps = await self._api.get_traps()
            self.logger.debug(
                "Received traps list %s from Victor Smart-Kill API.",
                sorted([trap.id for trap in traps]),
            )
            return traps
        except Exception:
            self.logger.debug(
                "Error getting traps from Victor Smart-Kill API.", exc_info=True
            )
            raise


async def _async_initialize_coordinator(
    hass: HomeAssistantType, entry: ConfigEntry
) -> VictorSmartKillDataUpdateCoordinator:
    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)
    enabled_platforms = [
        platform for platform in PLATFORMS if entry.options.get(platform, True)
    ]

    coordinator = VictorSmartKillDataUpdateCoordinator(
        hass, _LOGGER, SCAN_INTERVAL, username, password, enabled_platforms
    )

    # Initialize coordinator with trap data
    await coordinator.async_refresh()
    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    return coordinator


async def _async_forward_platform_setup(
    hass: HomeAssistantType,
    entry: ConfigEntry,
    coodinator: VictorSmartKillDataUpdateCoordinator,
):
    """Forward setup to each platform."""
    for platform in coodinator.platforms:
        _LOGGER.debug("Forward setup to %s platform.", platform)
        # Use `hass.async_create_task` to avoid a circular
        # dependency between the platform and the component
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )


@callback
async def _async_config_entry_changed(hass: HomeAssistantType, entry: ConfigEntry):
    _LOGGER.info("Config entry has change. Reload integration.")
    await hass.config_entries.async_reload(entry.entry_id)


def _setup_reload(
    hass: HomeAssistantType, entry: ConfigEntry, context: IntegrationContext
):
    """Set up listeners of reload triggers."""
    # Listen for config entry changes and reload when changed.
    context.unsubscribe_list.append(
        entry.add_update_listener(_async_config_entry_changed)
    )

    @callback
    async def async_trap_list_changed(event: EventType):
        _LOGGER.info("Trap list hast changed (%s). Reload integration.", event.data)
        await hass.config_entries.async_reload(entry.entry_id)

    # Listen for trap list changes and reload when changed (new traps etc.)
    hass.bus.async_listen_once(EVENT_TRAP_LIST_CHANGED, async_trap_list_changed)
