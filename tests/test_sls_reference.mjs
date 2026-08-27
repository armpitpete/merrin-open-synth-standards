import assert from "node:assert/strict";
import fs from "node:fs";
import {patternLevelAt, resolveState, statePresentation} from "../examples/sls-1-reference/sls.mjs";

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

console.log("PASS: SLS-1 reference resolver and renderer");
