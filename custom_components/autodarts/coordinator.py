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

        # 🔥 expliciete status
        self._online: bool = False

        super().__init__(
            hass,
            _LOGGER,
            name="Autodarts",
            update_interval=None,  # push-based
        )

    # ==================================================
    # STARTUP
    # ==================================================

    async def async_start(self) -> None:
        # Eerste fetch → status direct correct
        await self.async_refresh()
        await self._connect_websocket()

    # ==================================================
    # WEBSOCKET
    # ==================================================

    async def _connect_websocket(self) -> None:
        url = f"ws://{self.host}:{self.port}{AUTODARTS_WS_PATH}"
        _LOGGER.info("Connecting to Autodarts WebSocket: %s", url)

        def on_message(ws, message):
            try:
                data = json.loads(message)
                if data.get("type") == "motion_state":
                    asyncio.run_coroutine_threadsafe(
                        self._handle_motion_event(),
                        self.hass.loop,
                    )
            except Exception as err:
                _LOGGER.error("WebSocket message error: %s", err)

        def on_error(ws, error):
            _LOGGER.error("WebSocket error: %s", error)

        def on_close(ws):
            _LOGGER.warning("WebSocket closed")
            asyncio.run_coroutine_threadsafe(
                self._reconnect(),
                self.hass.loop,
            )

        self._ws = websocket.WebSocketApp(
            url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
        )

        asyncio.get_event_loop().run_in_executor(
            None,
            self._ws.run_forever,
        )

    async def _reconnect(self) -> None:
        await asyncio.sleep(5)
        await self._connect_websocket()

    async def _handle_motion_event(self) -> None:
        # kleine delay zodat Autodarts klaar is
        await asyncio.sleep(0.3)
        await self.async_refresh()

    # ==================================================
    # DATA FETCH (STATUS ZIT HIER)
    # ==================================================

    async def _async_update_data(self) -> dict[str, Any]:
        url = f"http://{self.host}:{self.port}{AUTODARTS_STATE_PATH}"

        try:
            async with self._session.get(url, timeout=2) as response:
                response.raise_for_status()
                raw_state = await response.json()

                # ✅ Autodarts is online
                self._online = True

                data = parse_x01_state(raw_state)
                data["autodarts_online"] = True
                return data

        except Exception as err:
            # ❌ Autodarts offline
            _LOGGER.error("Autodarts offline: %s", err)
            self._online = False

            return {
                "autodarts_online": False,
            }

    # ==================================================
    # SHUTDOWN
    # ==================================================

    async def async_close(self) -> None:
        if self._ws:
            self._ws.close()
        await self._session.close()

