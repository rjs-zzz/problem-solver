# Problem-Solver

[English README](README.en.md)

업무 문제를 **6단계(정의 → 구조화 → 진단 → 대안 → 결정 → 보고)**로 해결하고,
최종 결론 전 **5인 반대자 패널**의 비판적 검토를 자동으로 거치는
구조적 문제해결 Claude Skill입니다. 함께 들어 있는 **red-team** 스킬은 그 검토를
**새 대화 · 다른 모델**에서 다시 돌려, 작성한 쪽이 스스로를 채점하는 한계를 줄입니다.

"이 문제 어떻게 해결하지", "A안 B안 중 뭐가 나아", "판단해줘" 같은
**단일 결론(선택·가부·원인 판정)이 필요한 요청**에 반응합니다.

공공기관·관공서의 정책 판단·사업 검토·대안 비교 보고서 작성에
특히 유용합니다 — 기재부·행안부 보고서 양식(두괄식·개조식)을
기본으로 출력하고, 근거 등급·가정 표기·감사 대응력까지 자동으로
챙깁니다.

중장기 발전계획·경영계획·사업계획 등 계획서 수립 업무의 경우에는 
환경분석부터 목표 체계, 전략과제, 타당성 검토, 로드맵, 환류 체계까지 
기재부·행안부 보고서 양식 그대로 이어서 산출하고, 
단계별 정합성을 자동으로 검증하는 planning-suite skill(https://github.com/rjs-zzz/planning-suite) 사용하세요. 

## 빠른 시작

**1. 설치** — 아래 [설치](#설치). Claude.ai는 zip 파일 하나를 올리면 끝납니다.

**2. 요청** — 평소 말투로 쓰면 됩니다. 발동하지 않으면 앞에 "problem-solver로"를 붙이세요.

- "problem-solver로 검토해줘. 노후 교육시스템을 교체할지 유지보수 계약을 연장할지 정해야 해."
- "A안(자체 개발)과 B안(외주) 중 뭐가 나은지 판단해줘."
- "민원 처리 기간이 작년보다 길어진 원인 분석해줘."

**3. 준비물** — 많이 줄수록 결론이 단단해집니다. 꼭 필요한 것은 위 두 줄뿐입니다.

| 준비물 | 없으면 |
|---|---|
| **문제** — 무엇을 결정해야 하나 (필수) | 스킬이 먼저 묻습니다 |
| **선택지의 내용** — 비교·가부 판단을 요청할 때 (필수) | 스킬이 먼저 묻습니다 |
| 성공 기준 — 무엇이 되면 해결인가 | 가정으로 정하고 표시 — 권고안 순위가 달라질 수 있음 |
| 제약 — 예산 상한·인력·기한·규정 | 모든 대안을 실행 가능하다고 가정 |
| 근거 자료 — 실적·견적·규정·회의록 | 금액 계산 없이 등급 판정만 (수치를 지어내지 않음) |
| 조직 정보 — 아래 `[조직 프로필]` | 일반 조직 기준 적용 |

"준비물 양식 줘"라고 하면 채워 넣을 양식을 보여줍니다. 스킬은 **필수가 빠졌을 때만** 멈춰서 묻고,
나머지는 가정으로 채운 뒤 보고서 첫 장에 **입력 현황**과 **바뀌면 결론이 달라지는 입력 3개**를 적습니다.
→ [입력 점검 예시](examples/00_입력점검-예시.md)

**4. 조직 맞춤** — 아래 블록을 한 번 써서 대화에 붙여넣으세요. 파일을 고칠 필요가 없습니다.
(프로젝트 지침처럼 매번 자동으로 들어가는 곳에 저장해 두면 다시 붙여넣지 않아도 됩니다.)

```
[조직 프로필]
- 조직 유형: (예: 공공기관 / 지자체 / 민간기업 / 병원 / 학교 / 개인)
- 상급·감독 기관:
- 자주 걸리는 법령·규정:
- 평가·감사 체계: (예: 경영평가, 감사, 이사회 보고)
- 승인 경로: (예: 부서장 전결 → 경영진 → 이사회)
- 주요 이해관계자:
- 예산 주기·고정 일정:
```

**5. 분량 조절** — "약식으로"(1~3매, 묻지 않고 바로) / "표준으로"(5~10매) / "정식으로"(15매 이내, 계획 승인 후 진행).

**6. 독립 검증 (레드팀)** — 같은 대화·같은 모델의 검토는 작성할 때의 논리와 오류를 공유합니다.
중요한 결정은 06 검토를 **다른 대화, 다른 모델**에서 받으세요.

| 순서 | 어디서 | 무엇을 |
|---|---|---|
| 1 | 원 대화 | 표준·정식 실행 시 「검증 경로」 질문에서 **레드팀**을 고른다 (약식은 "레드팀으로"라고 명시) |
| 2 | 원 대화 | 05 초안과 `[RT-PACKET]`이 나오고 멈춘다 → 응답 전체 복사 |
| 3 | **프로젝트 밖 새 대화** | 모델 선택에서 **작성과 다른 모델**을 고르고 "red-team으로"와 함께 붙여넣기 |
| 4 | 새 대화 | 사용 규칙 점검 → 5인 패널 → 판정서와 `[RT-RETURN]` |
| 5 | 원 대화 | `[RT-RETURN]`을 붙여넣으면 보완·수용을 반영해 보고서 확정 (판정은 뒤집지 않음) |

- 레드팀은 같은 대화이거나 작성 모델과 같은 모델이면 스스로 알아채고 "규칙 충족"을 고르지 못하게 합니다.
  규칙을 어기고 진행하면 **독립성 등급**(높음·중간·낮음)이 낮게 기록되고, 그 등급이 최종 보고서 Ⅴ장에 남습니다.
- 다른 사람이 쓴 보고서·기획안도 새 대화에 붙여넣고 "red-team으로"라고 하면 검증합니다. 문서를 고쳐 쓰지는 않습니다.
- 규칙과 블록 형식: [`shared/rt_protocol.md`](shared/rt_protocol.md)

**최신 동향 탐색** — 실행할 때마다 관련 신규 이론·연구·사례·제도를 인터넷에서 찾아 반영합니다.

- 검색어에는 내부 안건명·기관명·금액을 넣지 않습니다. 일반화해도 사안이 드러나면 검색하지 않습니다.
- 실제로 연 출처만 싣고, 건마다 **반영 / 참고 / 기각**을 판정해 붙임에 남깁니다. 새롭다는 이유만으로 채택하지 않습니다.
- 웹 검색이 꺼져 있으면 "탐색 불가"로 표시하고 진행합니다 (기억으로 지어내지 않음).
- 건너뛰려면 "탐색 생략", 더 넓게 찾으려면 "탐색 강화"라고 하세요.

**주의** — 개인정보·대외비는 가리고 올리세요. 산출물은 판단을 돕는 자료입니다.
내부 검토는 한 모델이 분석과 검증을 함께 하므로 독립 검증이 아닙니다 — 중요한 결정은 레드팀 경로를 쓰고,
최종 판단은 사람이 합니다.

## 자가개선 체계

스킬이 스스로 고치지 않습니다. **탐색 → 개선안 → 시험 → PR → 승인** 순서로만 바뀝니다.

| 구성 | 위치 | 역할 |
|---|---|---|
| 지식 원장 | `shared/knowledge_ledger.md` | 검증된 최신 동향을 쌓아 두고, 탐색이 먼저 읽어 중복 검색을 줄임 |
| 개선 후보 | 실행 결과 끝의 `○ 스킬 개선 후보` → `improvement_inbox.md` | 실행 중 발견한 "스킬보다 나은 방법"을 모음 |
| 시험 사례 | `evals/` | 변경 전후를 같은 사례로 비교해 "나빠지지 않았는지" 판정 |
| 월간 점검 | `MAINTENANCE.md` | 신규 방법 탐색 → 개선안 → 시험 → PR. main에 직접 올리지 않음 |

실행 결과에 `○ 스킬 개선 후보`가 나오면 `improvement_inbox.md`에 붙여 두세요. 월간 점검이 모아서 검토합니다.

## 왜 이 스킬인가

일반적인 채팅에서 Claude는 물어보면 바로 답을 냅니다. 이 스킬은 그 대신
컨설팅 방법론을 실제로 밟게 만듭니다.

- **5 Whys, MECE 로직트리, Kepner-Tregoe, Working Backwards, 가중
  평가매트릭스** 등 검증된 방법론을 단계별로 강제 적용
- 표준·정식 규모에서는 모든 결론 전에 **5인 반대자 패널**(제1원리
  사상가·순진한 아웃사이더·전방위 감사관·프론티어 크리에이터·전면
  반대론자)이 카드 한 장만 보고 서로 다른 각도에서 공격 → 방어 →
  판정 (약식 규모는 5축 약식 + 스틸맨 1회로 축약)
- 근거를 4등급([1급] 로컬 자료 ~ [4급] 보도자료)으로 관리하고,
  확정 사실과 가정을 항상 구분 표기
- 완료 조건·분량 상한·보고서 규모를 미리 정의해 무한정 늘어지지 않음

## 설치

> **Claude · ChatGPT · Gemini 통합 설치 안내** — [INSTALL.md](INSTALL.md). 친구에게는 이 주소 하나만 보내면 됩니다.

### Claude Code — 한 줄 설치 (권장)

```
/plugin marketplace add rjs-zzz/problem-solver
/plugin install problem-solver@problem-solver
```

설치한 뒤 새 버전을 받으려면 `/plugin` → **Marketplaces** 탭에서 `problem-solver`를 고르고
**Update marketplace**를 누릅니다. 같은 화면에서 **Enable auto-update**를 켜 두면 이후에는 자동으로 갱신됩니다
(외부 마켓플레이스는 자동 갱신이 기본으로 꺼져 있습니다).

#### Claude Code에서 달라지는 점

| 항목 | 웹·데스크톱 채팅 | Claude Code |
|---|---|---|
| 부르기 | "problem-solver로 …" | 같은 문장, 또는 `/problem-solver:problem-solver …` |
| 레드팀 | 새 대화를 열고 다른 모델로 붙여넣기 | **자동** — `red-team-reviewer` 하위 에이전트가 별도 문맥·다른 모델로 실행하고 `[RT-RETURN]`을 바로 반영 |
| 아무 문서나 레드팀 | 새 대화에 붙여넣기 | `/problem-solver:red-team-run outputs/보고서.md` (모델 지정: `--model sonnet`) |
| 산출물 | 응답 본문 | 작업 폴더 `outputs/YYYYMMDD_사안_종류_v1.md`에 저장, 응답에는 요지와 경로 |
| 다음 단계로 넘기기 | `[DATA-…]` 블록 복사·붙여넣기 | 붙여넣기 없음 — 다음 스킬이 `outputs/`에서 찾아 읽음 |

- 레드팀 자동 실행은 계획 단계(Phase A)에서 「레드팀 — 자동」을 고르면 작동합니다. 독립성 등급은
  `[RT-RETURN]`의 `run_mode: 독립 문맥 자동`과 함께 보고서 Ⅴ장에 남습니다.
- 하위 에이전트는 작성 대화·작업 폴더·CLAUDE.md를 보지 못합니다(R1·R2). 모델은 작성 모델과 다른 계열로
  지정됩니다(R3) — Opus로 썼으면 Sonnet, Sonnet으로 썼으면 Opus.
- 법령·통계 MCP 서버가 연결돼 있으면 스킬이 우선 활용합니다. 없으면 웹 검색으로 대신하고 그 사실을 적습니다.

### Claude.ai (웹/데스크톱/모바일) — 파일 하나만 올리기

1. [`dist/problem-solver.zip`](dist/problem-solver.zip)과 [`dist/red-team.zip`](dist/red-team.zip)을 내려받습니다.
   (레드팀 경로를 쓰려면 두 개 모두 필요합니다)
2. Skills 업로드 화면에서 각 zip을 그대로 올립니다 — 압축을 풀거나 다시 묶지 않습니다
   (메뉴 경로는 플랜·시점에 따라 다릅니다 — [공식 안내](https://support.claude.com/en/articles/12512180) 참조).
3. 새 대화에서 "problem-solver로 …"라고 요청합니다.

새 버전이 나오면 같은 zip을 다시 내려받아 올리면 됩니다. 마켓플레이스로 설치했다면
사용자 지정 → 플러그인 → 마켓플레이스 관리에서 "업데이트 확인"을 누릅니다. 변경 내용은 [CHANGELOG](CHANGELOG.md)에 있습니다.

### ChatGPT · Gemini — 같은 zip 사용

ChatGPT와 Gemini도 같은 SKILL.md 형식(Agent Skills 표준)을 읽습니다. 위 `dist/` zip을 그대로 씁니다.

| AI | 방법 |
|---|---|
| ChatGPT | Skills → Create → Upload from your computer에서 zip을 올립니다 |
| Gemini (웹 gemini.google.com · Mac 앱) | 설정 → 스킬 → 업로드. zip이 거부되면 압축을 풀어 스킬 폴더를 올립니다 |
| Gemini CLI | `gemini skills install https://github.com/rjs-zzz/problem-solver.git --path plugins/problem-solver/skills/problem-solver` (red-team은 경로 끝을 `red-team`으로) |

- 부를 때: ChatGPT는 `@스킬명`, Gemini는 `/스킬명`. 요청이 스킬 설명과 맞으면 알아서 고르기도 합니다.
- ChatGPT 데스크톱 앱은 Plugins → Add → Add a marketplace에 `rjs-zzz/problem-solver`를 넣는 방법도 있습니다
  (OpenAI 문서상 Claude 형식 마켓플레이스와 호환). 웹·모바일에서 보이는지는 플랜·시점에 따라 다릅니다.
- 다른 회사 AI로 문서를 옮길 때는 기관명·인명을 일반화하고 대외비 원문은 넣지 않습니다.
- 메뉴 이름과 지원 범위는 각 회사의 개편에 따라 바뀝니다 (2026-11 기준).
- red-team은 작성할 때와 다른 회사 AI에서 돌리면 R3(다른 모델)를 충족합니다.

### 설치 전에 결과물부터 보기

[`examples/00_입력점검-예시.md`](examples/00_입력점검-예시.md)
— 실행 전에 무엇을 묻고, 그 결과가 보고서 첫 장에 어떻게 남는지 보여줍니다.

[`examples/01_short-report_교육시스템-교체.md`](examples/01_short-report_교육시스템-교체.md)
— 약식 규모 실행 시 나오는 전체 산출물(재정의 → KT 진단 → 가중 매트릭스 →
가정 목록 → 비판적 검토)입니다.

## 구조

```
problem-solver/
├── .claude-plugin/marketplace.json
├── plugins/problem-solver/
│   ├── .claude-plugin/plugin.json
│   └── skills/problem-solver/
│       ├── SKILL.md                    # 워크플로우 총괄, 트리거 조건
│       ├── modules/
│       │   ├── 00_problem-framing.md   # 문제 정의 (5 Whys, 드러커식 재구성)
│       │   ├── 01_issue-structuring.md # MECE 로직트리 분해
│       │   ├── 02_root-cause.md        # Kepner-Tregoe 원인 진단
│       │   ├── 03_options.md           # Working Backwards 대안 도출
│       │   ├── 04_decision.md          # 가중 평가매트릭스 + 가역성 판별
│       │   ├── 05_reporting.md         # 민토 피라미드 결정 요청 보고서
│       │   └── 06_critic-review.md     # 5인 반대자 패널 비판적 검토
│       ├── references/rt_protocol.md   # 레드팀 규약 사본 (shared/ 원본)
│       └── templates/
│           ├── report_short.md         # 약식 보고 (1~3매)
│           ├── report_full.md          # 표준·정밀 보고 (5~15매)
│           ├── decision_matrix.md      # 가중 평가매트릭스 템플릿
│           ├── intake_sheet.md         # 입력 양식 (준비물 안내)
│           └── data_block.md           # [DATA-PS-OUTPUT] 인계 블록 스키마
│   ├── agents/red-team-reviewer.md     # Claude Code 전용 — 레드팀 독립 실행 하위 에이전트
│   ├── commands/red-team-run.md        # Claude Code 전용 — /problem-solver:red-team-run
│   ├── evals/                          # claude plugin eval 사례 (evals/cases.md에서 생성)
│   └── skills/red-team/
│       ├── SKILL.md                    # 사용 규칙 게이트 → 카드 → 06 패널 → [RT-RETURN]
│       ├── modules/06_critic-review.md # 06 사본 (tools/sync_common.py가 복사 — 직접 수정 금지)
│       └── references/rt_protocol.md
├── dist/problem-solver.zip · red-team.zip  # Claude.ai 업로드용 (tools/build_dist.py로 생성)
├── examples/                           # 산출물·입력 점검 예시
├── COMMON_CONTROLS.md                  # 공통 실행 통제 블록 원본
├── shared/                             # 공통 참조 원본 (각 스킬 references/로 복사)
│   ├── frontier_scan.md                # 최신 동향 탐색 공통 절차
│   └── rt_protocol.md                  # 레드팀 사용 규칙·블록 스키마
├── CLAUDE.md                           # 저장소 작업 규칙 (Claude Code로 고칠 때 자동으로 읽힘)
└── tools/                              # sync_common.py · build_dist.py · build_evals.py · validate.py
```

## 함께 쓰는 스킬 — Planning Suite

이 스킬은 **단일 결론**(선택·가부·원인 판정) 하나를 내는 데 특화돼
있습니다. 다루는 문제가 계획서 전체 수립이거나, 아래 표의 산출물
중 하나를 원한다면 별도 저장소 **`planning-suite`**(P1~P6 +
관제 스킬 `planning-orchestrator`, 총 7개 스킬 세트)를 쓰는 편이
맞습니다.

| 원하는 산출물 | 쓸 스킬 |
|---|---|
| 단일 결론 (A안 vs B안, 원인 진단, Go/No-Go) | **이 저장소 (problem-solver)** |
| 완성 문서의 독립 검증 (새 대화·다른 모델) | **이 저장소 (red-team)** — 계획서도 검증 가능 |
| 환경분석 (PEST·3C·VRIO·SWOT) | planning-suite의 `env-scanning-loop-p1` |
| 목표 체계 (미션·비전·OKR·KPI) | planning-suite의 `goal-setting-loop-p2` |
| 전략과제 발굴 (ERRC·포트폴리오) | planning-suite의 `strategy-option-loop-p3` |
| 타당성 검토 (예산·법률·자원 스크리닝) | planning-suite의 `feasibility-review-loop-p4` |
| 실행 로드맵 (RACI·마일스톤·KPI 전개) | planning-suite의 `roadmap-design-loop-p5` |
| 환류·모니터링 체계 | planning-suite의 `feedback-loop-p6` |
| 계획서 전체, 또는 2개 이상 단계 연속 필요 | planning-suite의 `planning-orchestrator` |

두 세트는 서로를 참조하도록 설계돼 있습니다 — 계획 문서 작업 중
"이 대안 중 뭘 골라야 하나" 같은 단일 판단이 필요해지면
planning-suite 쪽 스킬들이 problem-solver로 위임하고, 반대로 이
스킬이 "그건 계획 문서의 한 파트다"라고 판단하면 해당 Phase
스킬로 안내합니다. 두 세트를 함께 설치해두면 이 위임이 자동으로
작동합니다.
단일 결론은 `[DATA-PS-OUTPUT]` 블록(`templates/data_block.md`)으로 반환돼
planning-suite가 가정·Go/No-Go 조건·실행 개요를 재입력 없이 이어받습니다.

## 사용 시 참고

- **조직 맥락 커스터마이징**: 가장 쉬운 방법은 위 `[조직 프로필]` 블록을 대화에 붙여넣는
  것입니다. 조직 전체가 같은 기준을 쓰게 하려면 SKILL.md의 "상시 적용 맥락"과 각 모듈 끝의
  "조직 맥락 체크포인트"를 소속 조직의 법령명·이해관계자 맵·평가 체계로 고쳐 배포하세요.
- **자주 막히는 지점**
  - 스킬이 발동하지 않는다 → 요청 앞에 "problem-solver로"를 붙입니다.
  - 질문 없이 바로 받고 싶다 → "없이 진행" 또는 "약식으로"라고 합니다.
  - 결과가 너무 길다 → "약식으로"를 지정합니다.
  - 계획을 먼저 확인하고 싶다 → "정식으로"를 지정하면 계획 승인 후 진행합니다.
- **저장소를 고친 뒤**: `python tools/sync_common.py` → `python tools/build_dist.py` →
  `python tools/build_evals.py` → `python tools/validate.py` 순으로 실행하면 공통 블록·zip·시험 사례·버전·
  매니페스트가 맞는지 확인됩니다. GitHub Actions가 push·PR마다 같은 점검을 돌립니다.
- **영문판 스킬**: 이 저장소는 한국어 전용입니다(출력 형식도 한국
  정부 보고서 양식).

## 라이선스

MIT License — 자유롭게 사용, 수정, 배포, 상용 이용 가능합니다.
저작자 표시는 필수는 아니지만 있으면 감사하겠습니다.
