# Problem-Solver

[한국어 README](https://github.com/rjs-zzz/problem-solver)

A structured problem-solving Claude Skill that walks any work problem
through **6 phases** (Framing → Structuring → Root Cause → Options →
Decision → Reporting), and runs every conclusion through a **5-persona
critic panel** before it's finalized.

Triggers on requests that need a **single, defensible conclusion**
(a choice, a go/no-go, a root-cause finding) — "should we do A or B",
"what's actually causing this", "help me decide".

Especially useful for public-sector and government-agency work —
policy judgment calls, project reviews, and comparative decision
memos. The default output leads with the conclusion in a bulleted
structure, and every claim is tagged by evidence tier with facts kept
separate from assumptions — the kind of paper trail an audit or an
oversight board expects to see.

For building an actual plan document — a long-term development plan,
management plan, or business plan — use the companion
**[planning-suite-en](https://github.com/rjs-zzz/planning-suite-en)**
skill set instead. It carries a matter from environmental scan
through goals, strategic initiatives, feasibility review, roadmap,
and feedback framework, producing output in a consistent report
format at every stage while automatically validating consistency
between phases.

## Why this skill

In a normal chat, Claude answers as soon as you ask. This skill
forces it to actually walk through consulting-grade methodology
instead.

- Enforces proven frameworks at each stage — **5 Whys, MECE logic
  trees, Kepner-Tregoe root-cause analysis, Working Backwards,
  weighted decision matrices**
- At standard/full scale, every conclusion passes through a
  **5-persona critic panel** (First-Principles Thinker, Naive
  Outsider, 360° Auditor, Frontier Creator, Full Dissenter) — each
  sees only a one-page brief and attacks from a different angle
  before the panel renders a verdict (short-form scale condenses this
  to an abbreviated 5-axis review + one steelman pass)
- Evidence is graded on a 4-tier scale ([Tier 1] local/primary
  sources down to [Tier 4] press releases), with confirmed facts and
  assumptions always labeled separately
- Completion criteria, length caps, and report scale are defined up
  front so the process doesn't run indefinitely

## Install

### Claude Code — one-line install (recommended)

```
/plugin marketplace add rjs-zzz/problem-solver
/plugin install problem-solver@problem-solver
```

### Claude.ai (web/desktop/mobile)

Zip the folder `plugins/problem-solver/skills/problem-solver/` and upload it on
the Skills screen (the menu path varies by plan and date — see the
[official guide](https://support.claude.com/en/articles/12512180)).

### See the output before installing

[`examples/01_short-report_교육시스템-교체.md`](examples/01_short-report_교육시스템-교체.md)
shows a complete short-form run: reframing, Kepner-Tregoe diagnosis, weighted
matrix, assumption ledger, and the critical review panel.

## Structure

```
problem-solver/
├── .claude-plugin/marketplace.json
├── plugins/problem-solver/
│   ├── .claude-plugin/plugin.json
│   └── skills/problem-solver/
│       ├── SKILL.md                    # Workflow control, trigger conditions
│       ├── modules/
│       │   ├── 00_problem-framing.md   # Problem framing (5 Whys, Drucker reframing)
│       │   ├── 01_issue-structuring.md # MECE logic tree decomposition
│       │   ├── 02_root-cause.md        # Kepner-Tregoe root cause
│       │   ├── 03_options.md           # Working Backwards option generation
│       │   ├── 04_decision.md          # Weighted matrix + reversibility test
│       │   ├── 05_reporting.md         # Minto pyramid decision memo
│       │   └── 06_critic-review.md     # Five-dissenter critical review panel
│       └── templates/
│           ├── report_short.md         # Short report (1-3 pages)
│           ├── report_full.md          # Standard / deep report (5-15 pages)
│           └── decision_matrix.md      # Weighted decision matrix template
├── examples/                           # Real output samples
├── COMMON_CONTROLS.md
└── tools/sync_common.py
```

## Works Well With — Planning Suite

This skill is built for one thing: a **single conclusion** (a
choice, a go/no-go, a root-cause finding). If what you're actually
working on is a full plan document, or you want one of the
deliverables below, the separate
**[planning-suite-en](https://github.com/rjs-zzz/planning-suite-en)**
repository (P1–P6 + the control skill `planning-orchestrator`, 7
skills total) is the better fit.

| What you want | Which skill |
|---|---|
| A single conclusion (A vs. B, root-cause finding, go/no-go) | **this repository (problem-solver)** |
| Environmental scan (PEST, 3C, VRIO, SWOT) | planning-suite-en's `env-scanning-loop-p1` |
| Goal framework (mission, vision, OKR, KPI) | planning-suite-en's `goal-setting-loop-p2` |
| Strategic-initiative discovery (ERRC, portfolio) | planning-suite-en's `strategy-option-loop-p3` |
| Feasibility review (budget, legal, resource screening) | planning-suite-en's `feasibility-review-loop-p4` |
| Execution roadmap (RACI, milestones, KPI rollout) | planning-suite-en's `roadmap-design-loop-p5` |
| Feedback/monitoring framework | planning-suite-en's `feedback-loop-p6` |
| A full plan document, or 2+ phases needed in sequence | planning-suite-en's `planning-orchestrator` |

The two sets are designed to reference each other — if a
planning-suite-en skill hits a point where it needs a single judgment
call ("which of these options should we pick"), it delegates to this
skill; conversely, if this skill determines a request is really "a
component of a planning document," it points to the matching Phase
skill. Install both and this handoff happens automatically.
The decision comes back as a `[DATA-PS-OUTPUT]` block
(`templates/data_block.md`), so planning-suite inherits assumptions,
Go/No-Go conditions, and the execution outline without re-entry.

## Notes on use

- **Customizing for your organization**: the "Organizational Context
  Checkpoint" section at the end of SKILL.md and each module is
  written generically on purpose. Filling it in with your own
  applicable laws, stakeholder map, and evaluation framework (public
  agency, corporate, hospital, etc.) meaningfully improves accuracy.
- **Korean-language version**: this is the English-language version
  of this skill. A Korean-language version — with output in Korean
  government report format — is maintained as a separate repository:
  [problem-solver](https://github.com/rjs-zzz/problem-solver).

## License

MIT License — free to use, modify, distribute, and use commercially.
Attribution isn't required, but it's appreciated.
