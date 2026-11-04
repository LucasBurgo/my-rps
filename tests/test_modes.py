"""Match boundaries, score changes, validation, and reset through real HTTP."""

# pylint: disable=redefined-outer-name,missing-function-docstring
import pytest
import app as web

pytestmark = pytest.mark.integration


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(web.random, "choice", lambda _moves: "scissors")
    return web.app.test_client()


@pytest.mark.parametrize("mode,target", [("best3", 2), ("best5", 3)])
@pytest.mark.parametrize(
    "round_case", [("rock", "player_score"), ("paper", "computer_score")]
)
def test_match_stops_at_target(client, mode, target, round_case, monkeypatch):
    move, winner = round_case
    assert client.post("/match", data={"mode": mode}).status_code == 200
    for number in range(1, target + 1):
        state = client.post("/round", data={"move": move}).json
        assert state[winner] == number
        assert state["finished"] == (number == target)
    with client.session_transaction() as stored:
        final = dict(stored["match"])

    def should_not_run(_player, _computer):
        pytest.fail("Finished matches must not run rules or score again")

    monkeypatch.setattr(web.game, "determine_winner", should_not_run)
    assert client.post("/round", data={"move": "rock"}).status_code == 409
    with client.session_transaction() as stored:
        assert stored["match"] == final


def test_ties_do_not_score_or_finish(client):
    client.post("/match", data={"mode": "best3"})
    client.post("/round", data={"move": "rock"})
    for _ in range(4):
        state = client.post("/round", data={"move": "scissors"}).json
        assert state["outcome"] == "tie"
        assert (state["player_score"], state["computer_score"]) == (1, 0)
        assert state["finished"] is False


def test_free_play_has_no_win_limit(client):
    client.post("/match", data={"mode": "free"})
    for number in range(1, 11):
        state = client.post("/round", data={"move": "rock"}).json
        assert state["player_score"] == number
        assert state["finished"] is False


def test_restart_and_reload_clear_match(client):
    client.post("/match", data={"mode": "best3"})
    client.post("/round", data={"move": "rock"})
    client.post("/round", data={"move": "rock"})
    state = client.post("/match", data={"mode": "best3"}).json
    assert state == {
        "mode": "best3",
        "player_score": 0,
        "computer_score": 0,
        "finished": False,
    }
    client.post("/round", data={"move": "paper"})
    assert client.get("/").status_code == 200
    assert client.post("/round", data={"move": "rock"}).status_code == 409


@pytest.mark.parametrize("mode", [None, "", "best7", "<script>"])
def test_invalid_mode_preserves_match(client, mode):
    client.post("/match", data={"mode": "free"})
    client.post("/round", data={"move": "rock"})
    response = client.post("/match", data={} if mode is None else {"mode": mode})
    assert response.status_code == 400
    assert "Choose Free mode" in response.json["error"]
    assert client.post("/round", data={"move": "rock"}).json["player_score"] == 2


def test_round_requires_mode_and_clients_are_isolated(client):
    assert client.post("/round", data={"move": "rock"}).status_code == 409
    client.post("/match", data={"mode": "free"})
    other = web.app.test_client()
    assert other.post("/round", data={"move": "rock"}).status_code == 409
