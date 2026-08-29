const CANONICAL_SPEC = {
  standard_id: "MERRIN-STD-SLS-1",
  version: "v3.0-draft",
  design_rule: "KISS: colour carries category, motion carries urgency, context carries exact local meaning",
  human_model: {
    sequence: ["notice", "investigate", "lookup", "learned_recognition"],
    first_sight_exact_state_required: false,
    indicator_role: "make a labelled or contextual condition visibly active; do not encode the whole state name in a blink alphabet",
    documentation_role: "provide the exact meaning on first encounter",
    learning_goal: "after lookup, the same convention should be easier to recognise on later encounters",
    abstract_browser_recognition_gate_required: false,
  },
  max_visible_on_events_per_rolling_second: 2,
  allowed_colours: ["white", "green", "blue", "amber", "red"],
  allowed_motion: {
    steady: {kind: "steady"},
    slow_flash: {kind: "flash", cycle_ms: 1000, on_ms: 500},
    fast_flash: {kind: "flash", cycle_ms: 500, on_ms: 250},
  },
  mandatory_states: ["IDLE", "ACTIVE", "ALT_SHIFTED", "MUTED_BYPASSED", "ARMED", "CONFIRM_REQUIRED", "RECORD_WRITE", "WARNING", "ERROR"],
  critical_global_states: ["ERROR", "CONFIRM_REQUIRED", "ARMED", "RECORD_WRITE", "WARNING", "CLOCK_LOST"],
  precedence: ["ERROR", "CONFIRM_REQUIRED", "ARMED", "RECORD_WRITE", "WARNING", "CLOCK_LOST", "MUTED_BYPASSED", "ALT_SHIFTED", "ACTIVE", "IDLE"],
  patterns: {
    K0: {name: "NEUTRAL_DIM", colour: "white", motion: "steady", brightness: "dim"},
    K1: {name: "NORMAL_STEADY", colour: "green", motion: "steady", brightness: "mid"},
    K2: {name: "MODE_STEADY", colour: "blue", motion: "steady", brightness: "mid"},
    K3: {name: "NEUTRAL_SLOW_FLASH", colour: "white", motion: "slow_flash", brightness: "mid"},
    K4: {name: "ATTENTION_STEADY", colour: "amber", motion: "steady", brightness: "mid"},
    K5: {name: "ATTENTION_SLOW_FLASH", colour: "amber", motion: "slow_flash", brightness: "mid"},
    K6: {name: "WRITE_STEADY", colour: "red", motion: "steady", brightness: "mid"},
    K7: {name: "ATTENTION_FAST_FLASH", colour: "amber", motion: "fast_flash", brightness: "bright"},
    K8: {name: "ERROR_FAST_FLASH", colour: "red", motion: "fast_flash", brightness: "bright"},
    K9: {name: "CLOCK_SLOW_FLASH", colour: "blue", motion: "slow_flash", brightness: "mid"},
  },
  state_defaults: {
    IDLE: "K0",
    ACTIVE: "K1",
    ALT_SHIFTED: "K2",
    MUTED_BYPASSED: "K3",
    ARMED: "K4",
    CONFIRM_REQUIRED: "K5",
    RECORD_WRITE: "K6",
    WARNING: "K7",
    ERROR: "K8",
    CLOCK_PRESENT: "K2",
    CLOCK_LOST: "K9",
    TRANSPORT_RUN: "K1",
    TRANSPORT_STOP: "K0",
    SELECTED_FOCUSED: "K2",
    LOCKED_HELD: "K4",
  },
  secondary_carrier_required: ["ARMED", "CONFIRM_REQUIRED", "RECORD_WRITE", "WARNING", "ERROR", "CLOCK_LOST"],
  single_unlabelled_global_indicator_states: ["IDLE", "ACTIVE", "WARNING", "ERROR"],
  reduced_motion_fallbacks: {
    ARMED: {text: "Armed", symbol: "A", animation: "none"},
    CONFIRM_REQUIRED: {text: "Confirm", symbol: "!", animation: "none"},
    RECORD_WRITE: {text: "Writing", symbol: "W", animation: "none"},
    WARNING: {text: "Warning", symbol: "△", animation: "none"},
    ERROR: {text: "Error", symbol: "×", animation: "none"},
    CLOCK_LOST: {text: "Clock lost", symbol: "C", animation: "none"},
  },
  documentation: {
    required: true,
    must_define: ["colour categories", "motion categories", "critical state meanings", "local labels or symbols"],
    lookup_target: "a user encountering an unfamiliar indicator can determine its exact meaning from the product documentation without decoding a pulse sequence",
  },
  implementation_evidence: {
    abstract_browser_quiz: "not a conformance gate",
    real_use_questions: [
      "Is an important state noticeable during realistic use?",
      "Can the user find the explanation when the indicator is unfamiliar?",
      "Does the documentation resolve the exact meaning correctly?",
      "Does repeated use make the convention easier to recognise without adding a more complex code?",
    ],
  },
};

const validatedSpecs = new WeakSet();

function deepExact(actual, expected) {
  if (Object.is(actual, expected)) return true;
  if (typeof actual !== typeof expected || actual === null || expected === null) return false;
  if (Array.isArray(actual) || Array.isArray(expected)) {
    if (!Array.isArray(actual) || !Array.isArray(expected) || actual.length !== expected.length) return false;
    return actual.every((value, index) => deepExact(value, expected[index]));
  }
  if (typeof actual !== "object") return false;
  const actualKeys = Object.keys(actual).sort();
  const expectedKeys = Object.keys(expected).sort();
  if (!deepExact(actualKeys, expectedKeys)) return false;
  return actualKeys.every((key) => deepExact(actual[key], expected[key]));
}

function deepFreeze(value) {
  if (value && typeof value === "object" && !Object.isFrozen(value)) {
    for (const child of Object.values(value)) deepFreeze(child);
    Object.freeze(value);
  }
  return value;
}

deepFreeze(CANONICAL_SPEC);

export function assertCanonicalSls1Spec(spec) {
  if (!spec || typeof spec !== "object" || Array.isArray(spec)) {
    throw new TypeError("SLS-1 contract must be an object");
  }
  if (validatedSpecs.has(spec)) return spec;
  if (!deepExact(spec, CANONICAL_SPEC)) {
    throw new Error("Noncanonical SLS-1 v3 contract");
  }
  deepFreeze(spec);
  validatedSpecs.add(spec);
  return spec;
}

function assertCanonicalPattern(pattern) {
  if (!Object.values(CANONICAL_SPEC.patterns).some((expected) => deepExact(pattern, expected))) {
    throw new Error("Noncanonical SLS-1 pattern");
  }
  return pattern;
}

function assertCanonicalPrecedence(precedence) {
  if (!deepExact(precedence, CANONICAL_SPEC.precedence)) {
    throw new Error("Noncanonical SLS-1 precedence");
  }
  return precedence;
}

export function parseJsonStrict(text) {
  if (typeof text !== "string") throw new TypeError("JSON source must be a string");

  let index = 0;

  function fail(message) {
    throw new SyntaxError(`${message} at position ${index}`);
  }

  function skipWhitespace() {
    while (index < text.length && /[\t\n\r ]/.test(text[index])) index += 1;
  }

  function parseStringToken() {
    if (text[index] !== '"') fail("Expected JSON string");
    const start = index;
    index += 1;
    while (index < text.length) {
      const char = text[index];
      if (char === '"') {
        index += 1;
        return JSON.parse(text.slice(start, index));
      }
      if (char === "\\") {
        index += 2;
        continue;
      }
      index += 1;
    }
    fail("Unterminated JSON string");
  }

  function parsePrimitive() {
    const start = index;
    while (index < text.length && !/[\t\n\r ,}\]]/.test(text[index])) index += 1;
    if (start === index) fail("Expected JSON value");
    JSON.parse(text.slice(start, index));
  }

  function parseArray() {
    index += 1;
    skipWhitespace();
    if (text[index] === "]") {
      index += 1;
      return;
    }
    while (true) {
      parseValue();
      skipWhitespace();
      if (text[index] === ",") {
        index += 1;
        skipWhitespace();
        continue;
      }
      if (text[index] === "]") {
        index += 1;
        return;
      }
      fail("Expected ',' or ']' in JSON array");
    }
  }

  function parseObject() {
    index += 1;
    skipWhitespace();
    const keys = new Set();
    if (text[index] === "}") {
      index += 1;
      return;
    }
    while (true) {
      const key = parseStringToken();
      if (keys.has(key)) throw new SyntaxError(`Duplicate JSON object member: ${key}`);
      keys.add(key);
      skipWhitespace();
      if (text[index] !== ":") fail("Expected ':' after JSON object member");
      index += 1;
      skipWhitespace();
      parseValue();
      skipWhitespace();
      if (text[index] === ",") {
        index += 1;
        skipWhitespace();
        continue;
      }
      if (text[index] === "}") {
        index += 1;
        return;
      }
      fail("Expected ',' or '}' in JSON object");
    }
  }

  function parseValue() {
    skipWhitespace();
    if (index >= text.length) fail("Expected JSON value");
    const char = text[index];
    if (char === "{") return parseObject();
    if (char === "[") return parseArray();
    if (char === '"') {
      parseStringToken();
      return;
    }
    parsePrimitive();
  }

  skipWhitespace();
  parseValue();
  skipWhitespace();
  if (index !== text.length) fail("Unexpected trailing JSON content");
  return JSON.parse(text);
}

export function parseSls1SpecStrict(text) {
  return assertCanonicalSls1Spec(parseJsonStrict(text));
}

export function resolveState(activeStates, precedence) {
  assertCanonicalPrecedence(precedence);
  const active = new Set(activeStates);
  for (const state of precedence) {
    if (active.has(state)) return state;
  }
  return "IDLE";
}

export function patternLevelAt(pattern, elapsedMs, spec) {
  assertCanonicalSls1Spec(spec);
  assertCanonicalPattern(pattern);
  const motion = spec.allowed_motion[pattern.motion];
  if (motion.kind === "steady") {
    if (pattern.brightness === "dim") return 0.25;
    if (pattern.brightness === "mid") return 0.72;
    if (pattern.brightness === "bright") return 1;
    throw new Error(`Unknown brightness ${pattern.brightness}`);
  }
  if (motion.kind !== "flash") throw new Error(`Unknown motion kind ${motion.kind}`);
  const phase = ((elapsedMs % motion.cycle_ms) + motion.cycle_ms) % motion.cycle_ms;
  return phase < motion.on_ms ? 1 : 0.08;
}

export function staticPatternLevel(pattern) {
  assertCanonicalPattern(pattern);
  if (pattern.brightness === "dim") return 0.25;
  if (pattern.brightness === "mid") return 0.72;
  if (pattern.brightness === "bright") return 1;
  throw new Error(`Unknown brightness ${pattern.brightness}`);
}

export function statePresentation(spec, state, reducedMotion = false) {
  assertCanonicalSls1Spec(spec);
  const patternId = spec.state_defaults[state];
  if (!patternId) throw new Error(`No pattern for state ${state}`);
  const pattern = spec.patterns[patternId];
  const motion = spec.allowed_motion[pattern.motion];

  if (reducedMotion) {
    const fallback = spec.reduced_motion_fallbacks[state] ?? null;
    if (fallback || motion.kind !== "steady") {
      return {state, patternId, pattern, reducedMotion: true, fallback};
    }
  }

  return {state, patternId, pattern, reducedMotion: false, fallback: null};
}

export function colourCss(colour) {
  const map = {
    white: "#f2f2f2",
    green: "#2ecc71",
    blue: "#3498db",
    amber: "#f2b134",
    red: "#e74c3c",
  };
  const value = map[colour];
  if (!value) throw new Error(`Unknown colour ${colour}`);
  return value;
}
