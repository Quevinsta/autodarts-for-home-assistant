from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_HOST, CONF_PORT, DEFAULT_PORT
from .coordinator import AutodartsCoordinator

PLATFORMS = ["sensor", "binary_sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = AutodartsCoordinator(
        hass=hass,
        host=entry.data[CONF_HOST],
        port=entry.data.get(CONF_PORT, DEFAULT_PORT),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # 1️⃣ Eerst platforms laden (entities bestaan nu)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # 2️⃣ PAS DAARNA WebSocket starten (🔥 belangrijk)
    hass.async_create_task(coordinator.start_websocket())

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = hass.data[DOMAIN].pop(entry.entry_id)

    await coordinator.stop()

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

