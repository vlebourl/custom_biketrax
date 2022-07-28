"""Support for BikeTrax device trackers."""
from __future__ import annotations

import logging

from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.components.device_tracker.const import SOURCE_TYPE_GPS
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from . import BikeTraxData
from .aiobiketrax.client import Device as BikeTrax
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

ATTR_IS_ALARM_TRIGGERED = "is_alarm_triggered"
ATTR_IS_TRACKING_ENABLED = "is_tracking_enabled"
ATTR_IS_STOLEN = "is_stolen"
ATTR_IS_GUARDED = "is_guarded"
ATTR_IS_AUTO_GUARDED = "is_auto_guarded"
ATTR_ACCURACY = "accuracy"
ATTR_SPEED = "speed"
ATTR_COURSE = "course"
ATTR_BATTERY_LEVEL = "battery_level"
ATTR_TOTAL_DISTANCE = "total_distance"
ATTR_SUBSCRIPTION_UNTIL = "subscription_until"
ATTR_LAST_UPDATED = "last_updated"
ATTR_STATUS = "status"
ATTR_TRIP = "trip"

DEFAULT_ICON = "mdi:bike"


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Tile device trackers."""
    data: BikeTraxData = hass.data[DOMAIN][entry.entry_id]

    _LOGGER.info("Found %d bikes", len(data.bikes))

    async_add_entities(
        [
            BikeTraxDeviceTracker(entry, data.coordinators[bt_id], bt)
            for bt_id, bt in data.bikes.items()
        ]
    )


class BikeTraxDeviceTracker(CoordinatorEntity, TrackerEntity):
    """Representation of a BikeTrax device tracker."""

    _attr_icon = DEFAULT_ICON

    def __init__(
        self, entry: ConfigEntry, coordinator: DataUpdateCoordinator, biketrax: BikeTrax
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)

        self._attr_extra_state_attributes = {}
        self._attr_name = biketrax.name
        self._attr_unique_id = f"{entry.data[CONF_USERNAME]}_{biketrax.bike_id}"
        self._entry = entry
        self._biketrax = biketrax
        self._attr_device_info = self.generate_device_info()

    def generate_device_info(self) -> DeviceInfo:
        """Return device registry information for this entity."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._biketrax.bike_id)},
            name=self._biketrax.name,
            manufacturer="PowUnity BikeTrax",
            model=self._biketrax.model,
        )

    @property
    def location_accuracy(self) -> int:
        """Return the location accuracy of the device.

        Value in meters.
        """
        return self._biketrax.accuracy

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        return self._biketrax.latitude

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        return self._biketrax.longitude

    @property
    def source_type(self) -> str:
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @callback
    def _handle_coordinator_update(self) -> None:
        """Respond to a DataUpdateCoordinator update."""
        self._update_from_latest_data()
        self.async_write_ha_state()

    @callback
    def _update_from_latest_data(self) -> None:
        """Update the entity from the latest data."""
        self._attr_extra_state_attributes.update(
            {
                ATTR_IS_ALARM_TRIGGERED: self._biketrax.is_alarm_triggered,
                ATTR_IS_TRACKING_ENABLED: self._biketrax.is_tracking_enabled,
                ATTR_IS_STOLEN: self._biketrax.is_stolen,
                ATTR_IS_GUARDED: self._biketrax.is_guarded,
                ATTR_IS_AUTO_GUARDED: self._biketrax.is_auto_guarded,
                ATTR_ACCURACY: self._biketrax.accuracy,
                ATTR_SPEED: self._biketrax.speed,
                ATTR_COURSE: self._biketrax.course,
                ATTR_BATTERY_LEVEL: self._biketrax.battery_level,
                ATTR_TOTAL_DISTANCE: self._biketrax.total_distance,
                ATTR_SUBSCRIPTION_UNTIL: self._biketrax.subscription_until,
                ATTR_LAST_UPDATED: self._biketrax.last_updated,
                ATTR_STATUS: self._biketrax.status,
                ATTR_TRIP: self._biketrax.trip,
            }
        )

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await super().async_added_to_hass()
        self._update_from_latest_data()
