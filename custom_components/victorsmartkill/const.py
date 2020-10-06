"""Constants for victorsmartkill."""
# Base component constants
MANUFACTURER = "VictorPest.com"
NAME = "Victor Smart-Kill"
DOMAIN = "victorsmartkill"
DOMAIN_DATA = f"{DOMAIN}_data"

ISSUE_URL = "https://github.com/toreamun/victorsmartkill-homeassistant/issues"

# Icons
ICON_COUNTER = "mdi:counter"
ICON_CAPTURED = "mdi:emoticon-dead-outline"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
PLATFORMS = [BINARY_SENSOR, SENSOR]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

EVENT_TRAP_LIST_CHANGED = "victorsmartkill_trap_list_changed"


# state attributes
ATTR_LAST_REPORT_DATE = "last_report_date"
ATTR_LAST_KILL_DATE = "last_kill_date"
ATTR_SSID = "ssid"


# units
SIGNAL_DBM = "dBm"
