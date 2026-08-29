# SLS-1 v1/v2 → v3 migration

SLS-1 v3 is a breaking simplification.

## Why

v1/v2 attempted to keep one light expressive by assigning several distinct temporal signatures. v2 made those signatures mechanically cleaner, but the resulting vocabulary still required memorising pulse counts and order.

The v3 KISS decision changes the design goal:

```text
Do not teach a more complicated blink language.
Use colour + simple motion + context.
```

## Required migration

| Earlier design | v3 replacement |
|---|---|
| steady dim IDLE | white dim steady |
| steady ACTIVE | green steady |
| breathe ALT/SHIFTED | blue steady |
| long pulse MUTED/BYPASSED | white slow flash or labelled local state |
| double pulse ARMED | amber steady + contextual carrier |
| triple pulse CONFIRM REQUIRED | amber slow flash + contextual carrier |
| short pulse RECORD/WRITE | red steady + contextual carrier |
| short→long WARNING | amber fast flash + contextual carrier |
| long→short ERROR | red fast flash + contextual carrier |
| special CLOCK LOST double | blue slow flash + contextual carrier |

## Removed concepts

The following are not part of v3:

- counted pulse groups;
- short–long / long–short temporal words;
- breathing as a state code;
- a requirement that every exact critical state be encoded by one anonymous global light.

## Human evidence

Do not reuse v1/v2 recognition results as v3 evidence.

The v3 gate is a separate unfamiliar-person test defined in `standards/data/sls-1-v3.0-kiss.json`.
