"""Sensor platform for victorsmartkill."""

from __future__ import annotations

import dataclasses as dc
import logging
from typing import TYPE_CHECKING

from homeassistant import util
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import (
    ATTR_BATTERY_LEVEL,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    EntityCategory,
    UnitOfTemperature,
)

from custom_components.victorsmartkill.const import (
    ATTR_LAST_KILL_DATE,
    ATTR_LAST_REPORT_DATE,
    ICON_COUNTER,
)
from custom_components.victorsmartkill.entity import VictorSmartKillEntity

if TYPE_CHECKING:
    from collections.abc import Callable
    from datetime import datetime

    import victor_smart_kill as victor
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.typing import StateType

    from custom_components.victorsmartkill import (
        IntegrationContext,
        VictorSmartKillConfigEntry,
        VictorSmartKillDataUpdateCoordinator,
    )

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: VictorSmartKillConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor platform."""
    context: IntegrationContext = entry.runtime_data
    traps: list[victor.Trap] = context.coordinator.data

    entities = []
    for trap in traps:
        entities.extend(_create_trap_sensors(context.coordinator, trap))
        _LOGGER.debug(
            "Add %s sensors for trap named '%s' with Victor trap id %d.",
            [f"{type(entity).__name__}" for entity in entities],
            trap.name,
            trap.id,
        )

    async_add_entities(entities, update_before_add=False)


def _create_trap_sensors(
    coordinator: VictorSmartKillDataUpdateCoordinator, trap: victor.Trap
) -> list[VictorSmartKillSensor]:
    return [
        VictorSmartKillSensor(
            trap.id,
            coordinator,
            VictorSmartKillSensorEntityDescription(
                key="kills_present",
                name="kills present",
                entity_category=EntityCategory.DIAGNOSTIC,
                icon=ICON_COUNTER,
                exclude_extra_state_attributes=[ATTR_LATITUDE, ATTR_LONGITUDE],
                value_func=lambda t: t.trapstatistics.kills_present,
            ),
        ),
        VictorSmartKillSensor(
            trap.id,
            coordinator,
            VictorSmartKillSensorEntityDescription(
                key="total_kills",
                name="total kills",
                entity_category=EntityCategory.DIAGNOSTIC,
                icon=ICON_COUNTER,
                exclude_extra_state_attributes=[ATTR_LATITUDE, ATTR_LONGITUDE],
                value_func=lambda t: t.trapstatistics.total_kills,
            ),
        ),
        VictorSmartKillSensor(
            trap.id,
            coordinator,
            VictorSmartKillSensorEntityDescription(
                key="total_escapes",
                name="total escapes",
                entity_category=EntityCategory.DIAGNOSTIC,
                icon=ICON_COUNTER,
                exclude_extra_state_attributes=[
                    ATTR_LAST_KILL_DATE,
                    ATTR_LATITUDE,
                    ATTR_LONGITUDE,
                ],
                value_func=lambda t: t.trapstatistics.total_escapes,
            ),
        ),
        VictorSmartKillSensor(
            trap.id,
            coordinator,
            VictorSmartKillSensorEntityDescription(
                key="total_retreats",
                name="total retreats",
                entity_category=EntityCategory.DIAGNOSTIC,
                icon=ICON_COUNTER,
                exclude_extra_state_attributes=[
                    ATTR_LAST_KILL_DATE,
                    ATTR_LATITUDE,
                    ATTR_LONGITUDE,
                ],
                value_func=lambda t: t.trapstatistics.total_retreats,
                entity_registry_enabled_default=False,
            ),
        ),
        VictorSmartKillSensor(
            trap.id,
            coordinator,
            VictorSmartKillSensorEntityDescription(
                key="wireless_network_rssi",
                name="wireless network rssi",
                entity_category=EntityCategory.DIAGNOSTIC,
                exclude_extra_state_attributes=[
                    ATTR_LAST_KILL_DATE,
                    ATTR_LATITUDE,
                    ATTR_LONGITUDE,
                ],
                value_func=lambda t: t.trapstatistics.wireless_network_rssi,
                native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
            ),
        ),
        VictorSmartKillSensor(
            trap.id,
            coordinator,
            VictorSmartKillSensorEntityDescription(
                key="temperature",
                name="temperature",
                entity_category=EntityCategory.DIAGNOSTIC,
                exclude_extra_state_attributes=[
                    ATTR_LAST_KILL_DATE,
                    ATTR_LATITUDE,
                    ATTR_LONGITUDE,
                ],
                value_func=lambda t: t.trapstatistics.temperature_celcius,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                device_class=SensorDeviceClass.TEMPERATURE,
                entity_registry_enabled_default=trap.trapstatistics.temperature
                is not None,
            ),
        ),
        VictorSmartKillSensor(
            trap.id,
            coordinator,
            VictorSmartKillSensorEntityDescription(
                key="last_kill_date",
                name="last kill date",
                entity_category=EntityCategory.DIAGNOSTIC,
                exclude_extra_state_attributes=[
                    ATTR_LAST_KILL_DATE,
                    ATTR_LATITUDE,
                    ATTR_LONGITUDE,
                ],
                value_func=lambda t: t.trapstatistics.last_kill_date,
                device_class=SensorDeviceClass.TIMESTAMP,
            ),
        ),
        VictorSmartKillSensor(
            trap.id,
            coordinator,
            VictorSmartKillSensorEntityDescription(
                key="last_report_date",
                name="last report date",
                entity_category=EntityCategory.DIAGNOSTIC,
                exclude_extra_state_attributes=[
                    ATTR_LAST_REPORT_DATE,
                    ATTR_LATITUDE,
                    ATTR_LONGITUDE,
                ],
                value_func=lambda t: t.trapstatistics.last_report_date,
                device_class=SensorDeviceClass.TIMESTAMP,
            ),
        ),
        VictorSmartKillSensor(
            trap.id,
            coordinator,
            VictorSmartKillSensorEntityDescription(
                key="battery_level",
                name="battery level",
                entity_category=EntityCategory.DIAGNOSTIC,
                exclude_extra_state_attributes=[
                    ATTR_LAST_KILL_DATE,
                    ATTR_BATTERY_LEVEL,
                    ATTR_LATITUDE,
                    ATTR_LONGITUDE,
                ],
                value_func=lambda t: t.trapstatistics.battery_level,
                native_unit_of_measurement=PERCENTAGE,
                device_class=SensorDeviceClass.BATTERY,
            ),
        ),
    ]


@dc.dataclass(frozen=True)
class EntityDescriptionRequiredKeysMixin:  # pylint: disable=too-few-public-methods
    """Mixin for required keys."""

    value_func: Callable[[victor.Trap], StateType | datetime]


@dc.dataclass(frozen=True)
class VictorSmartKillSensorEntityDescription(
    SensorEntityDescription, EntityDescriptionRequiredKeysMixin
):  # pylint: disable=too-few-public-methods
    """Describes Victor Smart-Kill sensor."""

    exclude_extra_state_attributes: list[str] | None = None


class VictorSmartKillSensor(VictorSmartKillEntity, SensorEntity):
    """Sensor base class."""

    def __init__(
        self,
        trap_id: int,
        coordinator: VictorSmartKillDataUpdateCoordinator,
        description: VictorSmartKillSensorEntityDescription,
    ) -> None:
        """Initialize VictorSmartKillSensor."""
        super().__init__(trap_id, coordinator)
        self.entity_description: VictorSmartKillSensorEntityDescription = description

    @property
    def _exclude_extra_state_attributes(self) -> list[str]:
        return (
            self.entity_description.exclude_extra_state_attributes
            if self.entity_description.exclude_extra_state_attributes
            else []
        )

    @property
    def _name_suffix(self) -> str:
        return str(self.entity_description.name)

    @property
    def _unique_id_suffix(self) -> str:
        return f"{util.slugify(str(self.entity_description.name))}"

    @property
    def native_value(self) -> StateType | datetime:
        """Return the value reported by the sensor."""
        return self.entity_description.value_func(self.trap)
