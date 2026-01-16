from __future__ import annotations

from typing import Any

from .const import IMPOSSIBLE_CHECKOUTS


def dart_to_value(multiplier: int, number: int) -> int:
    if multiplier == 3:
        return number * 3
    if multiplier == 2:
        return number * 2
    if multiplier == 1:
        return number
    return 0


def format_dart(multiplier: int, number: int) -> str:
    if multiplier == 3:
        return f"T{number}"
    if multiplier == 2:
        return f"D{number}"
    if multiplier == 1:
        return f"S{number}"
    return "M"


def is_checkout_possible(remaining: int) -> bool:
    if remaining <= 1:
        return False
    if remaining > 170:
        return False
    return remaining not in IMPOSSIBLE_CHECKOUTS


def parse_x01_state(state: dict[str, Any]) -> dict[str, Any]:
    throws = state.get("throws") or []
    game = state.get("game") or {}
    players = game.get("players") or []
    current_player = state.get("currentPlayer", 0)

    darts = ["", "", ""]
    values = [0, 0, 0]

    for i in range(min(3, len(throws))):
        segment = throws[i].get("segment") or {}
        multiplier = segment.get("multiplier", 0)
        number = segment.get("number", 0)

        darts[i] = format_dart(multiplier, number)
        values[i] = dart_to_value(multiplier, number)

    remaining = 501
    checkout_possible = False
    leg_result = "playing"

    if players and current_player < len(players):
        remaining = players[current_player].get("score", remaining)
        chec

