"""Real-browser check of the supplied unfinished shell, not completed rules.

Students add test_round.py using the real determine_winner function. This test
keeps the unfinished-path check useful after students implement their rules.
"""

import pytest
from playwright.sync_api import Page, expect

import app as web

pytestmark = pytest.mark.e2e


def test_unfinished_game_in_real_browser(page: Page, live_server, monkeypatch):
    """A Chromium click reaches the real server and shows the honest notice."""

    def unfinished(_player, _computer):
        raise NotImplementedError

    monkeypatch.setattr(web.game, "determine_winner", unfinished)
    monkeypatch.setattr(web.random, "choice", lambda _moves: "scissors")
    page.goto(live_server)
    for move in ("Rock", "Paper", "Scissors"):
        expect(page.get_by_role("button", name=move, exact=True)).to_be_visible()
    expect(page.get_by_role("status")).to_contain_text(
        "Starter: game rules not built yet."
    )

    page.get_by_role("button", name="Rock", exact=True).click()

    expect(page.get_by_label("This round’s choices")).to_be_visible()
    expect(page.get_by_text("You chose", exact=True)).to_be_visible()
    expect(page.get_by_text("Computer chose", exact=True)).to_be_visible()
    expect(page.get_by_role("status")).to_contain_text(
        "Starter: game rules not built yet."
    )
    expect(page.locator("[data-outcome]")).to_have_count(0)
