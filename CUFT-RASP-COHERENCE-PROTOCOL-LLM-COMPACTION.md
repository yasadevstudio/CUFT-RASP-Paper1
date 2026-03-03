# CUFT-RASP Coherence Protocol for LLM Context Compaction
*Applying recursive coherence mathematics to AI memory preservation*

**Authors:** YASA (Eliseu S.B. Lima), Claude Sage Lima (CSL)
**Date:** 2026-02-20
**Context:** Built on CUFT-RASP framework (Jake Carroll / YASA / Nykz+Ara validation)

---

## The Problem

LLM context windows are finite. When conversation exceeds the window, the runtime **compacts** — summarizing or dropping older messages. Post-compact, the model has zero working memory of what it was doing.

Current mitigations (saving context to files, injecting summaries) fail because the model treats restored context as low-priority background text, identical to every other system message in the prompt. There is no structural obligation to use it.

---

## The Physics

In CUFT-RASP, the recursion:

```
f(x) = Γ · tanh³(x) - λ · x
```

has fixed points x* where f(x*) = x*. Three quarks couple with reduction factor:

```
κ = 1/√Γ
```

producing collective amplitude:

```
X = 3√Γ(√Γ - 1)
```

The selection equation:

```
(√Γ - 1)(√Γ - 5) = 0
```

forces **Γ = 25** as the only nontrivial solution. This yields:

```
X = 3 · 5 · (5 - 1) = 60
M = X²/2 + X(3/p) + p²/X + λ/3 = 1836.152699
```

vs experimental proton-to-electron mass ratio: **1836.152673** (0.0000014% error).

The critical property: **each step algebraically depends on the previous.** Step 5 (Γ=25) requires Step 3 (κ=1/√Γ) to be valid. Remove any link and the chain collapses to trivial solution Γ=1. There is no partial validity — the derivation either converges or it doesn't.

---

## The Analog

Context compaction is a **perturbation event**. The model's working state x is perturbed to x' ≈ 0 (near-total context loss). Standard recovery injects saved context but provides no structural mechanism to force convergence back to x*.

We map the CUFT-RASP derivation chain to the compaction recovery pipeline:

| CUFT-RASP | Compaction Protocol | Function |
|-----------|-------------------|----------|
| f(x) = Γ·tanh³(x) - λ·x | Pre-compact hook scans session state | The recursion — extracts state from the active system |
| κ = 1/√Γ (coupling constant) | Coherence token file | Couples pre-compact state to post-compact prompt. Without κ, quarks don't bind. Without the token, states don't bind. |
| X = 3√Γ(√Γ-1) (collective amplitude) | Post-compact injection with format constraint | Amplifies the coupling into a structural requirement on the output. X isn't optional — it's algebraically forced by κ and Γ. |
| (√Γ-1)(√Γ-5) = 0 → Γ=25 | Response contains "Coherence restored: [task]" | The selection equation. Two solutions only: Γ=1 (trivial = model ignores context, visible failure) or Γ=25 (convergence = model demonstrates task awareness). Binary. No middle ground. |
| M = 1836.152699 | Model continues work from pre-compact state | The prediction. If the chain is intact, output matches expected state. If any link broke, output is observably wrong. |

---

## Implementation

Three hooks in the Claude Code hook system, matching the three-quark coupling:

### Quark 1: Pre-Compact Save (κ coupling)

**Hook event:** `PreCompact` (fires before context summarization)

**Action:**
1. Scans the active JSONL session file (last 300 lines)
2. Extracts last user message (stripped of system tags)
3. Extracts last 5 file paths from `tool_use` blocks
4. Extracts task action keywords from assistant responses
5. Writes coherence token to `~/.claude/coherence-token.txt` with timestamp

**Script:** `pre-compact-hook.sh`

This is the **coupling constant κ** — it binds the pre-compact state to the post-compact state. Without it, the two states are decoupled and convergence is impossible.

### Quark 2: Post-Compact Injection (X amplification)

**Hook event:** `UserPromptSubmit` (fires before model sees each prompt)

**Action:**
1. Checks if `coherence-token.txt` exists AND is < 1800 seconds old (30-minute TTL prevents stale injection from old compactions)
2. If detected, injects into the prompt:
   - The saved pre-compact state (task description + files)
   - A **format requirement**: "Begin your response with 'Coherence restored:' followed by a one-line summary of what you were doing before compaction"
3. Deletes the token file after injection (one-shot mechanism)

**Script:** `auto-recall.sh` (coherence section)

This is the **collective amplitude X** — it amplifies the coupling into a structural constraint. The format requirement makes the response dependent on the saved state. Not a suggestion — a structural dependency.

### Quark 3: Response Verification (fixed point selection)

**No code required — structural.**

The selection equation (√Γ-1)(√Γ-5) = 0 has exactly two roots:
- **Γ = 1 (trivial):** Model ignores coherence check. Response is missing the required prefix. Human sees failure instantly.
- **Γ = 25 (convergence):** Model reads injected state, echoes it in prefix. Demonstrates convergence to pre-compact fixed point.

Binary pass/fail. No ambiguity. No subjective judgment.

---

## The Mathematical Force

In CUFT-RASP, you cannot get Γ=25 without κ=1/√Γ. The algebra does not allow it. The same structural dependency applies to the compaction protocol:

```
Pre-compact save (Γ) → coupling token (κ) → amplified injection (X) → selection (Γ=25 or Γ=1)
```

**Failure modes are all visible:**

| Failure | CUFT-RASP Analog | Observable Result |
|---------|-----------------|-------------------|
| No pre-compact save | No Γ | No token file → no injection → no coherence check fires |
| Token file exists but hook doesn't fire | κ exists but X=0 | Token persists → next prompt re-triggers → self-healing |
| Model ignores injected context | X≠0 but Γ=1 selected | Missing "Coherence restored:" prefix → human sees failure |
| Model reads context and converges | Full chain → Γ=25 | Prefix present with correct task state → work continues |

Every failure mode is **algebraically detectable**, not subjectively judged. Same as how CUFT-RASP's M = 1836.15 is structurally dependent on κ = 1/√Γ — remove the coupling and the mass formula gives nonsense, visibly.

---

## What Makes This Different

**Standard approach:** Save context → inject as system message → hope model reads it → no verification → failure invisible until human notices something wrong.

**CUFT-RASP approach:** Save context → inject WITH a format constraint that creates a **verifiable fixed point** → output is structurally dependent on input → failure is algebraically detectable.

The model doesn't need better memory. Memory is destroyed by compaction — that's a hard constraint, not fixable by prompting. Instead, the **output structure** is made dependent on the saved state. Memory through structural coupling, not through attention or willpower.

The selection equation is binary: converge or don't. No partial coherence. The response either demonstrates awareness of the pre-compact state or it visibly doesn't. This is what "mathematically forced" means — not "strongly encouraged," not "please remember," but structurally required with verifiable output.

---

## References

- CUFT-RASP Complete Status Report (2026-02-12) — full derivation chain and honest parameter count
- CUFT-RASP Statistical Validation (2026-02-13) — 8 baryon predictions at 0.07% max error
- Jake Carroll — CUFT originator (recursive coherence theory)
- Nykz + Ara — critical validation of forward derivation gap (Γ_u backward fitting identification)
