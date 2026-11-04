"""Rock, Paper, Scissors rules from the player's perspective. See SPEC.md."""


def determine_winner(player: str, computer: str) -> str:
    """Return 'win', 'lose', or 'tie' from the player's perspective.

    The supplied web page accepts only 'rock', 'paper', and 'scissors'.
    Expected results are recorded in SPEC.md.
    """
    if player == computer:
        return "tie"
    winning_pairs = {("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")}
    return "win" if (player, computer) in winning_pairs else "lose"
