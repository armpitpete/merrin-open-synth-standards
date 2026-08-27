import assert from "node:assert/strict";
import fs from "node:fs";
import {patternLevelAt, resolveState, statePresentation} from "../examples/sls-1-reference/sls.mjs";
import {buildRecognitionTrials, scoreRecognition} from "../examples/sls-1-reference/recognition.mjs";

const spec = JSON.parse(fs.readFileSync(new URL("../standards/data/sls-1-v2.0-patterns.json", import.meta.url), "utf8"));

assert.equal(resolveState(["ACTIVE", "WARNING"], spec.precedence), "WARNING");
assert.equal(resolveState(["ARMED", "CONFIRM_REQUIRED"], spec.precedence), "CONFIRM_REQUIRED");
assert.equal(resolveState(["ERROR", "CONFIRM_REQUIRED", "ACTIVE"], spec.precedence), "ERROR");
assert.equal(resolveState([], spec.precedence), "IDLE");

for (const state of spec.critical_global_states) {
  const normal = statePresentation(spec, state, false);
  assert.equal(normal.reducedMotion, false);
  assert.ok(normal.pattern);
  const reduced = statePresentation(spec, state, true);
  assert.equal(reduced.reducedMotion, true);
  assert.equal(reduced.fallback.animation, "none");
  assert.ok(reduced.fallback.text.length > 0);
}

const armed = spec.patterns[spec.state_defaults.ARMED];
assert.equal(patternLevelAt(armed, 0), 1);
assert.ok(patternLevelAt(armed, 200) < 0.2);
assert.equal(patternLevelAt(armed, 300), 1);

const trials = buildRecognitionTrials(spec, 12345);
assert.equal(trials.filter((row) => row.state === "ERROR").length, 10);
assert.equal(trials.filter((row) => row.state === "CLOCK_LOST").length, 10);
assert.equal(trials.filter((row) => row.state === "IDLE").length, 3);

const perfect = trials.map((row, i) => ({
  trial: i + 1,
  state: row.state,
  answer: row.state,
  correct: true,
  phase_ms: row.phase_ms,
  critical: row.critical,
}));
assert.equal(scoreRecognition(perfect, spec).pass, true);

const confused = perfect.map((row) => ({...row}));
const armedIndex = confused.findIndex((row) => row.state === "ARMED");
confused[armedIndex].answer = "WARNING";
confused[armedIndex].correct = false;
assert.equal(scoreRecognition(confused, spec).pass, false);

console.log("PASS: SLS-1 reference resolver and recognition harness");
