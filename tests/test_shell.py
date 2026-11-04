"""Request validation and supplied interface checks."""

# pytest fixtures and descriptive test names provide the test documentation.
# pylint: disable=redefined-outer-name,missing-function-docstring

import pytest
import app as web

pytestmark = pytest.mark.integration


@pytest.fixture
def client():
    web.app.config.update(TESTING=True)
    return web.app.test_client()


def test_page_has_modes_and_three_labeled_moves(client):
    response = client.get("/")
    assert response.status_code == 200
    for move in ("rock", "paper", "scissors"):
        assert f'name="move" value="{move}"'.encode() in response.data
        assert move.capitalize().encode() in response.data
    for label in (b"Free mode", b"Best of 3", b"Best of 5"):
        assert label in response.data
    assert b' id="board"' in response.data
    assert b"game rules not built yet" not in response.data


@pytest.mark.parametrize("move", ["lizard", "<script>alert(1)</script>", ""])
def test_invalid_move_is_rejected_before_rules(client, monkeypatch, move):
    def should_not_run(_player, _computer):
        pytest.fail("Invalid input must not reach the rule function")

    monkeypatch.setattr(web.game, "determine_winner", should_not_run)
    response = client.post("/round", data={"move": move})
    assert response.status_code == 400
    assert response.json["error"] == "Choose Rock, Paper, or Scissors to play."
    assert b"<script>" not in response.data


def test_missing_move_is_rejected(client, monkeypatch):
    def should_not_run(_player, _computer):
        pytest.fail("A missing move must not reach the rule function")

    monkeypatch.setattr(web.game, "determine_winner", should_not_run)
    response = client.post("/round")
    assert response.status_code == 400
    assert response.json["error"] == "Choose Rock, Paper, or Scissors to play."


def test_stylesheet_is_available(client):
    response = client.get("/static/style.css")
    assert response.status_code == 200
    assert b"focus-visible" in response.data


def test_check_server_has_no_development_refresh(client):
    assert b"dev-refresh.js" not in client.get("/").data
    assert client.get("/__dev__/revision").status_code == 404
