import assert from "node:assert/strict";
import fs from "node:fs";
import {
  assertCanonicalSls1Spec,
  colourCss,
  parseJsonStrict,
  parseSls1SpecStrict,
  patternLevelAt,
  resolveState,
  statePresentation,
  staticPatternLevel,
} from "../examples/sls-1-reference/sls.mjs";

const specText = fs.readFileSync(new URL("../standards/data/sls-1-v3.0-kiss.json", import.meta.url), "utf8");
const spec = parseSls1SpecStrict(specText);
const cloneSpec = () => JSON.parse(specText);

// Duplicate-member ambiguity must be rejected before JSON.parse constructs an object.
assert.throws(
  () => parseJsonStrict('{"allowed_motion":{"steady":{"kind":"steady"}},"allowed_motion":{"steady":{"kind":"flash","cycle_ms":100,"on_ms":50}}}'),
  /Duplicate JSON object member: allowed_motion/,
);
assert.throws(
  () => parseJsonStrict('{"allowed_motion":{"fast_flash":{"kind":"flash","cycle_ms":500,"cycle_ms":100,"on_ms":250}}}'),
  /Duplicate JSON object member: cycle_ms/,
);
assert.throws(
  () => parseJsonStrict('{"reduced_motion_fallbacks":{"ERROR":{"text":"Error","text":"All clear","symbol":"×","animation":"none"}}}'),
  /Duplicate JSON object member: text/,
);
assert.throws(
  () => parseJsonStrict('{"documentation":{"required":true,"required":false}}'),
  /Duplicate JSON object member: required/,
);
assert.throws(
  () => parseJsonStrict('{"allowed_motion":{},"allowed_\\u006dotion":{}}'),
  /Duplicate JSON object member: allowed_motion/,
);

// Unambiguous but semantically noncanonical contracts must also be rejected.
{
  const candidate = cloneSpec();
  candidate.allowed_motion.double_flash = {kind: "flash", cycle_ms: 200, on_ms: 50};
  assert.throws(() => assertCanonicalSls1Spec(candidate), /Noncanonical SLS-1 v3 contract/);
}
{
  const candidate = cloneSpec();
  candidate.allowed_motion.fast_flash.cycle_ms = 100;
  candidate.allowed_motion.fast_flash.on_ms = 50;
  assert.throws(() => assertCanonicalSls1Spec(candidate), /Noncanonical SLS-1 v3 contract/);
}
{
  const candidate = cloneSpec();
  candidate.state_defaults.ERROR = "K1";
  assert.throws(() => statePresentation(candidate, "ERROR", false), /Noncanonical SLS-1 v3 contract/);
}
{
  const candidate = cloneSpec();
  candidate.reduced_motion_fallbacks.ERROR.text = "All clear";
  assert.throws(() => statePresentation(candidate, "ERROR", true), /Noncanonical SLS-1 v3 contract/);
}
{
  const candidate = cloneSpec();
  candidate.documentation.required = false;
  assert.throws(() => assertCanonicalSls1Spec(candidate), /Noncanonical SLS-1 v3 contract/);
}
{
  const candidate = cloneSpec();
  candidate.allowed_motion.fast_flash.cycle_ms = 100;
  const raw = JSON.stringify(candidate);
  assert.throws(() => parseSls1SpecStrict(raw), /Noncanonical SLS-1 v3 contract/);
}

// Direct exported helper inputs must not provide a renderer bypass.
{
  const precedence = [...spec.precedence].reverse();
  assert.throws(() => resolveState(["ERROR", "ACTIVE"], precedence), /Noncanonical SLS-1 precedence/);
}
{
  const candidate = cloneSpec();
  candidate.allowed_motion.fast_flash = {kind: "pulse_train", cycle_ms: 100, on_ms: 50};
  const pattern = candidate.patterns.K8;
  assert.throws(() => patternLevelAt(pattern, 0, candidate), /Noncanonical SLS-1 v3 contract/);
}
assert.throws(
  () => staticPatternLevel({name: "HIDDEN", colour: "red", motion: "steady", brightness: "bright"}),
  /Noncanonical SLS-1 pattern/,
);

assert.equal(Object.isFrozen(spec), true);
assert.equal(Object.isFrozen(spec.allowed_motion), true);
assert.equal(Object.isFrozen(spec.reduced_motion_fallbacks.ERROR), true);

assert.equal(resolveState(["ACTIVE", "WARNING"], spec.precedence), "WARNING");
assert.equal(resolveState(["ARMED", "CONFIRM_REQUIRED"], spec.precedence), "CONFIRM_REQUIRED");
assert.equal(resolveState(["ERROR", "ACTIVE"], spec.precedence), "ERROR");
assert.equal(resolveState([], spec.precedence), "IDLE");

assert.equal(colourCss("amber"), "#f2b134");
assert.throws(() => colourCss("purple"), /Unknown colour/);

const armed = spec.patterns[spec.state_defaults.ARMED];
assert.equal(patternLevelAt(armed, 0, spec), 0.72);
assert.equal(staticPatternLevel(armed), 0.72);

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

const mutedReduced = statePresentation(spec, "MUTED_BYPASSED", true);
assert.equal(mutedReduced.reducedMotion, true);
assert.equal(mutedReduced.fallback, null);
assert.equal(spec.allowed_motion[mutedReduced.pattern.motion].kind, "flash");
assert.equal(staticPatternLevel(mutedReduced.pattern), 0.72);

const activeReduced = statePresentation(spec, "ACTIVE", true);
assert.equal(activeReduced.reducedMotion, false);
assert.equal(activeReduced.fallback, null);

assert.deepEqual(spec.human_model.sequence, ["notice", "investigate", "lookup", "learned_recognition"]);
assert.equal(spec.human_model.first_sight_exact_state_required, false);
assert.equal(spec.human_model.abstract_browser_recognition_gate_required, false);
assert.equal(spec.documentation.required, true);
assert.equal(spec.implementation_evidence.abstract_browser_quiz, "not a conformance gate");
assert.equal("recognition_gate" in spec, false);

console.log("PASS: SLS-1 v3 KISS reference, strict JSON, semantic validation, and direct-input guards");
