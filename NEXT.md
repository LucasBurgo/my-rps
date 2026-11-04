# Choose your next feature

**Your turn with less guidance.** Finish and merge RPS-001 first. Choose **one** small feature, write your own short request, and ask AI to help clarify examples and checks before coding.

Give the agent your own example of what should happen. Keep the conversation: predict an outcome, explain one test together, then try the result and describe what you saw. Ask for one step at a time whenever you need help.

| Feature | What you practice |
| --- | --- |
| **RPS-002: First to two wins** — suggested next step | State, ties, match boundaries, and reset. See the starting decisions below. |
| **RPS-003: Explain the result** — e.g. “Paper covers rock” | Turning examples into clear output and testing every matchup, including ties. |
| **RPS-004: Make it yours** — a game title, colors, and move symbols | Describing a design, reviewing it in the browser, and keeping readable contrast and text labels. |

Reopen the same project. With a clean working tree, start your change from updated `main`; use `rps-003` or `rps-004` in the last command if you chose that feature:

```sh
git switch main
git pull --ff-only
git switch -c rps-002
```

Then use the README's **Returning later** instructions to run the game.

Add only your chosen feature to `SPEC.md`. Give it its own issue and PR. Keep the existing rules and checks working.

Repeat: discuss → update the spec and open an issue → build → AI checks → your review → PR.

## Suggested next step: RPS-002

Agree these decisions **before** coding:

- A win adds one point to the winner. Ties add no points.
- Show both scores. The first side to two wins the match.
- After the match, keep the final result visible and stop further scoring.
- A **New match** control resets both scores and clears the previous result.
- Decide what refreshing the page does. Keep storage/accounts outside this change.

Add RPS-002 to `SPEC.md`, with examples for a tie, a match win, another click after the match, and reset. Ask AI how it will test the sequence deterministically and preserve RPS-001’s nine rules. Choose the simplest design together; do not add a database or architecture pattern just for this exercise.

Plan valid play and rejected post-match actions at the appropriate test level. Keep most scoring/reset combinations in fast tests and one complete match/reset journey in the browser. Run `.venv/bin/python check.py` before review; passing the old round tests alone does not verify the new match behavior.

Ask AI to test and review first, then try it yourself. Explain one result using its requirement, code, and test before keeping the change.
