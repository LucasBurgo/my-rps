"""Local Rock, Paper, Scissors with a mode menu and cookie-backed matches."""

import os
import random

from flask import Flask, render_template, request, session

import game

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(32)
app.config.update(SESSION_COOKIE_SAMESITE="Lax", SESSION_COOKIE_HTTPONLY=True)
MOVES = {"rock": "✊", "paper": "✋", "scissors": "✌"}
MODES = {
    "free": ("Free mode", None),
    "best3": ("Best of 3", 2),
    "best5": ("Best of 5", 3),
}


@app.get("/")
def index():
    """A fresh visit or reload always returns to mode selection."""
    session.clear()
    response = app.make_response(render_template("index.html", moves=MOVES))
    response.headers["Cache-Control"] = "no-store"
    return response


@app.post("/match")
def start_match():
    """Start or restart a match with zero scores and no previous round."""
    mode = request.form.get("mode")
    if mode not in MODES:
        return {"error": "Choose Free mode, Best of 3, or Best of 5."}, 400
    match = {"mode": mode, "player_score": 0, "computer_score": 0, "finished": False}
    session["match"] = match
    return match


@app.post("/round")
def play_round():
    """Validate a move, apply real rules, and stop scoring finished matches."""
    player = request.form.get("move")
    if player not in MOVES:
        return {"error": "Choose Rock, Paper, or Scissors to play."}, 400
    match = session.get("match")
    if match is None:
        return {"error": "Choose a mode before playing."}, 409
    if match["finished"]:
        return {"error": "This match is over. Start a new match to play again."}, 409
    computer = random.choice(tuple(MOVES))
    outcome = game.determine_winner(player, computer)
    if outcome == "win":
        match["player_score"] += 1
    elif outcome == "lose":
        match["computer_score"] += 1
    target = MODES[match["mode"]][1]
    match["finished"] = target is not None and target in (
        match["player_score"],
        match["computer_score"],
    )
    session["match"] = match
    return {**match, "player": player, "computer": computer, "outcome": outcome}
