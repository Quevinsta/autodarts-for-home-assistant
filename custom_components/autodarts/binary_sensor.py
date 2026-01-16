from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


BINARY_SENSORS = {
    "autodarts_online": {
        "name": "Autodarts Status",
        "device_class": BinarySensorDeviceClass.CONNECTIVITY,
    },
}


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            AutodartsBinarySensor(
                coordinator,
                entry,
                key,
                meta["name"],
                meta["device_class"],
            )
            for key, meta in BINARY_SENSORS.items()
        ]
    )


class AutodartsBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator, entry, key, name, device_class):
        super().__init__(coordinator)
        self._key = key

        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_device_class = device_class

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Autodarts for Home Assistant",
            manufacturer="Quevinsta",
            model="Autodarts",
        )

    @property
    def is_on(self):
        if not self.coordinator.data:
            return False
        return bool(self.coordinator.data.get(self._key))

