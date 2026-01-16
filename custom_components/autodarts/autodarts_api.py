from __future__ import annotations

from typing import Any

from .const import IMPOSSIBLE_CHECKOUTS


EMPTY_STATE: dict[str, Any] = {
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


def dart_value(multiplier: int, number: int) -> int:
    if multiplier == 3:
        return number * 3
    if multiplier == 2:
        return number * 2
    if multiplier == 1:
        return number
    return 0


def dart_label(multiplier: int, number: int) -> str:
    if multiplier == 3:
        return f"T{number}"
    if multiplier == 2:
        return f"D{number}"
    if multiplier == 1:
        return f"S{number}"
    return "M"


def is_checkout_possible(remaining: int) -> bool:
    if remaining <= 1 or remaining > 170:
        return False
    return remaining not in IMPOSSIBLE_CHECKOUTS


def parse_x01_state(state: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(state, dict):
        return EMPTY_STATE.copy()

    data = EMPTY_STATE.copy()

    throws = state.get("throws") or []
    game = state.get("game") or {}
    players = game.get("players") or []
    current_player = state.get("currentPlayer", 0)

    # ---- darts ----
    for i in range(min(3, len(throws))):
        segment = throws[i].get("segment") or {}
        multiplier = segment.get("multiplier", 0)
        number = segment.get("number", 0)

        label = dart_label(multiplier, number)
        value = dart_value(multiplier, number)

        data[f"dart{i+1}"] = label
        data[f"dart{i+1}_value"] = value

    data["throw_summary"] = " | ".join(
        data[f"dart{i}"] for i in (1, 2, 3) if data[f"dart{i}"]
    )
    data["turn_total"] = (
        data["dart1_value"] + data["dart2_value"] + data["dart3_value"]
    )

    # ---- remaining / checkout ----
    if players and current_player < len(players):
        remaining = players[current_player].get("score", 0)
        data["remaining"] = remaining
        data["checkout_possible"] = is_checkout_possible(remaining)

        if players[current_player].get("hasWon"):
            data["leg_result"] = "win"
        elif any(p.get("hasWon") for i, p in enumerate(players) if i != current_player):
            data["leg_result"] = "lose"

    data["is_180"] = data["turn_total"] == 180

    return data

