# Rock, Paper, Scissors

## RPS-001: Play a round

**Purpose:** one person plays a quick round against the computer.

- Choose rock, paper, or scissors. The computer chooses one move for that round.
- Display both choices and the result: **You win!**, **Computer wins**, or **It’s a tie**.
- Each choice plays a round. The agreed modes below add match scoring without saved history.
- Extend the supplied interface and server with mode selection and score display.

### Expected results

Results are from the **player’s perspective**. `determine_winner(player, computer)` in `game.py` returns `win`, `lose`, or `tie`. Inputs are the lowercase moves below; the supplied server rejects other choices.

| Player | Computer | Expected return |
| --- | --- | --- |
| rock | rock | tie |
| rock | paper | lose |
| rock | scissors | win |
| paper | rock | win |
| paper | paper | tie |
| paper | scissors | lose |
| scissors | rock | lose |
| scissors | paper | win |
| scissors | scissors | tie |

### Agreed plan

Implement ties and the three winning pairs in `game.py`, returning results from the player's perspective. The learner predicted that Rock loses to Paper because paper covers rock. Check all nine literal matchups, real HTTP results, rejected missing/unsupported moves, and a real browser round with replay. Extend the supplied interface and server with the modes agreed below.

### Agreed extension: game modes

- Before playing, choose Free mode (unlimited rounds), Best of 3 (first to 2 wins), or Best of 5 (first to 3 wins).
- Show both scores. A round win adds one point to its winner; ties add no points.
- When a match finishes, keep the result visible and prevent further rounds/scoring.
- New match restarts the same mode with zero scores and no previous result. Change mode returns to selection.
- Reloading the page returns to mode selection and discards the match, as requested by the learner.
- Use the existing Flask app and styling, with a small JavaScript controller. Keep per-browser match state in a signed session cookie; no accounts or database.
- Check both match lengths, both winners, ties, unlimited free play, invalid mode/move input, post-match rejection, restart, reload, and browser mode selection/match completion.

### Checks

Visual update requested after the modes: replace the pale appearance with a colorful arcade style. Use a dark grid background, lime/pink/blue accents, SVG move icons, raised buttons, and clear score panels. Keep the agreed modes and rules. Stack mode cards on narrow screens, preserve keyboard focus indicators, and respect reduced-motion preferences.

Before coding, agree this small test plan with AI:

| Level | Cases and evidence |
| --- | --- |
| Unit — positive | All nine literal expected results above, including valid losses and ties. |
| Integration — positive | A submitted round uses the real rule function and displays both choices and the correct result. Fix the computer choice for the test. |
| Integration — negative | Reuse supplied missing/unsupported-move tests: HTTP 400 and a helpful explanation, without calling the rules. A crash is not the intended result. |
| E2E — positive | Add a real-browser round and replay in tests/e2e/test_round.py using the supplied live_server/page fixtures. Fix only the computer choice; use real rules and real HTTP. |

Use `unit`, `integration`, and `e2e` pytest markers. Run `.venv/bin/python check.py` for Black, Pylint, fast tests, and browser checks; then review the diff. Keep shared settings and meaningful assertions intact. The student still plays, inspects a rule and its test, and gives feedback. Browser automation does not establish every aspect of usability or application performance.

### Work record

- Issue: [RPS-001: Playable RPS game with game modes #1](https://github.com/LucasBurgo/my-rps/issues/1).
- Pull request: [RPS-001: Playable RPS with game modes #2](https://github.com/LucasBurgo/my-rps/pull/2).
- CI: [Python checks for implementation commit 5e3c7ae](https://github.com/LucasBurgo/my-rps/actions/runs/41781903930). Confirm checks pass on the latest PR commit before merging.
- Implementation: [winner rules](game.py), [match API](app.py), [mode menu](templates/index.html), and [browser controller](static/game.js). Implemented Free mode, Best of 3, Best of 5, score display, match completion, restart, and reload to selection.
- Checks: Full `.venv/bin/python check.py` passed: Black, Pylint, 29 non-browser tests, and 8 Chromium tests. [Rules and predicted loss](tests/test_game.py), [match scoring and validation](tests/test_modes.py), [browser round/replay and matches](tests/e2e/test_round.py). Existing input checks now exercise `/round`; development reload checks start from the new menu. Removed unfinished-rule checks because the rules are implemented; replaced them with completed-game/menu checks.
- Review: Compared implementation and tests with the nine expected results and agreed modes. The learner reported playing Paper against the computer's Rock and seeing a player win, consistent with paper covering rock. When the learner saw no mistake in the test example, explained that the passing assertion would catch a future rule bug returning `lose` or `tie` for Paper against Rock. Issue, PR, and actual CI run are linked above.
- Visual review: Inspected desktop menu and mobile gameplay screenshots. Browser previews at 1365px, 390px, and 320px had no horizontal overflow or JavaScript errors. Reduced-motion styling was verified. Replaced missing Ubuntu emoji glyphs with local [SVG icons](static/moves.svg); the Python-save browser check now verifies that changing available moves updates the rendered buttons.
