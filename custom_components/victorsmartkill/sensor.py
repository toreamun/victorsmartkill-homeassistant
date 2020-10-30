"""Sensor platform for victorsmartkill."""
import logging
from typing import Callable, Iterable, List, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_BATTERY_LEVEL,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_TIMESTAMP,
    PERCENTAGE,
    TEMP_CELSIUS,
)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.util import dt
from victor_smart_kill import Trap

from custom_components.victorsmartkill.const import (
    ATTR_LAST_KILL_DATE,
    ATTR_LAST_REPORT_DATE,
    DOMAIN,
    ICON_COUNTER,
    SIGNAL_DBM,
)
from custom_components.victorsmartkill.entity import VictorSmartKillEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistantType,
    entry: ConfigEntry,
    async_add_entities: Callable[[Iterable[Entity], Optional[bool]], None],
) -> None:
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    traps: List[Trap] = coordinator.data

    entities = []
    for trap in traps:
        entities.extend(
            [
                KillsPresentSensor(trap.id, coordinator),
                TotalKillsSensor(trap.id, coordinator),
                TotalEscapesSensor(trap.id, coordinator),
                TotalRetreatsSensor(trap.id, coordinator),
                WirelessNetworkRssiSensor(trap.id, coordinator),
                TemperatureSensor(trap.id, coordinator),
                LastKillDateSensor(trap.id, coordinator),
                LastReportDateSensor(trap.id, coordinator),
                BatterySensor(trap.id, coordinator),
            ]
        )
        _LOGGER.debug(
            "Add %s sensors for trap named '%s' with Victor trap id %d.",
            [f"{type(entity).__name__}" for entity in entities],
            trap.name,
            trap.id,
        )

    async_add_entities(entities, False)


class KillsPresentSensor(VictorSmartKillEntity):
    """Kills present sensor class."""

    @property
    def _name_suffix(self) -> str:
        return "kills present"

    @property
    def _unique_id_suffix(self) -> str:
        return "kills_present"

    @property
    def state(self) -> int:
        """Return the state of the sensor as present kills."""
        return self.trap.trapstatistics.kills_present

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return ICON_COUNTER


class TotalKillsSensor(VictorSmartKillEntity):
    """Total kills sensor class."""

    @property
    def _name_suffix(self) -> str:
        return "total kills"

    @property
    def _unique_id_suffix(self) -> str:
        return "total_kills"

    @property
    def state(self) -> Optional[int]:
        """Return the state of the sensor as total kills."""
        return self.trap.trapstatistics.total_kills

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return ICON_COUNTER


class TotalEscapesSensor(VictorSmartKillEntity):
    """Total escapes sensor class."""

    @property
    def _exclude_device_state_attributes(self) -> List[str]:
        return [ATTR_LAST_KILL_DATE]

    @property
    def _name_suffix(self) -> str:
        return "total escapes"

    @property
    def _unique_id_suffix(self) -> str:
        return "total_escapes"

    @property
    def state(self) -> Optional[int]:
        """Return the state of the sensor as total escapes."""
        return self.trap.trapstatistics.total_escapes

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return ICON_COUNTER


class TotalRetreatsSensor(VictorSmartKillEntity):
    """Total retreats sensor class."""

    @property
    def _exclude_device_state_attributes(self) -> List[str]:
        return [ATTR_LAST_KILL_DATE]

    @property
    def _name_suffix(self) -> str:
        return "total retreats"

    @property
    def _unique_id_suffix(self) -> str:
        return "total_retreats"

    @property
    def state(self) -> Optional[int]:
        """Return the state of the sensor as total retreats."""
        return self.trap.trapstatistics.total_retreats

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return ICON_COUNTER


class WirelessNetworkRssiSensor(VictorSmartKillEntity):
    """Wireless network rssi sensor class."""

    @property
    def _exclude_device_state_attributes(self) -> List[str]:
        return [ATTR_LAST_KILL_DATE]

    @property
    def _name_suffix(self) -> str:
        return "wireless network rssi"

    @property
    def _unique_id_suffix(self) -> str:
        return "wireless_network_rssi"

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        return self.trap.trapstatistics.wireless_network_rssi

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity."""
        return SIGNAL_DBM

    @property
    def device_class(self) -> str:
        """Return the class of this device, from component DEVICE_CLASSES."""
        return DEVICE_CLASS_SIGNAL_STRENGTH


class TemperatureSensor(VictorSmartKillEntity):
    """Temperature sensor class."""

    @property
    def _exclude_device_state_attributes(self) -> List[str]:
        return [ATTR_LAST_KILL_DATE]

    @property
    def _name_suffix(self) -> str:
        return "temperature"

    @property
    def _unique_id_suffix(self) -> str:
        return "temperature"

    @property
    def state(self) -> float:
        """Return the state of the sensor."""
        return self.trap.trapstatistics.temperature_celcius

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity."""
        return TEMP_CELSIUS

    @property
    def device_class(self) -> str:
        """Return the class of this device, from component DEVICE_CLASSES."""
        return DEVICE_CLASS_TEMPERATURE


class LastKillDateSensor(VictorSmartKillEntity):
    """Last kill date sensor class."""

    @property
    def _exclude_device_state_attributes(self) -> List[str]:
        return [ATTR_LAST_KILL_DATE]

    @property
    def _name_suffix(self) -> str:
        return "last kill date"

    @property
    def _unique_id_suffix(self) -> str:
        return "last_kill_date"

    @property
    def state(self) -> Optional[str]:
        """Return the state of the sensor."""
        if self.trap.trapstatistics.last_kill_date:
            return dt.as_local(self.trap.trapstatistics.last_kill_date).isoformat()
        return None

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity."""
        return "ISO8601"

    @property
    def device_class(self) -> str:
        """Return the class of this device, from component DEVICE_CLASSES."""
        return DEVICE_CLASS_TIMESTAMP


class LastReportDateSensor(VictorSmartKillEntity):
    """Last report date sensor class."""

    @property
    def _exclude_device_state_attributes(self) -> List[str]:
        return [ATTR_LAST_REPORT_DATE]

    @property
    def _name_suffix(self) -> str:
        return "last report date"

    @property
    def _unique_id_suffix(self) -> str:
        return "last_report_date"

    @property
    def state(self) -> Optional[str]:
        """Return the state of the sensor."""
        if self.trap.trapstatistics.last_report_date:
            return dt.as_local(self.trap.trapstatistics.last_report_date).isoformat()
        return None

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity."""
        return "ISO8601"

    @property
    def device_class(self) -> str:
        """Return the class of this device, from component DEVICE_CLASSES."""
        return DEVICE_CLASS_TIMESTAMP


class BatterySensor(VictorSmartKillEntity):
    """Battery sensor class."""

    @property
    def _exclude_device_state_attributes(self) -> List[str]:
        return [ATTR_LAST_KILL_DATE, ATTR_BATTERY_LEVEL]

    @property
    def _name_suffix(self) -> str:
        return "battery level"

    @property
    def _unique_id_suffix(self) -> str:
        return "battery_level"

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        return self.trap.trapstatistics.battery_level

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity."""
        return PERCENTAGE

    @property
    def device_class(self) -> str:
        """Return the class of this device, from component DEVICE_CLASSES."""
        return DEVICE_CLASS_BATTERY
