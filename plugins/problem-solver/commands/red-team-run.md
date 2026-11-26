---
description: 문서 하나를 별도 문맥·다른 모델의 레드팀 하위 작업으로 독립 검증한다 (새 대화를 열 필요 없음)
argument-hint: "[검토할 파일 경로] [--model sonnet|opus|haiku|fable]"
disable-model-invocation: true
---

완성 문서를 **독립 레드팀**에 넘겨 판정을 받는다. 규칙은 `${CLAUDE_PLUGIN_ROOT}/skills/problem-solver/references/rt_protocol.md` 7절이다.

인자: `$ARGUMENTS`

## 1. 대상 확보

- 인자에 파일 경로가 있으면 그 파일을 읽는다 (.md·.txt 원문. 다른 형식이면 텍스트로 옮긴 뒤 진행).
- 경로가 없으면 이 대화의 가장 최근 `[RT-PACKET]`과 그 바로 위 초안을 대상으로 한다.
- 둘 다 없으면 `outputs/`에서 가장 최근 보고서 파일을 제안하고 멈춘다. 추측으로 고르지 않는다.
- 주민등록번호·환자정보·계좌번호 등이 보이면 가린 사본을 넘기고 그 사실을 1줄 알린다.

## 2. 모델 지정 (R3)

- 인자에 `--model`이 있으면 그것을 쓴다.
- 없으면 지금 응답하는 모델과 **다른 계열**을 고른다: Opus → `sonnet`, Sonnet → `opus`, Haiku → `sonnet`, Fable·Mythos → `opus`.
- 같은 계열밖에 쓸 수 없으면 그대로 진행하되 R3 미충족(독립성 '중간')을 미리 1줄 알린다.

## 3. 하위 작업 실행

`problem-solver:red-team-reviewer` 에이전트를 2의 모델로 띄운다. 넘기는 프롬프트는 **아래 머리말 + 대상 원문뿐**이다.
작성 의도·설명·요약·변호를 덧붙이지 않는다 (덧붙이면 R1이 무너진다).

```
[RT-DISPATCH]
run_mode: 독립 문맥 자동
author_model: (대상 문서를 작성한 모델 — 패킷의 author_model, 모르면 "확인 불가")
reviewer_model_requested: (2에서 고른 모델)
round: 1
access: 작업 폴더·프로젝트 자료·과거 대화를 열지 않는다
[/RT-DISPATCH]

(대상 원문 그대로)
```

## 4. 결과 처리

- 판정서와 `[RT-RETURN]`을 `outputs/YYYYMMDD_<사안>_레드팀판정_v1.md`로 저장한다 (같은 이름이 있으면 `_v2`).
- 응답에는 판정 한 줄, 독립성 등급, 치명·중대 지적 수, 저장 경로만 낸다.
- 이 대화가 대상 문서를 쓴 problem-solver 대화면, 이어서 problem-solver의 「레드팀 반송 접수」로 반영한다 — 판정을 뒤집지 않는다.
- Round 2가 필요하면 보완본·반영표·Round 1 `[RT-RETURN]`을 넣어 `round: 2`로 다시 실행한다 (Round 3은 없다).
