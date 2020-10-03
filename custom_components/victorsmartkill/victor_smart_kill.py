"""Victor Smart Kill API module."""
from dataclasses import dataclass
from datetime import datetime
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from httpx import URL, AsyncClient, Response, codes
from marshmallow import RAISE
from marshmallow.schema import Schema
import marshmallow_dataclass

log = logging.getLogger(__name__)

DEFAULT_BASE_URL = URL("https://www.victorsmartkill.com")


class VictorAsyncClient(AsyncClient):
    """An asynchronous HTTP client to Victor Smart Kill API."""

    def __init__(self, username: str, password: str, **kwargs) -> None:
        """
        Initialize VictorAsyncClient.

        :param username: User name used to access Victor API.
        :param username: Password used to access Victor API.
        :param kwargs: Arguments to pass to the httpx.AsyncClient constructor.
        """
        super(VictorAsyncClient, self).__init__(**kwargs)

        if not username:
            raise ValueError("User name is required.")

        if not password:
            raise ValueError("Password is required.")

        if self.base_url == URL():
            self.base_url = DEFAULT_BASE_URL

        self._credentials = {"password": password, "username": username}
        self._token = None

    @property
    def has_token(self) -> bool:
        """Boolean that indicates whether this session has an token or not."""
        return self._token is not None

    async def fetch_token(self) -> None:
        """Fetch token and store in client."""
        self._token = None

        response = await super(VictorAsyncClient, self).request(
            "POST",
            "api-token-auth/",
            json=self._credentials,
        )

        response.raise_for_status()

        token = response.json().get("token")
        if token:
            self._token = token
            log.info("Fetched token.")
        else:
            raise Exception("Unexpected response from token endpoind")

    async def request(self, method, url, data=None, headers=None, **kwargs) -> Response:
        """Intercept all requests and add token. Fetches token if needed."""
        return await self._request(
            True, method, url, data=data, headers=headers, **kwargs
        )

    async def _request(
        self, retry_unauthorized, method, url, data=None, headers=None, **kwargs
    ) -> Response:
        if not self.has_token:
            log.info("Token is missing. Fetch token.")
            await self.fetch_token()

        if not headers:
            request_headers = dict()
        else:
            request_headers = headers.copy()

        request_headers["Authorization"] = f"Token {self._token}"

        log.debug("Adding token %s to request.", self._token)
        log.debug("Requesting url %s using method %s.", url, method)
        log.debug("Supplying headers %s and data %s", request_headers, data)
        log.debug("Passing through key word arguments %s.", kwargs)

        response = await super(VictorAsyncClient, self).request(
            method, url, headers=request_headers, data=data, **kwargs
        )

        if retry_unauthorized and response.status_code == codes.UNAUTHORIZED:
            log.info("Unauthorized response code. Fetch token and retry.")
            await self.fetch_token()
            response = await self._request(
                False, method, url, data=data, headers=headers, **kwargs
            )

        return response


@dataclass
class Activity:
    """Activity data class."""

    id: int
    url: str
    trap: str
    trap_name: str
    time_stamp: datetime
    time_stamp_unix: datetime
    sequence_number: int
    activity_type: int
    activity_type_text: str
    kills_present: int
    total_kills_reported: int
    battery_level: int
    wireless_network_rssi: int
    firmware_version_string: str
    temperature: int
    board_type: str
    error_code: int
    active: bool
    isRatKill: bool
    sexKillDetail: Optional[Any]
    ageKillDetail: Optional[Any]
    speciesKillDetail: Optional[Any]
    replacedAttractant: bool
    replacedBattery: bool
    cleanedTrap: bool
    note: Optional[Any]
    site_id: Optional[Any]
    building_id: Optional[Any]
    floor_id: Optional[Any]
    floor_plan_x: Optional[Any]
    floor_plan_y: Optional[Any]
    trap_type_text: str


@dataclass
class MobileApp:
    """Mobile app data class."""

    url: str
    min_android_version: int
    ideal_android_version: int
    min_ios_version: str
    ideal_ios_version: str
    commercial_min_android_version: int
    commercial_ideal_android_version: int
    commercial_min_ios_version: str
    commercial_ideal_ios_version: str


@dataclass
class Profile:
    """Profile data class."""

    id: int
    url: str
    user: str
    name: Optional[str]
    operator: str
    operator_name: str
    client: Optional[str]
    client_name: Optional[str]
    telephone_number: str
    phoneNames: Optional[Any]
    phoneNumbers: Optional[Any]
    emailAddresses: Optional[Any]
    email_notifications_enabled: bool
    notifications_enabled: bool
    terms_version: int
    notify_wifi_connection: bool
    notify_low_battery: bool
    notify_kill_alerts: bool
    notify_new_products: bool
    text_notifications_enabled: bool
    notify_empty_trap: bool
    fcmTokens: Optional[Any]
    apnsTokens: Optional[Any]
    fcmARNs: Optional[Any]
    apnsARNs: Optional[Any]
    fcmTokensPro: Optional[Any]
    apnsTokensPro: Optional[Any]
    fcmARNsPro: Optional[Any]
    apnsARNsPro: Optional[Any]
    favorite_sites: Optional[Any]
    notify_false_trigger: bool


@dataclass
class User:
    """User data class."""

    id: int
    url: str
    username: str
    password: str
    email: str
    groups: List[str]
    group_names: List[str]
    date_joined: datetime
    last_login: datetime
    first_name: str
    last_name: str
    profile: Profile


@dataclass
class TermsAndConditions:
    """Terms- and condtions data class."""

    id: int
    operator_id: int
    time_stamp: datetime
    terms_and_conditions: str
    terms_version: str


@dataclass
class Operator:
    """Operator data class."""

    id: int
    url: str
    account_number: str
    name: str
    address: str
    type: int
    number_sites: int
    number_buildings: int
    number_traps: int
    terms_version: int
    terms: str
    contact: User
    terms_and_conditions: Optional[List[TermsAndConditions]]


@dataclass
class TrapStatistics:
    """Trap statistics data class."""

    id: int
    url: str
    trap: str
    trap_name: str
    kills_present: int
    install_date: datetime
    owner_name: str
    owner_email: str
    last_report_date: datetime
    last_kill_date: Optional[datetime]
    temperature: int
    battery_level: int
    total_kills: Optional[int]
    total_escapes: Optional[int]
    rx_power_level: int
    firmware_version: str
    trap_provisioned: bool
    last_sequence_number: Optional[int]
    total_retreats: Optional[int]
    wireless_network_rssi: int
    error_code: int
    send_conn_lost_nt: bool
    send_empty_trap_nt: bool
    board_type: str
    last_maintenance_date: Union[str, datetime]


@dataclass
class Trap:
    """Trap data class."""

    id: int
    url: str
    corruption_status: int
    corruption_status_options: Optional[List[Tuple[int, str]]]
    operator: Optional[str]
    operator_name: Optional[str]
    name: str
    ssid: str
    serial_number: str
    auto_upgrade: bool
    status: int
    location: str
    lat: str
    long: str
    upgrade_firmware: Optional[str]
    commercial_gateway: Optional[str]
    commercial_monitor_mode_enabled: bool
    lorawan_app_key: str
    site_name: Optional[str]
    floor_plan_x: int
    floor_plan_y: int
    building_name: Optional[str]
    floor_name: Optional[str]
    room: Optional[str]
    room_name: Optional[str]
    trap_type: int
    trap_type_verbose: str
    alerts: int
    trapstatistics: TrapStatistics

    @property
    def corruption_status_verbose(self) -> Optional[str]:
        """Get description of corruption_status code."""
        if self.corruption_status_options:
            return next(
                item[1]
                for item in self.corruption_status_options
                if item[0] == self.corruption_status
            )
        return None


ActivitySchema = marshmallow_dataclass.class_schema(Activity)
MobileAppsSchema = marshmallow_dataclass.class_schema(MobileApp)
OperatorSchema = marshmallow_dataclass.class_schema(Operator)
ProfileSchema = marshmallow_dataclass.class_schema(Profile)
TermsAndConditionsSchema = marshmallow_dataclass.class_schema(TermsAndConditions)
TrapSchema = marshmallow_dataclass.class_schema(Trap)
TrapStatisticsSchema = marshmallow_dataclass.class_schema(TrapStatistics)
UserSchema = marshmallow_dataclass.class_schema(User)


class VictorApi:
    """Access Victor remote API."""

    def __init__(self, victor_client: VictorAsyncClient, unknown: str = None) -> None:
        """Initialize VictorApi."""
        if not victor_client:
            raise ValueError("Victor client is required.")
        self._client = victor_client
        self._unknown = RAISE if unknown is None else unknown

    async def _get_json_list(self, url: str) -> List[Dict[str, Any]]:
        response = await self._client.get(url)
        response.raise_for_status()
        json = response.json()

        if isinstance(json, list):
            return json

        result = json.get("results")
        if result:
            return result

        raise Exception("Unexpected response content")

    async def _get_list_by_schema(self, schema: Schema, url: str) -> List[Any]:
        return schema.load(
            await self._get_json_list(url), unknown=self._unknown, many=True
        )

    async def _get_json(self, url: str) -> Dict[str, Any]:
        response = await self._client.get(url)
        response.raise_for_status()
        return response.json()

    async def _get_by_schema(self, schema: Schema, url: str) -> Any:
        return schema.load(await self._get_json(url), unknown=self._unknown)

    async def get_activity_logs(self) -> List[Activity]:
        """Get activity logs."""
        return await self._get_list_by_schema(ActivitySchema(), "activitylogs/")

    async def get_activity_log_record(self, log_record_id: int) -> Activity:
        """Get activity log record by record id."""
        return await self._get_by_schema(
            ActivitySchema(), f"activitylogs/{log_record_id}/"
        )

    async def get_mobile_apps(self) -> List[MobileApp]:
        """Get mobile apps."""
        return await self._get_list_by_schema(MobileAppsSchema(), "mobileapps/")

    async def get_mobile_app_by_id(self, app_id: int) -> MobileApp:
        """Get mobile app by app id."""
        return await self.get_mobile_app_by_url(f"mobileapps/{app_id}/")

    async def get_mobile_app_by_url(self, url: str) -> MobileApp:
        """Get mobile app by url."""
        return await self._get_by_schema(MobileAppsSchema(), url)

    async def get_operators(self) -> List[Operator]:
        """Get operators."""
        return await self._get_list_by_schema(OperatorSchema(), "operators/")

    async def get_operator_by_id(self, operator_id: int) -> Operator:
        """Get operator by operator id."""
        return await self.get_operator_by_url(f"operators/{operator_id}/")

    async def get_operator_by_url(self, url: str) -> Operator:
        """Get operator by url."""
        return await self._get_by_schema(OperatorSchema(), url)

    async def get_profiles(self) -> List[Profile]:
        """Get profiles."""
        return await self._get_list_by_schema(ProfileSchema(), "profiles/")

    async def get_profile_by_id(self, profile_id: int) -> Profile:
        """Get profile by profile id."""
        return await self.get_profile_by_url(f"profiles/{profile_id}/")

    async def get_profile_by_url(self, url: str) -> Profile:
        """Get profile by url."""
        return await self._get_by_schema(ProfileSchema(), url)

    async def get_traps(self) -> List[Trap]:
        """Get traps."""
        return await self._get_list_by_schema(TrapSchema(), "traps/")

    async def get_trap_by_id(self, trap_id: int) -> Trap:
        """Get trap by trap id."""
        return await self.get_trap_by_url(f"traps/{trap_id}/")

    async def get_trap_by_url(self, url: str) -> Trap:
        """Get trap by url."""
        return await self._get_by_schema(TrapSchema(), url)

    async def get_trap_history(self, trap_id: int) -> List[Activity]:
        """Get trap history by trap id."""
        return await self._get_list_by_schema(
            ActivitySchema(), f"traps/{trap_id}/history/"
        )

    async def get_users(self) -> List[User]:
        """Get users."""
        return await self._get_list_by_schema(UserSchema(), "users/")

    async def get_user_by_id(self, user_id: int) -> User:
        """Get user by user id."""
        return await self.get_user_by_url(f"users/{user_id}/")

    async def get_user_by_url(self, url: str) -> User:
        """Get user by user id."""
        return await self._get_by_schema(UserSchema(), url)
