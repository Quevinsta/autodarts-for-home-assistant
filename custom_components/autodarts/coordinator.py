from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from aiohttp import ClientError

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import AUTODARTS_STATE_PATH
from .autodarts_api import parse_x01_state

_LOGGER = logging.getLogger(__name__)


EMPTY_STATE: dict[str, Any] = {
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


class AutodartsCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            name="Autodarts",
            update_interval=timedelta(seconds=10),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        url = f"http://{self.host}:{self.port}{AUTODARTS_STATE_PATH}"

        try:
            async with self.session.get(url, timeout=5) as response:
                response.raise_for_status()
                raw_state = await response.json()

                parsed = parse_x01_state(raw_state)

                # 🔒 DEFENSIVE: nooit aannemen dat parsed geldig is
                if not isinstance(parsed, dict):
                    _LOGGER.error(
                        "parse_x01_state returned invalid data: %s", parsed
                    )
                    data = EMPTY_STATE.copy()
                else:
                    data = parsed

                data["autodarts_online"] = True
                return data

        except (ClientError, TimeoutError) as err:
            _LOGGER.warning("Autodarts unreachable: %s", err)
            return EMPTY_STATE.copy()

        except Exception:
            _LOGGER.exception("Unexpected Autodarts error")
            return EMPTY_STATE.copy()

