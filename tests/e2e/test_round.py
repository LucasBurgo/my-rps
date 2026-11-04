"""Real rules and HTTP: round replay, match completion, reset, and reload."""

import pytest
from playwright.sync_api import Page, expect
import app as web

pytestmark = pytest.mark.e2e


def test_round_and_replay(page: Page, live_server, monkeypatch):
    """The learner's Rock/Paper example displays a loss and can be replayed."""
    monkeypatch.setattr(web.random, "choice", lambda _moves: "paper")
    page.goto(live_server)
    page.get_by_role("button", name="Free mode").click()
    page.get_by_role("button", name="Rock", exact=True).click()
    expect(
        page.get_by_role("heading", name="Computer wins", exact=True)
    ).to_be_visible()
    expect(page.locator("#player-choice")).to_contain_text("Rock")
    expect(page.locator("#computer-choice")).to_contain_text("Paper")
    expect(page.locator("#computer-score")).to_have_text("1")
    page.get_by_role("button", name="Scissors", exact=True).click()
    expect(page.get_by_role("heading", name="You win!", exact=True)).to_be_visible()
    expect(page.locator("#player-score")).to_have_text("1")


@pytest.mark.parametrize("mode_case", [("Best of 3", 2), ("Best of 5", 3)])
def test_match_reset_and_refresh(page: Page, live_server, monkeypatch, mode_case):
    """Ties, match lock, restart, mode changes and reload use real requests."""
    mode, target = mode_case
    monkeypatch.setattr(web.random, "choice", lambda _moves: "scissors")
    page.goto(live_server)
    page.get_by_role("button", name=mode).click()
    page.get_by_role("button", name="Scissors", exact=True).click()
    expect(page.get_by_role("heading", name="It’s a tie")).to_be_visible()
    expect(page.locator("#player-score")).to_have_text("0")
    for number in range(1, target + 1):
        page.get_by_role("button", name="Rock", exact=True).click()
        expect(page.locator("#player-score")).to_have_text(str(number))
    expect(page.get_by_role("heading", name="You win the match!")).to_be_visible()
    expect(page.get_by_role("button", name="Rock", exact=True)).to_be_disabled()
    page.get_by_role("button", name="New match", exact=True).click()
    expect(page.locator("#player-score")).to_have_text("0")
    expect(page.get_by_label("This round’s choices")).to_be_hidden()
    expect(page.get_by_role("button", name="Rock", exact=True)).to_be_enabled()
    page.get_by_role("button", name="Rock", exact=True).click()
    expect(page.locator("#player-score")).to_have_text("1")
    page.reload()
    expect(page.get_by_role("heading", name="Choose your mode")).to_be_visible()
    expect(page.locator("#board")).to_be_hidden()
    page.get_by_role("button", name="Free mode").click()
    expect(page.locator("#player-score")).to_have_text("0")
    page.get_by_role("button", name="Change mode").click()
    expect(page.get_by_role("heading", name="Choose your mode")).to_be_visible()
