// Historical research note for SLS-1 v3.
//
// The earlier browser recognition quizzes are no longer conformance gates.
// SLS-1 now models indicator use as:
// notice -> investigate -> lookup -> learned recognition.
//
// This module intentionally exposes no quiz/scoring implementation so that
// downstream examples cannot accidentally treat the retired protocol as normative.

export const RECOGNITION_RESEARCH_STATUS = "retired-nonconformance-research";

export const HUMAN_USE_SEQUENCE = [
  "notice",
  "investigate",
  "lookup",
  "learned_recognition",
];

export function recognitionResearchNotice() {
  return {
    status: RECOGNITION_RESEARCH_STATUS,
    sequence: [...HUMAN_USE_SEQUENCE],
    firstSightExactStateRequired: false,
    abstractBrowserQuizIsConformanceGate: false,
  };
}
