"""Constants for victorsmartkill."""
# Base component constants
MANUFACTURER = "VictorPest.com"
NAME = "Victor Smart Kill"
DOMAIN = "victorsmartkill"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ISSUE_URL = "https://github.com/toreamun/victorsmartkill-homeassistant/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
PLATFORMS = [BINARY_SENSOR, SENSOR]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

EVENT_TRAP_LIST_CHANGED = "victorsmartkill_trap_list_changed"

ICON_COUNTER = "mdi:counter"
ICON_CAPTURED = "mdi:emoticon-dead-outline"


# state attributes
ATTR_LAST_REPORT_DATE = "last_report_date"
ATTR_LAST_KILL_DATE = "last_kill_date"
ATTR_SSID = "ssid"


# units
SIGNAL_DBM = "dBm"
