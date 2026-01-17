import asyncio
import json
import logging
import websockets

from .const import AUTODARTS_WS_PATH

_LOGGER = logging.getLogger(__name__)


class AutodartsWebSocket:
    def __init__(self, host: str, port: int, on_event):
        self._url = f"ws://{host}:{port}{AUTODARTS_WS_PATH}"
        self._on_event = on_event
        self._task = None
        self._running = False

    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()

    async def _run(self):
        while self._running:
            try:
                async with websockets.connect(self._url) as ws:
                    _LOGGER.info("Autodarts WebSocket connected")
                    async for message in ws:
                        data = json.loads(message)
                        await self._on_event(data)
            except Exception as err:
                _LOGGER.warning("WebSocket error: %s", err)
                await asyncio.sleep(2)

