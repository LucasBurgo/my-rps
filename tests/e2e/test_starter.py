"""Real-browser checks for the mode menu and invalid-round feedback."""

import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e


def test_mode_menu_and_invalid_round(page: Page, live_server):
    """Mode selection precedes play; the API retains useful validation."""
    page.goto(live_server)
    for name in ("Free mode", "Best of 3", "Best of 5"):
        expect(page.get_by_role("button", name=name)).to_be_visible()
    expect(page.get_by_role("button", name="Rock", exact=True)).to_be_hidden()
    response = page.request.post(live_server + "/round", form={"move": "lizard"})
    assert response.status == 400
    assert response.json()["error"] == "Choose Rock, Paper, or Scissors to play."
