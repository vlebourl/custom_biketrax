"""Models for the Biketrax API."""

import contextlib
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, List, Optional, Type, TypeVar, cast

import dateutil.parser

T = TypeVar("T")


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    """Retrieve from a list."""
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    """Retrieve from a str."""
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    """Retrieve from a bool."""
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    """Retrieve from a int."""
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    """Retrieve from a datetime."""
    return dateutil.parser.parse(x)


def from_none(x: Any) -> Any:
    """Retrieve from a None."""
    assert x is None
    return x


def from_union(fs, x):
    """Return the first type that matches."""
    for f in fs:
        with contextlib.suppress(Exception):
            return f(x)
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    """Convert a class instance to a dictionary."""
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_float(x: Any) -> float:
    """Retrieve from a float."""
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    """Convert a value to a float."""
    assert isinstance(x, float)
    return x


@dataclass
class Passport:
    """Passport."""

    bike_pictures: List[str]
    bike_type: str
    colour: str
    engine: str
    frame_number: str
    insurance: bool
    manufacturer: str
    model: str
    price: int
    receipt_pictures: List[str]

    @staticmethod
    def from_dict(obj: Any) -> "Passport":
        """Build a class instance from a dictionary."""
        assert isinstance(obj, dict)
        bike_pictures = from_list(from_str, obj.get("bikePictures"))
        bike_type = from_str(obj.get("bikeType", "Unknown"))
        colour = from_str(obj.get("colour", "Unknown"))
        engine = from_str(obj.get("engine", "Unknown"))
        frame_number = from_str(obj.get("frameNumber", "Unknown"))
        insurance = from_bool(obj.get("insurance", False))
        manufacturer = from_str(obj.get("manufacturer", "Unknown"))
        model = from_str(obj.get("model", "Unknown"))
        price = int(from_str(obj.get("price", "Unknown")))
        receipt_pictures = from_list(from_str, obj.get("receiptPictures", "Unknown"))
        return Passport(
            bike_pictures,
            bike_type,
            colour,
            engine,
            frame_number,
            insurance,
            manufacturer,
            model,
            price,
            receipt_pictures,
        )

    def to_dict(self) -> dict:
        """Convert a class instance to a dictionary."""
        result: dict = {"bikePictures": from_list(from_str, self.bike_pictures)}
        result["bikeType"] = from_str(self.bike_type)
        result["colour"] = from_str(self.colour)
        result["engine"] = from_str(self.engine)
        result["frameNumber"] = from_str(self.frame_number)
        result["insurance"] = from_bool(self.insurance)
        result["manufacturer"] = from_str(self.manufacturer)
        result["model"] = from_str(self.model)
        result["price"] = from_str(str(self.price))
        result["receiptPictures"] = from_list(from_str, self.receipt_pictures)
        return result


@dataclass
class DeviceAttributes:
    """Device attributes."""

    alarm: bool
    auto_guard: bool
    geofence_radius: int
    guarded: bool
    guard_type: str
    last_alarm: int
    passport: Passport
    trial_end: datetime
    stolen: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> "DeviceAttributes":
        """Build a class instance from a dictionary."""
        assert isinstance(obj, dict)
        alarm = from_bool(obj.get("alarm"))
        auto_guard = from_bool(obj.get("autoGuard"))
        geofence_radius = from_int(obj.get("geofenceRadius"))
        guarded = from_bool(obj.get("guarded"))
        guard_type = from_str(obj.get("guardType"))
        last_alarm = from_int(obj.get("lastAlarm"))
        passport = Passport.from_dict(obj.get("passport"))
        trial_end = from_datetime(obj.get("trialEnd"))
        stolen = from_union([from_bool, from_none], obj.get("stolen"))
        return DeviceAttributes(
            alarm,
            auto_guard,
            geofence_radius,
            guarded,
            guard_type,
            last_alarm,
            passport,
            trial_end,
            stolen,
        )

    def to_dict(self) -> dict:
        """Convert a class instance to a dictionary."""
        result: dict = {"alarm": from_bool(self.alarm)}
        result["autoGuard"] = from_bool(self.auto_guard)
        result["geofenceRadius"] = from_int(self.geofence_radius)
        result["guarded"] = from_bool(self.guarded)
        result["guardType"] = from_str(self.guard_type)
        result["lastAlarm"] = from_int(self.last_alarm)
        result["passport"] = to_class(Passport, self.passport)
        result["trialEnd"] = self.trial_end.isoformat()
        result["stolen"] = from_union([from_bool, from_none], self.stolen)
        return result


@dataclass
class Device:
    """Device."""

    attributes: DeviceAttributes
    category: None
    contact: None
    disabled: bool
    geofence_ids: List[Any]
    group_id: int
    bike_id: int
    last_update: datetime
    model: None
    name: str
    phone: None
    position_id: int
    status: str
    unique_id: str

    @staticmethod
    def from_dict(obj: Any) -> "Device":
        """Build a class instance from a dictionary."""
        assert isinstance(obj, dict)
        attributes = DeviceAttributes.from_dict(obj.get("attributes"))
        category = from_str(obj.get("category", "Unknown"))
        contact = from_str(obj.get("contact", "Unknown"))
        disabled = from_bool(obj.get("disabled", False))
        geofence_ids = from_list(lambda x: x, obj.get("geofenceIds"))
        group_id = from_int(obj.get("groupId"))
        bike_id = from_int(obj.get("id"))
        last_update = from_datetime(obj.get("lastUpdate"))
        model = from_str(obj.get("model", "Unknown"))
        name = from_str(obj.get("name", "Unknown"))
        phone = from_str(obj.get("phone", "Unknown"))
        position_id = from_int(obj.get("positionId"))
        status = from_str(obj.get("status", "Unknown"))
        unique_id = from_str(obj.get("uniqueId", "Unknown"))
        return Device(
            attributes,
            category,
            contact,
            disabled,
            geofence_ids,
            group_id,
            bike_id,
            last_update,
            model,
            name,
            phone,
            position_id,
            status,
            unique_id,
        )

    def to_dict(self) -> dict:
        """Convert a class instance to a dictionary."""
        result: dict = {"attributes": to_class(DeviceAttributes, self.attributes)}
        result["category"] = from_str(self.category)
        result["contact"] = from_str(self.contact)
        result["disabled"] = from_bool(self.disabled)
        result["geofenceIds"] = from_list(lambda x: x, self.geofence_ids)
        result["groupId"] = from_int(self.group_id)
        result["bike_id"] = from_int(self.bike_id)
        result["lastUpdate"] = self.last_update.isoformat()
        result["model"] = from_str(self.model)
        result["name"] = from_str(self.name)
        result["phone"] = from_str(self.phone)
        result["positionId"] = from_int(self.position_id)
        result["status"] = from_str(self.status)
        result["uniqueId"] = from_str(self.unique_id)
        return result


@dataclass
class PositionAttributes:
    """Position attributes."""

    battery_level: int
    charge: bool
    distance: float
    hours: int
    ignition: bool
    motion: bool
    status: int
    total_distance: float
    alarm: Optional[str] = None
    armed: Optional[bool] = None
    index: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "PositionAttributes":
        """Build a class instance from a dictionary."""
        assert isinstance(obj, dict)
        battery_level = from_int(obj.get("batteryLevel"))
        charge = from_bool(obj.get("charge"))
        distance = from_float(obj.get("distance"))
        hours = from_int(obj.get("hours"))
        ignition = from_bool(obj.get("ignition"))
        motion = from_bool(obj.get("motion"))
        status = from_int(obj.get("status"))
        total_distance = from_float(obj.get("totalDistance"))
        alarm = from_union([from_str, from_none], obj.get("alarm"))
        armed = from_union([from_bool, from_none], obj.get("armed"))
        index = from_union([from_int, from_none], obj.get("index"))
        return PositionAttributes(
            battery_level,
            charge,
            distance,
            hours,
            ignition,
            motion,
            status,
            total_distance,
            alarm,
            armed,
            index,
        )

    def to_dict(self) -> dict:
        """Convert a class instance to a dictionary."""
        result: dict = {"batteryLevel": from_int(self.battery_level)}
        result["charge"] = from_bool(self.charge)
        result["distance"] = to_float(self.distance)
        result["hours"] = from_int(self.hours)
        result["ignition"] = from_bool(self.ignition)
        result["motion"] = from_bool(self.motion)
        result["status"] = from_int(self.status)
        result["totalDistance"] = to_float(self.total_distance)
        result["alarm"] = from_union([from_str, from_none], self.alarm)
        result["armed"] = from_union([from_bool, from_none], self.armed)
        result["index"] = from_union([from_int, from_none], self.index)
        return result


@dataclass
class Position:
    """Position."""

    accuracy: float
    address: None
    altitude: float
    attributes: PositionAttributes
    course: float
    device_id: int
    device_time: datetime
    fix_time: datetime
    bike_id: int
    latitude: float
    longitude: float
    network: None
    outdated: bool
    protocol: str
    server_time: datetime
    speed: float
    type: None
    valid: bool

    @staticmethod
    def from_dict(obj: Any) -> "Position":
        """Build a class instance from a dictionary."""
        assert isinstance(obj, dict)
        accuracy = from_float(obj.get("accuracy"))
        address = from_none(obj.get("address"))
        altitude = from_float(obj.get("altitude"))
        attributes = PositionAttributes.from_dict(obj.get("attributes"))
        course = from_float(obj.get("course"))
        device_id = from_int(obj.get("deviceId"))
        device_time = from_datetime(obj.get("deviceTime"))
        fix_time = from_datetime(obj.get("fixTime"))
        bike_id = from_int(obj.get("id"))
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        network = from_none(obj.get("network"))
        outdated = from_bool(obj.get("outdated"))
        protocol = from_str(obj.get("protocol"))
        server_time = from_datetime(obj.get("serverTime"))
        speed = from_float(obj.get("speed"))
        bike_type = from_none(obj.get("type"))
        valid = from_bool(obj.get("valid"))
        return Position(
            accuracy,
            address,
            altitude,
            attributes,
            course,
            device_id,
            device_time,
            fix_time,
            bike_id,
            latitude,
            longitude,
            network,
            outdated,
            protocol,
            server_time,
            speed,
            bike_type,
            valid,
        )

    def to_dict(self) -> dict:
        """Convert a class instance to a dictionary."""
        result: dict = {"accuracy": to_float(self.accuracy)}
        result["address"] = from_none(self.address)
        result["altitude"] = to_float(self.altitude)
        result["attributes"] = to_class(PositionAttributes, self.attributes)
        result["course"] = to_float(self.course)
        result["deviceId"] = from_int(self.device_id)
        result["deviceTime"] = self.device_time.isoformat()
        result["fixTime"] = self.fix_time.isoformat()
        result["bike_id"] = from_int(self.bike_id)
        result["latitude"] = to_float(self.latitude)
        result["longitude"] = to_float(self.longitude)
        result["network"] = from_none(self.network)
        result["outdated"] = from_bool(self.outdated)
        result["protocol"] = from_str(self.protocol)
        result["serverTime"] = self.server_time.isoformat()
        result["speed"] = to_float(self.speed)
        result["type"] = from_none(self.bike_type)
        result["valid"] = from_bool(self.valid)
        return result


@dataclass
class SessionAttributes:
    """Session attributes."""

    app_environment: str
    app_package: str
    app_version: str
    fcm_tokens: List[str]
    locale: str
    send_analytics: bool

    @staticmethod
    def from_dict(obj: Any) -> "SessionAttributes":
        """Build a class instance from a dictionary."""
        assert isinstance(obj, dict)
        app_environment = from_str(obj.get("appEnvironment"))
        app_package = from_str(obj.get("appPackage"))
        app_version = from_str(obj.get("appVersion"))
        fcm_tokens = from_list(from_str, obj.get("fcmTokens"))
        locale = from_str(obj.get("locale"))
        send_analytics = from_bool(obj.get("sendAnalytics"))
        return SessionAttributes(
            app_environment,
            app_package,
            app_version,
            fcm_tokens,
            locale,
            send_analytics,
        )

    def to_dict(self) -> dict:
        """Convert a class instance to a dictionary."""
        result: dict = {"appEnvironment": from_str(self.app_environment)}
        result["appPackage"] = from_str(self.app_package)
        result["appVersion"] = from_str(self.app_version)
        result["fcmTokens"] = from_list(from_str, self.fcm_tokens)
        result["locale"] = from_str(self.locale)
        result["sendAnalytics"] = from_bool(self.send_analytics)
        return result


@dataclass
class Session:
    """Session."""

    administrator: bool
    attributes: SessionAttributes
    coordinate_format: None
    device_limit: int
    device_readonly: bool
    disabled: bool
    email: str
    expiration_time: None
    bike_id: int
    latitude: float
    limit_commands: bool
    login: None
    longitude: float
    bike_map: None
    name: str
    password: None
    phone: None
    poi_layer: None
    readonly: bool
    token: str
    twelve_hour_format: bool
    user_limit: int
    zoom: int

    @staticmethod
    def from_dict(obj: Any) -> "Session":
        """Build a class instance from a dictionary."""
        assert isinstance(obj, dict)
        administrator = from_bool(obj.get("administrator"))
        attributes = SessionAttributes.from_dict(obj.get("attributes"))
        coordinate_format = from_none(obj.get("coordinateFormat"))
        device_limit = from_int(obj.get("deviceLimit"))
        device_readonly = from_bool(obj.get("deviceReadonly"))
        disabled = from_bool(obj.get("disabled"))
        email = from_str(obj.get("email"))
        expiration_time = from_none(obj.get("expirationTime"))
        bike_id = from_int(obj.get("id"))
        latitude = from_float(obj.get("latitude"))
        limit_commands = from_bool(obj.get("limitCommands"))
        login = from_none(obj.get("login"))
        longitude = from_float(obj.get("longitude"))
        bike_map = from_none(obj.get("map"))
        name = from_str(obj.get("name"))
        password = from_none(obj.get("password"))
        phone = from_none(obj.get("phone"))
        poi_layer = from_none(obj.get("poiLayer"))
        readonly = from_bool(obj.get("readonly"))
        token = from_str(obj.get("token"))
        twelve_hour_format = from_bool(obj.get("twelveHourFormat"))
        user_limit = from_int(obj.get("userLimit"))
        zoom = from_int(obj.get("zoom"))
        return Session(
            administrator,
            attributes,
            coordinate_format,
            device_limit,
            device_readonly,
            disabled,
            email,
            expiration_time,
            bike_id,
            latitude,
            limit_commands,
            login,
            longitude,
            bike_map,
            name,
            password,
            phone,
            poi_layer,
            readonly,
            token,
            twelve_hour_format,
            user_limit,
            zoom,
        )

    def to_dict(self) -> dict:
        """Convert a class instance to a dictionary."""
        result: dict = {"administrator": from_bool(self.administrator)}
        result["attributes"] = to_class(SessionAttributes, self.attributes)
        result["coordinateFormat"] = from_none(self.coordinate_format)
        result["deviceLimit"] = from_int(self.device_limit)
        result["deviceReadonly"] = from_bool(self.device_readonly)
        result["disabled"] = from_bool(self.disabled)
        result["email"] = from_str(self.email)
        result["expirationTime"] = from_none(self.expiration_time)
        result["bike_id"] = from_int(self.bike_id)
        result["latitude"] = to_float(self.latitude)
        result["limitCommands"] = from_bool(self.limit_commands)
        result["login"] = from_none(self.login)
        result["longitude"] = to_float(self.longitude)
        result["map"] = from_none(self.bike_map)
        result["name"] = from_str(self.name)
        result["password"] = from_none(self.password)
        result["phone"] = from_none(self.phone)
        result["poiLayer"] = from_none(self.poi_layer)
        result["readonly"] = from_bool(self.readonly)
        result["token"] = from_str(self.token)
        result["twelveHourFormat"] = from_bool(self.twelve_hour_format)
        result["userLimit"] = from_int(self.user_limit)
        result["zoom"] = from_int(self.zoom)
        return result


@dataclass
class Subscription:
    """Subscription."""

    category: str
    created_at: datetime
    bike_id: int
    setup_fee: None
    subscription_id: None
    trial_duration: int
    trial_end: datetime
    unique_id: str
    updated_at: datetime

    @staticmethod
    def from_dict(obj: Any) -> "Subscription":
        """Build a class instance from a dictionary."""
        assert isinstance(obj, dict)
        category = from_str(obj.get("category"))
        created_at = from_datetime(obj.get("createdAt"))
        bike_id = from_int(obj.get("id"))
        setup_fee = from_none(obj.get("setupFee"))
        subscription_id = from_str(obj.get("subscriptionId", "Unknown"))
        trial_duration = from_int(obj.get("trialDuration"))
        trial_end = from_datetime(obj.get("trialEnd"))
        unique_id = from_str(obj.get("uniqueId"))
        updated_at = from_datetime(obj.get("updatedAt"))
        return Subscription(
            category,
            created_at,
            bike_id,
            setup_fee,
            subscription_id,
            trial_duration,
            trial_end,
            unique_id,
            updated_at,
        )

    def to_dict(self) -> dict:
        """Convert a class instance to a dictionary."""
        result: dict = {"category": from_str(self.category)}
        result["createdAt"] = self.created_at.isoformat()
        result["bike_id"] = from_int(self.bike_id)
        result["setupFee"] = from_none(self.setup_fee)
        result["subscriptionId"] = from_none(self.subscription_id)
        result["trialDuration"] = from_int(self.trial_duration)
        result["trialEnd"] = self.trial_end.isoformat()
        result["uniqueId"] = from_str(self.unique_id)
        result["updatedAt"] = self.updated_at.isoformat()
        return result


@dataclass
class Trip:
    """Trip."""

    average_speed: float
    device_id: int
    device_name: str
    distance: float
    driver_name: None
    driver_unique_id: None
    duration: int
    end_address: None
    end_lat: float
    end_lon: float
    end_odometer: float
    end_position_id: int
    end_time: datetime
    max_speed: float
    spent_fuel: float
    start_address: None
    start_lat: float
    start_lon: float
    start_odometer: float
    start_position_id: int
    start_time: datetime

    @staticmethod
    def from_dict(obj: Any) -> "Trip":
        """Build a class instance from a dictionary."""
        assert isinstance(obj, dict)
        average_speed = from_float(obj.get("averageSpeed"))
        device_id = from_int(obj.get("deviceId"))
        device_name = from_str(obj.get("deviceName"))
        distance = from_float(obj.get("distance"))
        driver_name = from_none(obj.get("driverName"))
        driver_unique_id = from_none(obj.get("driverUniqueId"))
        duration = from_int(obj.get("duration"))
        end_address = from_none(obj.get("endAddress"))
        end_lat = from_float(obj.get("endLat"))
        end_lon = from_float(obj.get("endLon"))
        end_odometer = from_float(obj.get("endOdometer"))
        end_position_id = from_int(obj.get("endPositionId"))
        end_time = from_datetime(obj.get("endTime"))
        max_speed = from_float(obj.get("maxSpeed"))
        spent_fuel = from_float(obj.get("spentFuel"))
        start_address = from_none(obj.get("startAddress"))
        start_lat = from_float(obj.get("startLat"))
        start_lon = from_float(obj.get("startLon"))
        start_odometer = from_float(obj.get("startOdometer"))
        start_position_id = from_int(obj.get("startPositionId"))
        start_time = from_datetime(obj.get("startTime"))
        return Trip(
            average_speed,
            device_id,
            device_name,
            distance,
            driver_name,
            driver_unique_id,
            duration,
            end_address,
            end_lat,
            end_lon,
            end_odometer,
            end_position_id,
            end_time,
            max_speed,
            spent_fuel,
            start_address,
            start_lat,
            start_lon,
            start_odometer,
            start_position_id,
            start_time,
        )

    def to_dict(self) -> dict:
        """Convert a class instance to a dictionary."""
        result: dict = {"averageSpeed": to_float(self.average_speed)}
        result["deviceId"] = from_int(self.device_id)
        result["deviceName"] = from_str(self.device_name)
        result["distance"] = to_float(self.distance)
        result["driverName"] = from_none(self.driver_name)
        result["driverUniqueId"] = from_none(self.driver_unique_id)
        result["duration"] = from_int(self.duration)
        result["endAddress"] = from_none(self.end_address)
        result["endLat"] = to_float(self.end_lat)
        result["endLon"] = to_float(self.end_lon)
        result["endOdometer"] = to_float(self.end_odometer)
        result["endPositionId"] = from_int(self.end_position_id)
        result["endTime"] = self.end_time.isoformat()
        result["maxSpeed"] = to_float(self.max_speed)
        result["spentFuel"] = to_float(self.spent_fuel)
        result["startAddress"] = from_none(self.start_address)
        result["startLat"] = to_float(self.start_lat)
        result["startLon"] = to_float(self.start_lon)
        result["startOdometer"] = to_float(self.start_odometer)
        result["startPositionId"] = from_int(self.start_position_id)
        result["startTime"] = self.start_time.isoformat()
        return result


def device_from_dict(s: Any) -> Device:
    """Build a class instance from a dictionary."""
    return Device.from_dict(s)


def device_to_dict(x: Device) -> Any:
    """Convert a class instance to a dictionary."""
    return to_class(Device, x)


def device_attributes_from_dict(s: Any) -> DeviceAttributes:
    """Build a class instance from a dictionary."""
    return DeviceAttributes.from_dict(s)


def device_attributes_to_dict(x: DeviceAttributes) -> Any:
    """Convert a class instance to a dictionary."""
    return to_class(DeviceAttributes, x)


def passport_from_dict(s: Any) -> Passport:
    """Build a class instance from a dictionary."""
    return Passport.from_dict(s)


def passport_to_dict(x: Passport) -> Any:
    """Convert a class instance to a dictionary."""
    return to_class(Passport, x)


def position_from_dict(s: Any) -> Position:
    """Build a class instance from a dictionary."""
    return Position.from_dict(s)


def position_to_dict(x: Position) -> Any:
    """Convert a class instance to a dictionary."""
    return to_class(Position, x)


def position_attributes_from_dict(s: Any) -> PositionAttributes:
    """Build a class instance from a dictionary."""
    return PositionAttributes.from_dict(s)


def position_attributes_to_dict(x: PositionAttributes) -> Any:
    """Convert a class instance to a dictionary."""
    return to_class(PositionAttributes, x)


def session_from_dict(s: Any) -> Session:
    """Build a class instance from a dictionary."""
    return Session.from_dict(s)


def session_to_dict(x: Session) -> Any:
    """Convert a class instance to a dictionary."""
    return to_class(Session, x)


def session_attributes_from_dict(s: Any) -> SessionAttributes:
    """Build a class instance from a dictionary."""
    return SessionAttributes.from_dict(s)


def session_attributes_to_dict(x: SessionAttributes) -> Any:
    """Convert a class instance to a dictionary."""
    return to_class(SessionAttributes, x)


def subscription_from_dict(s: Any) -> Subscription:
    """Build a class instance from a dictionary."""
    return Subscription.from_dict(s)


def subscription_to_dict(x: Subscription) -> Any:
    """Convert a class instance to a dictionary."""
    return to_class(Subscription, x)


def trip_from_dict(s: Any) -> Trip:
    """Build a class instance from a dictionary."""
    return Trip.from_dict(s)


def trip_to_dict(x: Trip) -> Any:
    """Convert a class instance to a dictionary."""
    return to_class(Trip, x)
