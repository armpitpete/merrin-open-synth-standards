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

export function statePresentation(spec, state, reducedMotion = false) {
  const patternId = spec.state_defaults[state];
  if (!patternId) throw new Error(`No pattern for state ${state}`);
  const pattern = spec.patterns[patternId];
  if (!pattern) throw new Error(`Unknown pattern ${patternId}`);

  if (reducedMotion && spec.reduced_motion_fallbacks[state]) {
    return {
      state,
      patternId,
      pattern,
      reducedMotion: true,
      fallback: spec.reduced_motion_fallbacks[state],
    };
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
