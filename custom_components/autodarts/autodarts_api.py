from __future__ import annotations

from typing import Any

from .const import IMPOSSIBLE_CHECKOUTS


def dart_to_value(multiplier: int, number: int) -> int:
    if multiplier == 3:
        return number * 3
    if multiplier == 2:
        return number * 2
    if multiplier == 0:
        return 0
    return number


def format_dart(multiplier: int, number: int) -> str:
    if multiplier == 3:
        return f"T{number}"
    if multiplier == 2:
        return f"D{number}"
    if multiplier == 0:
        return f"M{number}"
    return str(number)


def is_checkout_possible(remaining: int) -> bool:
    if remaining <= 1:
        return False
    if remaining > 170:
        return False
    return remaining not in IMPOSSIBLE_CHECKOUTS


def parse_x01_state(state: dict[str, Any]) -> dict[str, Any]:
    throws = state.get("throws", [])
    game = state.get("game", {})
    players = game.get("players", [])
    current_player = state.get("currentPlayer", 0)

    darts = ["0", "0", "0"]
    values = [0, 0, 0]

    for i in range(min(3, len(throws))):
        segment = throws[i].get("segment", {})
        multiplier = segment.get("multiplier", 0)
        number = segment.get("number", 0)

        darts[i] = format_dart(multiplier, number)
        values[i] = dart_to_value(multiplier, number)

    remaining = 0
    checkout_possible = False
    leg_result = "playing"

    if players and current_player < len(players):
        remaining = players[current_player].get("score", 0)
        checkout_possible = is_checkout_possible(remaining)

        if players[current_player].get("hasWon"):
            leg_result = "win"
        elif any(
            p.get("hasWon")
            for i, p in enumerate(players)
            if i != current_player
        ):
            leg_result = "lose"

    return {
        "dart1": darts[0],
        "dart2": darts[1],
        "dart3": darts[2],
        "dart1_value": values[0],
        "dart2_value": values[1],
        "dart3_value": values[2],
        "turn_total": sum(values),
        "remaining": remaining,
        "checkout_possible": checkout_possible,
        "is_180": sum(values) == 180,
        "leg_result": leg_result,
    }

