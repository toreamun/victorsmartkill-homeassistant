"""VictorSmartKillEntity class."""
from abc import ABC, abstractproperty
from typing import Any, Dict, List

from homeassistant.const import ATTR_BATTERY_LEVEL, ATTR_LATITUDE, ATTR_LONGITUDE
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


class VictorSmartKillEntity(CoordinatorEntity, ABC):
    """Victor Smart-Kill entity abstract base class."""

    def __init__(
        self,
        trap_id: int,
        coordinator: DataUpdateCoordinator[List[Trap]],
    ) -> None:
        """Initialize VictorSmartKillEntity."""
        super().__init__(coordinator)

        trap = next(t for t in coordinator.data if t.id == trap_id)
        if not trap:
            raise ValueError(
                (
                    f"Trap with id {trap_id} not found in list "
                    f"{[t.id for t in coordinator.data]} of traps."
                )
            )
        self.trap: Trap = trap

    @abstractproperty
    def _name_suffix(self) -> str:
        pass

    @abstractproperty
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
    def device_info(self) -> Dict[str, Any]:
        """Return device specific attributes."""
        # See: https://developers.home-assistant.io/docs/device_registry_index/#device-properties
        return {
            "identifiers": {(DOMAIN, self.trap.id, self.trap.serial_number)},
            "name": self.trap.name,
            "model": f"{self.trap.trap_type_verbose} ({self.trap.trapstatistics.board_type})",
            "manufacturer": MANUFACTURER,
            "sw_version": self.trap.trapstatistics.firmware_version,
        }

    @property
    def _exclude_device_state_attributes(self) -> List[str]:
        return []

    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        """Return device specific state attributes."""
        state_attributes = {
            ATTR_BATTERY_LEVEL: self.trap.trapstatistics.battery_level,
            ATTR_SSID: self.trap.ssid,
            ATTR_LATITUDE: float(self.trap.lat),
            ATTR_LONGITUDE: float(self.trap.long),
            ATTR_LAST_REPORT_DATE: dt.as_local(
                self.trap.trapstatistics.last_report_date
            ),
            ATTR_LAST_KILL_DATE: dt.as_local(self.trap.trapstatistics.last_kill_date)
            if self.trap.trapstatistics.last_kill_date
            else None,
        }

        for key in self._exclude_device_state_attributes:
            if key in state_attributes:
                del state_attributes[key]

        return state_attributes
