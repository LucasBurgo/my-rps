"""Literal rule outcomes and real HTTP round behavior."""

# pylint: disable=missing-function-docstring
import pytest
import app as web
from game import determine_winner


@pytest.mark.unit
@pytest.mark.parametrize(
    ("player", "computer", "expected"),
    [
        ("rock", "rock", "tie"),
        ("rock", "paper", "lose"),
        ("rock", "scissors", "win"),
        ("paper", "rock", "win"),
        ("paper", "paper", "tie"),
        ("paper", "scissors", "lose"),
        ("scissors", "rock", "lose"),
        ("scissors", "paper", "win"),
        ("scissors", "scissors", "tie"),
    ],
)
def test_nine_matchups(player, computer, expected):
    assert determine_winner(player, computer) == expected


@pytest.mark.integration
def test_predicted_losing_round(monkeypatch):
    monkeypatch.setattr(web.random, "choice", lambda _moves: "paper")
    with web.app.test_client() as client:
        client.post("/match", data={"mode": "best3"})
        response = client.post("/round", data={"move": "rock"})
    assert response.status_code == 200
    assert response.json == {
        "mode": "best3",
        "player_score": 0,
        "computer_score": 1,
        "finished": False,
        "player": "rock",
        "computer": "paper",
        "outcome": "lose",
    }
