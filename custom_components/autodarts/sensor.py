from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import AutodartsCoordinator


SENSORS: dict[str, dict[str, Any]] = {
    "dart1": {"name": "Dart 1"},
    "dart2": {"name": "Dart 2"},
    "dart3": {"name": "Dart 3"},
    "dart1_value": {"name": "Dart 1 Value"},
    "dart2_value": {"name": "Dart 2 Value"},
    "dart3_value": {"name": "Dart 3 Value"},
    "turn_total": {"name": "Turn Total"},
    "remaining": {"name": "Points Remaining"},
    "leg_result": {"name": "Leg Result"},
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
) -> None:
    coordinator: AutodartsCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        AutodartsSensor(coordinator, entry, key, description)
        for key, description in SENSORS.items()
    ]

    async_add_entities(entities)


class AutodartsSensor(CoordinatorEntity[AutodartsCoordinator], SensorEntity):
    def __init__(
        self,
        coordinator: AutodartsCoordinator,
        entry: ConfigEntry,
        key: str,
        description: dict[str, Any],
    ) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_name = description["name"]
        self._attr_unique_id = f"{entry.entry_id}_{key}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Autodarts for Home Assistant",
            manufacturer="Quevinsta",
            model="X01",
        )

    @property
    def native_value(self):
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get(self._key)

