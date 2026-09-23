# [DATA-PS-OUTPUT] 인계 블록 (Phase D 조건부 출력)

problem-solver의 단일 결론을 planning-suite(P1~P6·orchestrator)가 재해석 없이
승계하도록 만드는 구조화 블록. 출력 조건은 SKILL.md Phase D 참조.

## 작성 규칙
- 보고서 본문의 확정 내용만 옮긴다 — 본문에 없는 판단·수치 추가 금지
- 라벨([정량]/[추정]/[가정 An]/[확인 필요])은 본문 그대로 유지
- 06 판정관이 "회귀" 판정한 결론은 블록을 출력하지 않는다 (미확정 결론 인계 금지)
- 필드가 해당 없음이면 `null` — 필드 삭제 금지 (Q-Gate 스키마 검사 대상)

## 스키마

```
[DATA-PS-OUTPUT]
meta:
  decision_id: PS-YYYYMMDD-nn
  scale: 약식 | 표준 | 정식
  origin: 단독 | P1~P6 | orchestrator
  return_ref: 호출 Phase의 쟁점 키 (예: P3.conflicts#2) | null
question: 재정의 문제 (HMW 1문장)
verdict:
  type: 선택 | Go/No-Go | 원인판정
  result: 권고안 요지 1~2줄
  panel_ruling: 유지 | 조건부 유지(조건 명시)
reversibility: Two-way | 부분가역 | One-way
options:            # Do Nothing 포함, 전건
  - {id, 요지, 판정: 채택|기각, 사유 1줄}
control_tags:       # 채택안 핵심 조치별
  - {조치, 등급: 자체|내부승인|외부}
cost:
  mode: 정밀 | 개산 | 정성
  figures: 핵심 수치 (라벨 포함) | null
assumptions:
  - {id: An, 내용, 확신도: 상|중|하, 틀릴 경우 영향 1줄}
go_nogo_conditions:  # 06 E 미해결 항목 전건 포함
  - {조건, 조기 경보 신호, 판단 시점, 출처: E미해결|판정관}
exec_outline:        # 05 실행 계획 요지 — 가역 조치 선행 순서 유지
  - {단계, 조치, 담당(안), 선행 조건}
handoff:
  next_skill: roadmap-design-loop-p5 | feasibility-review-loop-p4 | 호출 Phase | null
  notes: 주의 논점 1~3개
[/DATA-PS-OUTPUT]
```

## 승계 측 처리 기준 (planning-suite)
- P3·P4: return_ref 쟁점의 판정으로 승계 (재판정 시 불일치 사유 기록)
- P5: exec_outline → WBS 초안, go_nogo_conditions → 선결 과업·Go/No-Go 마일스톤,
  control_tags의 [외부] 조치 → 병행 트랙(성사 확인 시점 마일스톤화)
- 전 Phase: assumptions → 가정 누계에 합산 (id 앞에 PS- 접두)
