# Problem-Solver

[English README](README.en.md)

업무 문제를 **6단계(정의 → 구조화 → 진단 → 대안 → 결정 → 보고)**로 해결하고,
최종 결론 전 **5인 반대자 패널**의 비판적 검토를 자동으로 거치는
구조적 문제해결 Claude Skill입니다.

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

### Claude Code — 한 줄 설치 (권장)

```
/plugin marketplace add rjs-zzz/problem-solver
/plugin install problem-solver@problem-solver
```

### Claude.ai (웹/데스크톱/모바일)

`plugins/problem-solver/skills/problem-solver/` 폴더를 zip으로 압축해
Skills 업로드 화면에서 올리면 됩니다(메뉴 경로는 플랜·시점에 따라 다릅니다 —
[공식 안내](https://support.claude.com/en/articles/12512180) 참조).

### 설치 전에 결과물부터 보기

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
│       └── templates/
│           ├── report_short.md         # 약식 보고 (1~3매)
│           ├── report_full.md          # 표준·정밀 보고 (5~15매)
│           ├── decision_matrix.md      # 가중 평가매트릭스 템플릿
│           └── data_block.md           # [DATA-PS-OUTPUT] 인계 블록 스키마
├── examples/                           # 실제 산출물 예시
├── COMMON_CONTROLS.md
└── tools/sync_common.py
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

- **조직 맥락 커스터마이징**: SKILL.md와 각 모듈 끝의 "조직 맥락
  체크포인트" 섹션은 범용으로 작성돼 있습니다. 소속 조직(공공기관,
  기업, 병원 등)에 맞는 법령명·이해관계자 맵·평가 체계로 직접
  채워 넣으면 정확도가 크게 올라갑니다.
- **영문판 스킬**: 이 저장소는 한국어 전용입니다(출력 형식도 한국
  정부 보고서 양식).

## 라이선스

MIT License — 자유롭게 사용, 수정, 배포, 상용 이용 가능합니다.
저작자 표시는 필수는 아니지만 있으면 감사하겠습니다.
