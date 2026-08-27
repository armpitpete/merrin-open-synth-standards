export function resolveState(activeStates, precedence) {
  const active = new Set(activeStates);
  for (const state of precedence) {
    if (active.has(state)) return state;
  }
  return "IDLE";
}

export function patternLevelAt(pattern, elapsedMs) {
  if (pattern.kind === "steady") {
    if (pattern.brightness === "dim") return 0.25;
    if (pattern.brightness === "mid") return 0.65;
    return 1;
  }
  if (pattern.kind === "breathe") {
    const cycle = pattern.cycle_ms;
    const phase = ((elapsedMs % cycle) + cycle) % cycle / cycle;
    const low = Number(pattern.min_brightness ?? 0.2);
    const high = Number(pattern.max_brightness ?? 0.8);
    const wave = (1 - Math.cos(phase * Math.PI * 2)) / 2;
    return low + (high - low) * wave;
  }
  if (pattern.kind === "pulse") {
    const cycle = pattern.cycle_ms;
    let phase = ((elapsedMs % cycle) + cycle) % cycle;
    for (const segment of pattern.segments) {
      if (phase < segment.duration_ms) return segment.level ? 1 : 0.08;
      phase -= segment.duration_ms;
    }
    return 0.08;
  }
  throw new Error(`Unsupported pattern kind: ${pattern.kind}`);
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
