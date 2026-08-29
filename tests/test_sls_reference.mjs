import assert from "node:assert/strict";
import fs from "node:fs";
import {colourCss, patternLevelAt, resolveState, statePresentation} from "../examples/sls-1-reference/sls.mjs";

const spec = JSON.parse(fs.readFileSync(new URL("../standards/data/sls-1-v3.0-kiss.json", import.meta.url), "utf8"));

assert.equal(resolveState(["ACTIVE", "WARNING"], spec.precedence), "WARNING");
assert.equal(resolveState(["ARMED", "CONFIRM_REQUIRED"], spec.precedence), "CONFIRM_REQUIRED");
assert.equal(resolveState(["ERROR", "ACTIVE"], spec.precedence), "ERROR");
assert.equal(resolveState([], spec.precedence), "IDLE");

assert.equal(colourCss("amber"), "#f2b134");
assert.throws(() => colourCss("purple"), /Unknown colour/);

const armed = spec.patterns[spec.state_defaults.ARMED];
assert.equal(patternLevelAt(armed, 0, spec), 0.72);

const confirm = spec.patterns[spec.state_defaults.CONFIRM_REQUIRED];
assert.equal(patternLevelAt(confirm, 0, spec), 1);
assert.ok(patternLevelAt(confirm, 750, spec) < 0.2);

const error = spec.patterns[spec.state_defaults.ERROR];
assert.equal(patternLevelAt(error, 0, spec), 1);
assert.ok(patternLevelAt(error, 300, spec) < 0.2);
assert.equal(patternLevelAt(error, 550, spec), 1);

for (const state of spec.critical_global_states) {
  const reduced = statePresentation(spec, state, true);
  assert.equal(reduced.reducedMotion, true);
  assert.equal(reduced.fallback.animation, "none");
  assert.ok(reduced.fallback.text.length > 0);
}

assert.deepEqual(spec.human_model.sequence, ["notice", "investigate", "lookup", "learned_recognition"]);
assert.equal(spec.human_model.first_sight_exact_state_required, false);
assert.equal(spec.human_model.abstract_browser_recognition_gate_required, false);
assert.equal(spec.documentation.required, true);
assert.equal(spec.implementation_evidence.abstract_browser_quiz, "not a conformance gate");
assert.equal("recognition_gate" in spec, false);

console.log("PASS: SLS-1 v3 KISS reference and learnability contract");
