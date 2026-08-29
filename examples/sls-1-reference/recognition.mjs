export function makeRng(seed = 0x51a71e) {
  let state = seed >>> 0;
  return () => {
    state ^= state << 13;
    state ^= state >>> 17;
    state ^= state << 5;
    return (state >>> 0) / 0x100000000;
  };
}

export function buildRecognitionTrials(spec, seed = 0x51a71e) {
  const gate = spec.recognition_gate;
  const rng = makeRng(seed);
  const trials = [];

  for (const state of gate.states) {
    for (let i = 0; i < gate.repetitions_per_state; i += 1) {
      const pattern = spec.patterns[spec.state_defaults[state]];
      const motion = spec.allowed_motion[pattern.motion];
      const cycle = Number(motion.cycle_ms || 1000);
      trials.push({state, phase_ms: Math.floor(rng() * cycle)});
    }
  }

  for (let i = trials.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rng() * (i + 1));
    [trials[i], trials[j]] = [trials[j], trials[i]];
  }
  return trials;
}

export function scoreRecognition(results, spec) {
  const gate = spec.recognition_gate;
  const total = results.length;
  const correct = results.filter((item) => item.correct).length;
  const overall = total ? correct / total : 0;

  const byState = {};
  for (const state of gate.states) {
    const rows = results.filter((item) => item.state === state);
    byState[state] = {
      attempts: rows.length,
      correct: rows.filter((item) => item.correct).length,
    };
  }

  const perfectRequired = gate.perfect_states.every(
    (state) => byState[state]?.attempts > 0 && byState[state].correct === byState[state].attempts,
  );

  const prohibited = {};
  for (const [a, b] of gate.prohibited_confusions) {
    const key = `${a}_${b}`.toLowerCase();
    prohibited[key] = results.filter(
      (item) =>
        (item.state === a && item.answer === b) ||
        (item.state === b && item.answer === a),
    ).length;
  }

  return {
    total,
    correct,
    overall,
    byState,
    prohibited,
    pass:
      overall >= gate.minimum_overall_accuracy &&
      perfectRequired &&
      Object.values(prohibited).every((count) => count === 0),
  };
}
