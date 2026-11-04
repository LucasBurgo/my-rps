"""Supplied browser shell. Students implement the rules in game.py."""

import random

from flask import Flask, render_template, request

import game

app = Flask(__name__)

MOVES = {"rock": "✊", "paper": "✋", "scissors": "✌"}
RESULTS = {
    "win": ("You win!", "Nice move. Ready for another round?"),
    "lose": ("Computer wins", "A rematch is one click away."),
    "tie": ("It’s a tie", "Great minds think alike. Try again?"),
}


@app.route("/", methods=["GET", "POST"])
def index():
    """Display a supplied shell or the result of one submitted round."""
    player = computer = outcome = None
    unfinished = False
    error = None

    if request.method == "GET":
        # A harmless tie probe hides the starter notice once the rules exist.
        try:
            game.determine_winner("rock", "rock")
        except NotImplementedError:
            unfinished = True

    if request.method == "POST":
        player = request.form.get("move")
        if player not in MOVES:
            error = "Choose Rock, Paper, or Scissors to play."
            player = None
        else:
            computer = random.choice(tuple(MOVES))
            try:
                outcome = game.determine_winner(player, computer)
            except NotImplementedError:
                unfinished = True

    return render_template(
        "index.html",
        moves=MOVES,
        player=player,
        computer=computer,
        outcome=outcome,
        result=RESULTS[outcome] if outcome is not None else None,
        unfinished=unfinished,
        error=error,
    ), (400 if error else 200)
