from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

import aiohttp
import websocket

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import AUTODARTS_STATE_PATH, AUTODARTS_WS_PATH
from .autodarts_api import parse_x01_state

_LOGGER = logging.getLogger(__name__)


class AutodartsCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, host: str, port: int) -> None:
        self.hass = hass
        self.host = host
        self.port = port

        self._session = aiohttp.ClientSession()
        self._ws: websocket.WebSocketApp | None = None

        super().__init__(
            hass,
            _LOGGER,
            name="Autodarts",
            update_interval=10,  # 🔥 heartbeat elke 10 sec
        )

    async def async_start(self) -> None:
        await self._connect_websocket()
        await self.async_refresh()

    # ---------------- WEBSOCKET ----------------

    async def _connect_websocket(self) -> None:
        url = f"ws://{self.host}:{self.port}{AUTODARTS_WS_PATH}"
        _LOGGER.info("Connecting to Autodarts WebSocket: %s", url)

        def on_message(ws, message):
            try:
                data = json.loads(message)
                if data.get("type") == "motion_state":
                    asyncio.run_coroutine_threadsafe(
                        self.async_refresh(),
                        self.hass.loop,
                    )
            except Exception as err:
                _LOGGER.error("WebSocket error: %s", err)

        def on_close(ws):
            _LOGGER.warning("WebSocket closed")

        self._ws = websocket.WebSocketApp(
            url,
            on_message=on_message,
            on_close=on_close,
        )

        asyncio.get_event_loop().run_in_executor(None, self._ws.run_forever)

    # ---------------- DATA FETCH ----------------

    async def _async_update_data(self) -> dict[str, Any]:
        url = f"http://{self.host}:{self.port}{AUTODARTS_STATE_PATH}"

        try:
            async with self._session.get(url, timeout=2) as response:
                response.raise_for_status()
                raw_state = await response.json()

                data = parse_x01_state(raw_state)
                data["autodarts_online"] = "online"
                return data

        except Exception as err:
            _LOGGER.error("Autodarts offline: %s", err)

            return {
                "autodarts_online": "offline",
            }

    async def async_close(self) -> None:
        if self._ws:
            self._ws.close()
        await self._session.close()

