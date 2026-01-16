from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


SENSORS = {
    "throw_summary": "Throw Summary",
    "turn_total": "Turn Total",
    "remaining": "Remaining",
}


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            AutodartsSensor(coordinator, entry, key, name)
            for key, name in SENSORS.items()
        ]
    )


class AutodartsSensor(CoordinatorEntity, SensorEntity):
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
    def native_value(self):
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get(self._key)

