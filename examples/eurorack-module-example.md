# Example — Eurorack Module

This example shows how a small Eurorack-style module can apply SLS-1 v3 and HIL-1.

It is illustrative, not human-recognition evidence.

## Module

```text
Example name: Small Delay / Memory Module
Width: 8HP or 10HP
Main functions: input, delay/memory, feedback, wet/dry output
```

## HIL-1 layout

```text
Title / identity
↓
main performance controls
↓
secondary controls and mode switch
↓
state LEDs near affected controls
↓
patch jacks
```

## SLS-1 v3 state map

| Behaviour | State | Expression |
|---|---|---|
| Powered but idle | IDLE | white dim steady |
| Delay active | ACTIVE | green steady |
| Alternate mode held | ALT / SHIFTED | blue steady |
| Delay path bypassed | MUTED / BYPASSED | white slow flash |
| About to clear memory | ARMED | amber steady beside CLEAR |
| Waiting to confirm clear | CONFIRM REQUIRED | amber slow flash beside CONFIRM/CLEAR |
| Writing/saving setting | RECORD / WRITE | red steady beside WRITE/MEMORY |
| Feedback unsafe/high | WARNING | amber fast flash + warning carrier |
| Internal fault | ERROR | red fast flash + error carrier |

## Clear-memory flow

```text
normal
→ deliberate clear/arm
→ ARMED
→ deliberate proceed
→ CONFIRM REQUIRED
→ explicit confirm
→ RECORD / WRITE while memory is actually changed
→ IDLE/ACTIVE on success
→ WARNING/ERROR on failure
```

Timeout or cancel must not clear memory.

## KISS rule

If an exact meaning cannot be understood from colour + simple motion + where the light is located, add context. Do not add another pulse word.

## Common mistake

Weak design:

```text
LED blinks randomly with delay activity and also means armed/error.
```

Better design:

```text
Audio activity has its own meter or is omitted.
State indicators use the small SLS-1 v3 vocabulary.
```
