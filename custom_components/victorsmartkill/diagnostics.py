"""Victor Smart-Kill diagnostics."""

from __future__ import annotations

import dataclasses as dc
from typing import TYPE_CHECKING, Any

from homeassistant.components.diagnostics import async_redact_data

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from custom_components.victorsmartkill import (
        IntegrationContext,
        VictorSmartKillConfigEntry,
    )

TO_REDACT_DATA = {
    "lorawan_app_key",
    "ssid",
    "serial_number",
    "lat",
    "long",
    "owner_email",
    "owner_name",
}

TO_REDACT_CONFIG = {
    "title",
    "username",
    "password",
    "unique_id",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    config_entry: VictorSmartKillConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    diagnostics: dict[str, Any] = {
        "config_entry": async_redact_data(config_entry.as_dict(), TO_REDACT_CONFIG)
    }

    context: IntegrationContext = config_entry.runtime_data
    if context and context.coordinator:
        if context.coordinator.data:
            diagnostics["data"] = async_redact_data(
                {x.id: dc.asdict(x) for x in context.coordinator.data}, TO_REDACT_DATA
            )
        diagnostics["last_exception"] = context.coordinator.last_exception

    return diagnostics
