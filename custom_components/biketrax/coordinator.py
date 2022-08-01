"""BikeTrax coordinator."""
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .aiobiketrax import Device


class BikeTraxDataUpdateCoordinator(DataUpdateCoordinator):
    """Define a class to manage BikeTrax data updates."""

    def __init__(self, hass, logger, *, client, name, update_interval):
        """Initialize."""
        self._logger = logger
        self._name = name
        self._update_interval = update_interval
        self.client = client
        super().__init__(
            hass,
            logger,
            name=name,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict[str, Device]:
        """Update data via library."""
        self._logger.debug("Updating data")
        await self.client.update_devices()
        devices: dict[str, Device] = {d.bike_id: d for d in self.client.devices}
        for bt_id, bt in devices.items():
            self._logger.debug("Updating device (%s)", bt_id)
            try:
                await bt.update_position()
            except Exception as err:
                raise UpdateFailed(f"Error while updating position: {err}") from err
            try:
                await bt.update_trip()
            except Exception as err:
                raise UpdateFailed(f"Error while updating trip: {err}") from err
            try:
                await bt.update_subscription()
            except Exception as err:
                raise UpdateFailed(f"Error while updating subscription: {err}") from err
            self._logger.debug("device guard state: %s", bt.is_guarded)
        return devices
