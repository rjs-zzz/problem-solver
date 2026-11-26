# 저장소 작업 규칙 (problem-solver)

이 저장소는 Claude 플러그인 마켓플레이스다. 같은 SKILL.md를 Claude(웹·데스크톱·Claude Code)·ChatGPT·Gemini가 함께 읽는다.

## 단일 원본 — 사본을 직접 고치지 않는다

| 원본 | 생성되는 사본 | 반영 명령 |
|---|---|---|
| `COMMON_CONTROLS.md` | 모든 SKILL.md의 「실행 통제 (공통)」 블록 | `python tools/sync_common.py` |
| `shared/*.md` | 각 스킬 `references/` | 같음 |
| `evals/cases.md` | `plugins/*/evals/<사례>/` (claude plugin eval용) | `python tools/build_evals.py` |
| `plugins/*/skills/*` | `dist/*.zip` (웹 업로드용) | `python tools/build_dist.py` |

- `plugins/problem-solver/skills/problem-solver/modules/06_critic-review.md`가 원본이고 red-team의 06은 사본(MIRRORS)이다.
- 레드팀 자동 실행 구성: `plugins/problem-solver/agents/red-team-reviewer.md` + `plugins/problem-solver/commands/red-team-run.md`. 규약은 `shared/rt_protocol.md` 7절.

## 고친 뒤 반드시

```
python tools/sync_common.py && python tools/build_dist.py && python tools/build_evals.py && python tools/validate.py
```

validate가 실패하면 커밋하지 않는다. Windows(Git Bash)에서 `python`이 없으면 `py`로 실행한다.

## 쓰는 규칙

- **스킬 본문**(`plugins/*/skills/**`)에는 특정 AI 환경 이름(Claude Code·ChatGPT 등)을 쓰지 않는다 — "하위 작업을 띄우는 도구가 있는 환경"처럼 능력으로 쓴다.
- Claude Code 전용 기능은 스킬 밖 `plugins/<플러그인>/agents/`·`commands/`에 둔다 (웹 업로드 zip에 들어가지 않는다). `${CLAUDE_PLUGIN_ROOT}` 경로는 validate가 실재를 확인한다.
- 버전은 `.claude-plugin/marketplace.json`(metadata·각 항목)·모든 `plugin.json`·`CHANGELOG.md` 최신 항목을 같은 값으로 올린다. 절차 변경은 minor, 문구·지식 원장만이면 patch.
- 저장소에 기관 내부 정보·개인정보·실명·내부 금액을 넣지 않는다 (공개 저장소).

## 개선·시험

- 월간 자가개선은 `MAINTENANCE.md` 절차를 따른다 — main에 직접 올리지 않고 PR만 만든다.
- 행동 시험: `claude plugin eval plugins/<플러그인> --allow-tools WebSearch WebFetch` (사용량이 든다). 결과 요약은 `evals/results/YYYY-MM-DD_<버전>.md`에 남긴다.
