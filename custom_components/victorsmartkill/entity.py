"""VictorSmartKillEntity class."""
from __future__ import annotations

from abc import ABC, abstractmethod
import logging
from typing import Any

from homeassistant.const import ATTR_BATTERY_LEVEL, ATTR_LATITUDE, ATTR_LONGITUDE
from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import dt
from victor_smart_kill import Trap

from custom_components.victorsmartkill.const import (
    ATTR_LAST_KILL_DATE,
    ATTR_LAST_REPORT_DATE,
    ATTR_SSID,
    DOMAIN,
    MANUFACTURER,
)

_LOGGER = logging.getLogger(__name__)


class VictorSmartKillEntity(CoordinatorEntity, ABC):
    """Victor Smart-Kill entity abstract base class."""

    def __init__(
        self,
        trap_id: int,
        coordinator: DataUpdateCoordinator[list[Trap]],
    ) -> None:
        """Initialize VictorSmartKillEntity."""
        super().__init__(coordinator)
        self.trap_id = trap_id

    @property
    def trap(self) -> Trap:
        """Trap data of current trap."""
        trap = next(t for t in self.coordinator.data if t.id == self.trap_id)
        if not trap:
            raise ValueError(
                f"Trap with id {self.trap_id} not found in list "
                f"{[t.id for t in self.coordinator.data]} of traps."
            )
        return trap

    @property
    @abstractmethod
    def _name_suffix(self) -> str:
        pass

    @property
    @abstractmethod
    def _unique_id_suffix(self) -> str:
        pass

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{self.trap.name} {self._name_suffix}"

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        # See requirements:
        # https://developers.home-assistant.io/docs/entity_registry_index#unique-id-requirements
        return f"{DOMAIN}_{self.trap.id}_{self._unique_id_suffix}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device specific attributes."""
        # See: https://developers.home-assistant.io/docs/device_registry_index/#device-properties
        return DeviceInfo(
            identifiers={(DOMAIN, self.trap.id, self.trap.serial_number)},
            name=self.trap.name,
            model=self.trap.trap_type_verbose,
            manufacturer=MANUFACTURER,
            sw_version=self.trap.trapstatistics.firmware_version,
            hw_version=self.trap.trapstatistics.board_type,
        )

    @property
    def _exclude_extra_state_attributes(self) -> list[str]:
        return []

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return device specific state attributes."""
        state_attributes = {
            ATTR_BATTERY_LEVEL: self.trap.trapstatistics.battery_level,
            ATTR_SSID: self.trap.ssid,
        }

        if self.trap.trapstatistics.last_report_date:
            state_attributes[ATTR_LAST_REPORT_DATE] = dt.as_local(
                self.trap.trapstatistics.last_report_date
            )

        if self.trap.trapstatistics.last_kill_date:
            state_attributes[ATTR_LAST_KILL_DATE] = dt.as_local(
                self.trap.trapstatistics.last_kill_date
            )

        if self.trap.lat:
            state_attributes[ATTR_LATITUDE] = self.trap.lat

        if self.trap.long:
            state_attributes[ATTR_LONGITUDE] = self.trap.long

        # remove excluded attributes
        for key in self._exclude_extra_state_attributes:
            if key in state_attributes:
                del state_attributes[key]

        return state_attributes

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        _LOGGER.debug("%s has been added to hass.", self.entity_id)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug(
            "%s received update from coordinator: %s",
            self.entity_id,
            self.state,
        )
        super()._handle_coordinator_update()
