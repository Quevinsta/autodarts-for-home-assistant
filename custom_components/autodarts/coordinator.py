import asyncio
import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class AutodartsCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass: HomeAssistant, host: str, port: int):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),  # fallback, WS is realtime
        )

        self.host = host
        self.port = port

        self.data = {
            "online": False,
        }

        self._ws = None
        self._ws_started = False

    async def _async_update_data(self) -> dict:
        """
        Called by HA to check availability.
        We NEVER block here.
        """
        return self.data

    async def start_websocket(self):
        """Start WebSocket AFTER HA setup is complete"""
        if self._ws_started:
            return

        self._ws_started = True

        # ⚠️ Lazy import to prevent circular import
        from .ws_direct import AutodartsWebSocket

        self._ws = AutodartsWebSocket(
            self.host,
            self.port,
            self._handle_ws_event,
        )

        await self._ws.start()
        _LOGGER.info("Autodarts WebSocket started")

    async def _handle_ws_event(self, payload: dict):
        """
        Handle incoming WS events from Autodarts
        """
        # Mark online as soon as we get data
        self.data["online"] = True

        # Merge payload into coordinator data
        self.data.update(payload)

        # Push update to HA immediately
        self.async_set_updated_data(self.data)

    async def stop(self):
        if self._ws:
            await self._ws.stop()

