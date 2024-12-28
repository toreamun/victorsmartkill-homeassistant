"""Binary sensor platform for Victor Smart-Kill."""

from __future__ import annotations

import logging
from typing import Callable, Iterable

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
import victor_smart_kill as victor

from custom_components.victorsmartkill import (
    IntegrationContext,
    VictorSmartKillConfigEntry,
)
from custom_components.victorsmartkill.const import (
    ATTR_LAST_KILL_DATE,
    DOMAIN,
    ICON_CAPTURED,
)
from custom_components.victorsmartkill.entity import VictorSmartKillEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: VictorSmartKillConfigEntry,
    async_add_entities: Callable[[Iterable[Entity], bool | None], None],
) -> None:
    """Set up binary_sensor platform."""
    context: IntegrationContext = entry.runtime_data
    traps: list[victor.Trap] = context.coordinator.data

    entities = []
    for trap in traps:
        entities.extend([VictorSmartKillBinarySensor(trap.id, context.coordinator)])
        _LOGGER.debug(
            "Add %s binary sensors for trap named '%s' with Victor trap id %d.",
            [f"{type(entity).__name__}" for entity in entities],
            trap.name,
            trap.id,
        )

    async_add_entities(entities, False)


class VictorSmartKillBinarySensor(VictorSmartKillEntity, BinarySensorEntity):
    """Victor Smart-Kill occupancy binary sensor class."""

    @property
    def _exclude_extra_state_attributes(self) -> list[str]:
        return [ATTR_LAST_KILL_DATE]

    @property
    def _name_suffix(self) -> str:
        return "capture"

    @property
    def _unique_id_suffix(self) -> str:
        return "capture"

    @property
    def device_class(self) -> BinarySensorDeviceClass:
        """Return the class of this binary_sensor."""
        return BinarySensorDeviceClass.OCCUPANCY

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.trap.trapstatistics.kills_present > 0

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return ICON_CAPTURED
