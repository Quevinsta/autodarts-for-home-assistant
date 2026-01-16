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
            update_interval=None,  # push via websocket
        )

    async def async_start(self) -> None:
        await self.async_refresh()
        await self._connect_websocket()

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
            _LOGGER.warning("Autodarts WebSocket closed")

        self._ws = websocket.WebSocketApp(
            url,
            on_message=on_message,
            on_close=on_close,
        )

        asyncio.get_event_loop().run_in_executor(
            None,
            self._ws.run_forever,
        )

    # ---------------- DATA FETCH ----------------

    async def _async_update_data(self) -> dict[str, Any]:
        url = f"http://{self.host}:{self.port}{AUTODARTS_STATE_PATH}"

        try:
            async with self._session.get(url, timeout=2) as response:
                response.raise_for_status()
                raw_state = await response.json()

                data = parse_x01_state(raw_state)
                data["autodarts_online"] = True
                return data

        except Exception as err:
            _LOGGER.error("Autodarts offline: %s", err)

            return {
                "autodarts_online": False,
                "dart1": "",
                "dart2": "",
                "dart3": "",
                "dart1_value": 0,
                "dart2_value": 0,
                "dart3_value": 0,
                "throw_summary": "",
                "turn_total": 0,
                "remaining": 0,
                "checkout_possible": False,
                "is_180": False,
                "leg_result": "unknown",
            }

    async def async_close(self) -> None:
        if self._ws:
            self._ws.close()
        await self._session.close()

