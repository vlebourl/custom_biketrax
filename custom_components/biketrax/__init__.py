"""The BikeTrax component."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers import device_registry as dr

from .aiobiketrax import Account
from .aiobiketrax.client import Device as BikeTrax
from .const import DOMAIN, LOGGER
from .coordinator import BikeTraxDataUpdateCoordinator

PLATFORMS = [Platform.DEVICE_TRACKER]

DEFAULT_UPDATE_INTERVAL = timedelta(minutes=1)


@dataclass
class BikeTraxData:
    """Define an object to be stored in `hass.data`."""

    coordinator: BikeTraxDataUpdateCoordinator
    devices: dict[str, BikeTrax]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up BikeTrax as config entry."""

    websession = aiohttp_client.async_get_clientsession(hass)

    try:
        client = Account(
            entry.data[CONF_USERNAME],
            entry.data[CONF_PASSWORD],
            session=websession,
        )
    except Exception as err:
        raise ConfigEntryAuthFailed("Failed to authenticate") from err

    coordinator = BikeTraxDataUpdateCoordinator(
        hass,
        LOGGER,
        client=client,
        name="biketrax coordinator",
        update_interval=DEFAULT_UPDATE_INTERVAL,
    )
    await coordinator.async_config_entry_first_refresh()
    devices = {device.bike_id: device for device in coordinator.data.values()}

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = BikeTraxData(
        coordinator=coordinator, devices=devices
    )

    await hass.config_entries.async_forward_entry_setup(entry, PLATFORMS[0])

    device_registry = await dr.async_get_registry(hass)
    for device_id, device in devices.items():
        LOGGER.debug("Add device (%s)", device_id)

        device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, device_id)},
            model=device.model,
            manufacturer="PowUnity BikeTrax",
            name=device.name,
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Tile config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
