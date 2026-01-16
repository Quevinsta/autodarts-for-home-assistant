from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import AutodartsCoordinator


BINARY_SENSORS: dict[str, dict[str, Any]] = {
    "checkout_possible": {"name": "Checkout Possible"},
    "is_180": {"name": "180"},
    "autodarts_online": {"name": "Autodarts Status"},
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
) -> None:
    coordinator: AutodartsCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        AutodartsBinarySensor(coordinator, entry, key, description)
        for key, description in BINARY_SENSORS.items()
    )


class AutodartsBinarySensor(
    CoordinatorEntity[AutodartsCoordinator], BinarySensorEntity
):
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

        # 🔥 Device info (zoals jij wilde)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Autodarts for Home Assistant",
            manufacturer="Quevinsta",
            model="X01",
        )

    @property
    def is_on(self):
        if not self.coordinator.data:
            return None
        return bool(self.coordinator.data.get(self._key))

