# Problem-Solver

[한국어 README](README.md)

A structured problem-solving Claude Skill that walks any work problem
through **6 phases** (Framing → Structuring → Root Cause → Options →
Decision → Reporting), and runs every conclusion through a **5-persona
critic panel** before it's finalized.

Triggers on requests that need a **single, defensible conclusion**
(a choice, a go/no-go, a root-cause finding) — "should we do A or B",
"what's actually causing this", "help me decide".

Especially useful for **public-sector and government agency work** —
policy judgment calls, project reviews, and comparative decision
memos. The default output follows Korean government report
conventions (lead-with-conclusion, bulleted structure), and every
claim is tagged by evidence tier with facts kept separate from
assumptions — the kind of paper trail an audit or an oversight board
expects to see.

## Why this skill

In a normal chat, Claude answers as soon as you ask. This skill
forces it to actually walk through consulting-grade methodology
instead.

- Enforces proven frameworks at each stage — **5 Whys, MECE logic
  trees, Kepner-Tregoe root-cause analysis, Working Backwards,
  weighted decision matrices**
- Every conclusion passes through a **5-persona critic panel**
  (First-Principles Thinker, Naive Outsider, 360° Auditor, Frontier
  Creator, Full Dissenter) — each sees only a one-page brief and
  attacks from a different angle before the panel renders a verdict
- Evidence is graded on a 4-tier scale ([Tier 1] local/primary
  sources down to [Tier 4] press releases), with confirmed facts and
  assumptions always labeled separately
- Completion criteria, length caps, and report scale are defined up
  front so the process doesn't run indefinitely

## Install

### Claude.ai (web / desktop / mobile)
1. Open the Skills upload screen in Claude settings (the exact menu
   path varies by plan — see the
   [official guide](https://support.claude.com/en/articles/12512180))
2. Upload the `problem-solver` folder as a zip

### Claude Code
Drop the folder into `~/.claude/skills/problem-solver/`
(or `.claude/skills/` for a project-scoped install).

## Structure

```
problem-solver/
├── SKILL.md                        # Workflow overview, trigger conditions
├── modules/
│   ├── 00_problem-framing.md       # Problem definition (5 Whys, Drucker-style reframe)
│   ├── 01_issue-structuring.md     # MECE logic tree decomposition
│   ├── 02_root-cause.md            # Kepner-Tregoe root-cause diagnosis
│   ├── 03_options.md               # Working Backwards option generation
│   ├── 04_decision.md              # Weighted decision matrix + reversibility check
│   ├── 05_reporting.md             # Minto Pyramid decision-request report
│   └── 06_critic-review.md         # 5-persona critic panel review
└── templates/
    ├── report_short.md             # Short-form report (1–3 pages)
    ├── report_full.md              # Standard/detailed report (5–15 pages)
    └── decision_matrix.md          # Weighted decision matrix template
```

## Notes on use

- **Customizing for your organization**: the "Organizational Context
  Checkpoint" section at the end of SKILL.md and each module is
  written generically on purpose. Filling it in with your own
  applicable laws, stakeholder map, and evaluation framework (public
  agency, corporate, hospital, etc.) meaningfully improves accuracy.
- **Language**: this skill is Korean-only. Every instruction, module,
  and template is written in Korean, and the output format follows
  Korean government report conventions (lead-with-conclusion,
  bulleted structure, 【 】 heading system). To use it in English,
  you'd need to translate the "출력 표준" (Output Standard) section of
  SKILL.md and each module yourself.
- **Relationship to the Phase skills**: if the request is really one
  component of a larger planning document, the `planning-suite` set
  (P1–P6 + orchestrator, separate repository) may fit better than this
  skill alone. `planning-orchestrator` is the name of the control
  skill inside that set, not the repository.

## License

MIT License — free to use, modify, distribute, and use commercially.
Attribution isn't required, but it's appreciated.
