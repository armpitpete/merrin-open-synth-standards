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
  const rng = makeRng(seed);
  const critical = new Set(spec.critical_global_states);
  const states = [...new Set([...spec.mandatory_states, ...spec.critical_global_states])];
  const trials = [];

  for (const state of states) {
    const repetitions = critical.has(state) ? 10 : 3;
    for (let i = 0; i < repetitions; i += 1) {
      const pattern = spec.patterns[spec.state_defaults[state]];
      const cycle = Number(pattern.cycle_ms || 1000);
      trials.push({
        state,
        phase_ms: Math.floor(rng() * cycle),
        critical: critical.has(state),
      });
    }
  }

  for (let i = trials.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rng() * (i + 1));
    [trials[i], trials[j]] = [trials[j], trials[i]];
  }
  return trials;
}

export function scoreRecognition(results, spec) {
  const critical = new Set(spec.critical_global_states);
  const total = results.length;
  const correct = results.filter((item) => item.correct).length;
  const overall = total ? correct / total : 0;

  const byState = {};
  for (const state of [...new Set([...spec.mandatory_states, ...spec.critical_global_states])]) {
    const rows = results.filter((item) => item.state === state);
    byState[state] = {
      attempts: rows.length,
      correct: rows.filter((item) => item.correct).length,
    };
  }

  const prohibited = {
    armed_warning_confusions: results.filter(
      (item) =>
        (item.state === "ARMED" && item.answer === "WARNING") ||
        (item.state === "WARNING" && item.answer === "ARMED"),
    ).length,
    error_active_confusions: results.filter(
      (item) =>
        (item.state === "ERROR" && item.answer === "ACTIVE") ||
        (item.state === "ACTIVE" && item.answer === "ERROR"),
    ).length,
  };

  const requiredPerfect = ["ERROR", "ARMED", "CONFIRM_REQUIRED", "RECORD_WRITE"];
  const perfectCritical = requiredPerfect.every(
    (state) => byState[state]?.attempts > 0 && byState[state].correct === byState[state].attempts,
  );

  return {
    total,
    correct,
    overall,
    byState,
    prohibited,
    pass:
      overall >= 0.9 &&
      perfectCritical &&
      prohibited.armed_warning_confusions === 0 &&
      prohibited.error_active_confusions === 0,
    critical_states_tested: [...critical],
  };
}
