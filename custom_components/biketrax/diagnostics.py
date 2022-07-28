"""Diagnostics support for Tile."""
from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant

from . import BikeTraxData
from .const import DOMAIN

CONF_ALTITUDE = "altitude"
CONF_ID = "id"

TO_REDACT = {
    CONF_ALTITUDE,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_ID,
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data: BikeTraxData = hass.data[DOMAIN][entry.entry_id]

    return async_redact_data(
        {"bikes": [bt.as_dict() for bt in data.bikes.values()]}, TO_REDACT
    )
