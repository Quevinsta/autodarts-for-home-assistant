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

    # defaults
    darts = ["M", "M", "M"]
    values = [0, 0, 0]
    remaining = 501
    checkout_possible = False
    leg_result = "playing"

    for i in range(min(3, len(throws))):
        segment = throws[i].get("segment") or {}
        multiplier = segment.get("multiplier", 0)
        number = segment.get("number", 0)

        darts[i] = format_dart(multiplier, number)
        values[i] = dart_to_value(multiplier, number)

    if players and current_player < len(players):
        remaining = players[current_player].get("score", remaining)
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
        # Dart strings
        "dart1": darts[0],
        "dart2": darts[1],
        "dart3": darts[2],

        # Dart values
        "dart1_value": values[0],
        "dart2_value": values[1],
        "dart3_value": values[2],

        # Summary (ALTIJD STRING → nooit Onbekend)
        "throw_summary": " | ".join(darts),

        # Totals
        "turn_total": sum(values),
        "remaining": remaining,

        # States
        "checkout_possible": checkout_possible,
        "is_180": sum(values) == 180,
        "leg_result": leg_result,

        # Status
        "autodarts_online": True,
    }

