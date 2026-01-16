from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


BINARY_SENSORS = {
    "checkout_possible": "Checkout Possible",
}


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            AutodartsBinarySensor(coordinator, entry, key, name)
            for key, name in BINARY_SENSORS.items()
        ]
    )


class AutodartsBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator, entry, key, name):
        super().__init__(coordinator)
        self._key = key

        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Autodarts for Home Assistant",
            manufacturer="Quevinsta",
            model="Autodarts",
        )

    @property
    def is_on(self):
        data = self.coordinator.data or {}
        return bool(data.get(self._key, False))

