"""Binary sensor platform for Victor Smart Kill."""
from typing import List

from homeassistant.components.binary_sensor import BinarySensorDevice
from homeassistant.helpers.entity import dt_util

from custom_components.victorsmartkill.const import (
    ATTR_LAST_KILL_DATE,
    DOMAIN,
    ICON_CAPTURED,
)
from custom_components.victorsmartkill.entity import VictorSmartKillEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    devices = [
        VictorSmartKillBinarySensor(trap.id, coordinator) for trap in coordinator.data
    ]
    async_add_devices(devices)


class VictorSmartKillBinarySensor(VictorSmartKillEntity, BinarySensorDevice):
    """Victor Smart Kill occupancy binary sensor class."""

    @property
    def _exclude_device_state_attributes(self) -> List[str]:
        return [ATTR_LAST_KILL_DATE]

    @property
    def _name_suffix(self) -> str:
        return "capture"

    @property
    def _unique_id_suffix(self) -> str:
        return "capture"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return "occupancy"

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.trap.trapstatistics.kills_present > 0

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON_CAPTURED
