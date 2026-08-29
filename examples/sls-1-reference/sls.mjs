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

export function resolveState(activeStates, precedence) {
  const active = new Set(activeStates);
  for (const state of precedence) {
    if (active.has(state)) return state;
  }
  return "IDLE";
}

export function patternLevelAt(pattern, elapsedMs, spec) {
  const motion = spec.allowed_motion[pattern.motion];
  if (!motion) throw new Error(`Unknown motion ${pattern.motion}`);
  if (motion.kind === "steady") {
    if (pattern.brightness === "dim") return 0.25;
    if (pattern.brightness === "mid") return 0.72;
    return 1;
  }
  const phase = ((elapsedMs % motion.cycle_ms) + motion.cycle_ms) % motion.cycle_ms;
  return phase < motion.on_ms ? 1 : 0.08;
}

export function staticPatternLevel(pattern) {
  if (pattern.brightness === "dim") return 0.25;
  if (pattern.brightness === "mid") return 0.72;
  return 1;
}

export function statePresentation(spec, state, reducedMotion = false) {
  const patternId = spec.state_defaults[state];
  if (!patternId) throw new Error(`No pattern for state ${state}`);
  const pattern = spec.patterns[patternId];
  if (!pattern) throw new Error(`Unknown pattern ${patternId}`);
  const motion = spec.allowed_motion[pattern.motion];
  if (!motion) throw new Error(`Unknown motion ${pattern.motion}`);

  if (reducedMotion) {
    const fallback = spec.reduced_motion_fallbacks[state] ?? null;
    if (fallback || motion.kind !== "steady") {
      return {
        state,
        patternId,
        pattern,
        reducedMotion: true,
        fallback,
      };
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
