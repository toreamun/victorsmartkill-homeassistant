"""Constants for victorsmartkill."""

from __future__ import annotations

# Base component constants
MANUFACTURER = "VictorPest.com"
NAME = "Victor Smart-Kill"
DOMAIN = "victorsmartkill"
ISSUE_URL = "https://github.com/toreamun/victorsmartkill-homeassistant/issues"


# Icons
ICON_COUNTER = "mdi:counter"
ICON_CAPTURED = "mdi:emoticon-dead-outline"


# Configuration and options
DEFAULT_UPDATE_INTERVAL_MINUTES = 10


# state attributes
ATTR_LAST_REPORT_DATE = "last_report_date"
ATTR_LAST_KILL_DATE = "last_kill_date"
ATTR_SSID = "ssid"

# events
EVENT_TRAP_LIST_CHANGED = "victorsmartkill_trap_list_changed"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
