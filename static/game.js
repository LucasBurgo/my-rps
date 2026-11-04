"use strict";

const menu = document.querySelector("#menu");
const board = document.querySelector("#board");
const error = document.querySelector("#error");
const modeForm = document.querySelector("#mode-form");
const moveForm = document.querySelector("#move-form");
const heading = document.querySelector("#game-heading");
const result = document.querySelector(".result");
const choices = document.querySelector("#choices");
const labels = {free: "Free mode · Unlimited rounds", best3: "Best of 3 · First to 2 wins", best5: "Best of 5 · First to 3 wins"};
const moves = {rock: "Rock", paper: "Paper", scissors: "Scissors"};
const outcomes = {win: "You win!", lose: "Computer wins", tie: "It’s a tie"};
let mode = null;
let busy = false;
let finished = false;

async function send(path, data) {
  if (busy) return;
  busy = true;
  error.hidden = true;
  document.querySelectorAll("button").forEach(button => { button.disabled = true; });
  try {
    const response = await fetch(path, {method: "POST", body: new URLSearchParams(data)});
    const state = await response.json();
    if (!response.ok) throw new Error(state.error || "Unable to play. Try again.");
    mode = state.mode;
    finished = state.finished;
    menu.hidden = true;
    board.hidden = false;
    document.querySelector("#mode-label").textContent = labels[mode];
    document.querySelector("#player-score").textContent = state.player_score;
    document.querySelector("#computer-score").textContent = state.computer_score;
    choices.hidden = !state.outcome;
    if (state.outcome) {
      document.querySelector("#player-choice").textContent = moves[state.player];
      document.querySelector("#computer-choice").textContent = moves[state.computer];
      result.dataset.outcome = state.outcome;
      heading.textContent = finished ? (state.outcome === "win" ? "You win the match!" : "Computer wins the match") : outcomes[state.outcome];
    } else {
      delete result.dataset.outcome;
      heading.textContent = "Your next move?";
    }
    document.querySelector("#result-detail").textContent = finished ? "Match complete. Start a new match or change mode." : "Choose a move below to play. Ties award no points.";
    if (!state.outcome || finished) {
      const focusTarget = finished ? document.querySelector("#restart") : moveForm.querySelector("button");
      requestAnimationFrame(() => focusTarget.focus());
    }
  } catch (failure) {
    error.textContent = failure.message;
    error.hidden = false;
  } finally {
    busy = false;
    document.querySelectorAll("button").forEach(button => { button.disabled = false; });
    moveForm.querySelectorAll("button").forEach(button => { button.disabled = finished; });
  }
}

modeForm.addEventListener("submit", event => {
  event.preventDefault();
  if (event.submitter) send("/match", {mode: event.submitter.value});
});
moveForm.addEventListener("submit", event => {
  event.preventDefault();
  if (event.submitter && !finished) send("/round", {move: event.submitter.value});
});
document.querySelector("#restart").addEventListener("click", () => send("/match", {mode}));
document.querySelector("#change-mode").addEventListener("click", () => { window.location.assign("/"); });
