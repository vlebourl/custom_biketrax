"""The BikeTrax component."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from functools import partial

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util.async_ import gather_with_concurrency

from .aiobiketrax import Account
from .aiobiketrax.client import Device as BikeTrax
from .const import DOMAIN, LOGGER

PLATFORMS = [Platform.DEVICE_TRACKER]

DEFAULT_INIT_TASK_LIMIT = 2
DEFAULT_UPDATE_INTERVAL = timedelta(minutes=2)


@dataclass
class BikeTraxData:
    """Define an object to be stored in `hass.data`."""

    coordinators: dict[str, DataUpdateCoordinator]
    bikes: dict[str, BikeTrax]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up BikeTrax as config entry."""

    websession = aiohttp_client.async_get_clientsession(hass)

    try:
        client = await Account(
            entry.data[CONF_USERNAME],
            entry.data[CONF_PASSWORD],
            session=websession,
        )
        await client.update_devices()
        bikes = {bike.id: bike for bike in client.devices}
    except Exception as err:
        raise ConfigEntryAuthFailed("Failed to authenticate") from err

    async def async_update_bt(bt: BikeTrax) -> None:
        """Update the BikeTrax."""
        try:
            await bt.update_position()
            await bt.update_trip()
            await bt.update_subscription()
        except Exception as err:
            raise UpdateFailed(f"Error while retrieving data: {err}") from err

    coordinators = {}
    coordinator_init_tasks = []

    for bt_id, bt in bikes.items():
        coordinator = coordinators[bt_id] = DataUpdateCoordinator(
            hass,
            LOGGER,
            name=bt.name,
            update_interval=DEFAULT_UPDATE_INTERVAL,
            update_method=partial(async_update_bt, bt),
        )
        coordinator_init_tasks.append(coordinator.async_refresh())

    await gather_with_concurrency(DEFAULT_INIT_TASK_LIMIT, *coordinator_init_tasks)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = BikeTraxData(
        coordinators=coordinators, bikes=bikes
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Tile config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
