# 스킬 설치 안내 — Claude · ChatGPT · Gemini

업무 판단·기획 스킬 10종입니다. 같은 스킬 파일(SKILL.md, Agent Skills 표준)을 세 AI가 함께 읽습니다.
쓰는 AI를 골라 따라 하세요.

**[Claude](#claude) · [ChatGPT](#chatgpt) · [Gemini](#gemini) · [스킬 목록](#스킬-목록) · [쓰는 요령](#쓰는-요령)**

> **카카오톡에서 열었다면** 내려받기가 막힐 수 있습니다. 메뉴(⋮)에서 「다른 브라우저로 열기」를 누르세요.
> 파일 업로드는 **PC**에서 하는 것이 가장 확실합니다.

## 스킬 목록

처음이면 **problem-solver 하나**로 시작하세요. 계획서를 쓸 때 필요한 단계만 더 받습니다.

### 문제해결 세트

| 스킬 | 하는 일 | 내려받기 |
|---|---|---|
| problem-solver | 선택·가부·원인 판정을 결재용 검토 보고서로 | [zip](https://github.com/rjs-zzz/problem-solver/raw/main/dist/problem-solver.zip) |
| red-team | 완성된 문서를 새 대화·다른 AI에서 독립적으로 공격·판정 | [zip](https://github.com/rjs-zzz/problem-solver/raw/main/dist/red-team.zip) |

### 기획 세트

| 스킬 | 하는 일 | 내려받기 |
|---|---|---|
| env-scanning-loop-p1 | P1 환경분석 (PEST·3C·VRIO·SWOT) | [zip](https://github.com/rjs-zzz/planning-suite/raw/main/dist/env-scanning-loop-p1.zip) |
| goal-setting-loop-p2 | P2 미션·비전·OKR·KPI | [zip](https://github.com/rjs-zzz/planning-suite/raw/main/dist/goal-setting-loop-p2.zip) |
| strategy-option-loop-p3 | P3 전략과제 발굴·우선순위 | [zip](https://github.com/rjs-zzz/planning-suite/raw/main/dist/strategy-option-loop-p3.zip) |
| feasibility-review-loop-p4 | P4 예산·법률·자원 타당성 검토 | [zip](https://github.com/rjs-zzz/planning-suite/raw/main/dist/feasibility-review-loop-p4.zip) |
| roadmap-design-loop-p5 | P5 로드맵·역할분담·KPI 전개 | [zip](https://github.com/rjs-zzz/planning-suite/raw/main/dist/roadmap-design-loop-p5.zip) |
| feedback-loop-p6 | P6 모니터링·환류 | [zip](https://github.com/rjs-zzz/planning-suite/raw/main/dist/feedback-loop-p6.zip) |
| planning-orchestrator | P1~P6 연결·정합 검증 (계획서 전체를 쓸 때만) | [zip](https://github.com/rjs-zzz/planning-suite/raw/main/dist/planning-orchestrator.zip) |
| visual-presenter | 결과를 표·도식·차트·한 장 요약으로 | [zip](https://github.com/rjs-zzz/planning-suite/raw/main/dist/visual-presenter.zip) |

## Claude

### 주소로 설치 (권장)

1. 사용자 지정 → 플러그인 → 추가 → 마켓플레이스 추가 → 저장소에서 추가
2. `rjs-zzz/problem-solver` 입력. 기획 세트도 쓰려면 같은 방법으로 `rjs-zzz/planning-suite` 추가
3. 목록에서 필요한 플러그인을 설치

새 버전은 마켓플레이스 관리 화면의 「업데이트 확인」으로 받습니다.

Claude Code에서는 아래 두 줄입니다.

```
/plugin marketplace add rjs-zzz/problem-solver
/plugin install problem-solver@problem-solver
```

### 파일로 설치

스킬 업로드 화면에서 위 [스킬 목록](#스킬-목록)의 zip을 **그대로** 올립니다. 압축을 풀지 않습니다.

## ChatGPT

### 파일로 설치 (권장)

1. 스킬 → 만들기(Create) → 컴퓨터에서 업로드(Upload from your computer)
2. 위 [스킬 목록](#스킬-목록)의 zip을 올립니다. 거부되면 압축을 풀어 나온 폴더를 올립니다.
3. 채팅에서 `@problem-solver`처럼 이름을 불러 씁니다. 요청이 스킬 설명과 맞으면 알아서 고르기도 합니다.

### 주소로 설치 (데스크톱 앱)

플러그인 → 추가 → 마켓플레이스 추가(Add a marketplace)에 `rjs-zzz/problem-solver`를 넣습니다.
화면에 따라 이 메뉴가 없을 수 있습니다. 그때는 파일로 설치하세요.

> 「사용자 지정 MCP 서버 추가」는 다른 기능입니다. 여기에 주소를 넣으면 설치되지 않습니다.

## Gemini

### 웹(gemini.google.com) · Mac 앱

1. zip을 내려받아 압축을 풉니다. 스킬 이름의 폴더가 나옵니다 (안에 SKILL.md가 있음).
2. 설정 → 스킬 → 업로드에서 그 **폴더**를 올립니다.
   SKILL.md 한 파일만 올리면 딸린 참고 파일(modules·templates 등)이 빠집니다.
3. 채팅에서 `/problem-solver`처럼 불러 씁니다. 올린 스킬은 휴대폰 앱에서도 쓸 수 있습니다.

### Gemini CLI

```
gemini skills install https://github.com/rjs-zzz/problem-solver.git --path plugins/problem-solver/skills/problem-solver
gemini skills install https://github.com/rjs-zzz/planning-suite.git --path plugins/goal-setting-loop-p2/skills/goal-setting-loop-p2
```

다른 스킬은 경로의 이름 두 곳을 바꿉니다 (red-team은 `plugins/problem-solver/skills/red-team`).

## 쓰는 요령

- **기획 단계 잇기**: 앞 단계 결과 끝의 `[DATA-PN-OUTPUT]` 블록을 복사해 다음 단계 대화에 붙여 넣습니다. 어느 AI에서나 같습니다.
- **red-team**: 작성한 대화가 아닌 **새 대화**에서, 가능하면 작성할 때와 **다른 AI**로 돌립니다.
- **민감정보**: 개인정보·대외비는 가리고 넣습니다.
- **새 버전**: 파일로 설치했다면 같은 zip을 다시 올립니다. 바뀐 내용은 [problem-solver](https://github.com/rjs-zzz/problem-solver/blob/main/CHANGELOG.md) · [planning-suite](https://github.com/rjs-zzz/planning-suite/blob/main/CHANGELOG.md) 변경 이력에 있습니다.
- 메뉴 이름과 지원 범위는 각 회사의 개편에 따라 바뀝니다 (2026-11 기준). 막히면 [Issue](https://github.com/rjs-zzz/problem-solver/issues)로 알려 주세요.

---

저장소: [rjs-zzz/problem-solver](https://github.com/rjs-zzz/problem-solver) · [rjs-zzz/planning-suite](https://github.com/rjs-zzz/planning-suite) · MIT 라이선스
