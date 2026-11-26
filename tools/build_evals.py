#!/usr/bin/env python3
"""evals/cases.md(사람이 읽는 시험 사례, 단일 원본)에서 `claude plugin eval`용 사례 폴더를 만든다.

사용법:  python tools/build_evals.py          (저장소 루트에서 실행)
         python tools/build_evals.py --check  (생성본이 최신인지 확인만, 다르면 종료코드 1)

규칙
  - 각 사례 머리 아래 `<!-- target: 플러그인/스킬 -->` 주석이 대상이다.
  - 「이어지는 입력」이 있거나 입력이 '같은 대화'·'작업 폴더'·'하위 작업'을 전제하면 자동 시험에서 뺀다 (수동 시험 — evals/README.md).
  - 출력: plugins/<플러그인>/evals/<사례id>/prompt.md + graders/{must,quality,skill-fired}.md
    must = ★ 항목(가중 2), quality = 나머지 항목, skill-fired = 대상 스킬이 실제로 불렸는지(기준선 비교에서 제외되는 지표).
  - 시험 실행은 파일 쓰기 도구를 주지 않는다 → 스킬이 산출물을 응답 본문에 내므로 채점기가 본문을 읽는다.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "evals", "cases.md")
MARK = "<!-- 생성 파일: evals/cases.md에서 tools/build_evals.py가 만든다. 직접 고치지 않는다. -->"

PROMPT_FM = """---
description: "{title}"
tags: [{tags}]
runs: 1
max_turns: 60
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, WebSearch, WebFetch]
---

"""


def parse(text):
    cases = []
    for blk in re.split(r"\n(?=## )", text):
        h = re.match(r"## ((?:[A-Z]+)-\d+)\s+(.*)", blk)
        if not h:
            continue
        cid, title = h.group(1), h.group(2).strip()
        tg = re.search(r"<!-- target: ([\w-]+)/([\w-]+) -->", blk)
        im = re.search(r"\*\*입력\*\*(.*?)\n((?:>.*\n?)+)", blk)
        crit = re.search(r"\*\*합격 기준\*\*\n((?:- .*\n?)+)", blk)
        manual = "**이어지는 입력**" in blk or bool(im and re.search(r"같은 대화|작업 폴더|하위 작업", im.group(1)))
        items = [l[2:].strip() for l in crit.group(1).splitlines()] if crit else []
        cases.append({
            "id": cid, "title": title,
            "plugin": tg.group(1) if tg else None, "skill": tg.group(2) if tg else None,
            "prompt": "\n".join(re.sub(r"^> ?", "", l) for l in im.group(2).rstrip("\n").splitlines()) if im else "",
            "must": [i[1:].strip() for i in items if i.startswith("★")],
            "quality": [i for i in items if not i.startswith("★")],
            "manual": bool(manual),
        })
    return cases


def render(c):
    files = {}
    files["prompt.md"] = PROMPT_FM.format(title=f"{c['id']} {c['title']}".replace('"', "'"),
                                          tags=", ".join([c["id"].split("-")[0].lower(), c["skill"]])) + c["prompt"] + "\n"
    rubric = lambda items: "\n".join(f"- {i}" for i in items)
    files["graders/must.md"] = (
        "---\ntype: llm\nweight: 2\n---\n\n"
        f"{MARK}\n\n아래 필수 조건을 **모두** 충족하면 PASS, 하나라도 어기면 FAIL이다. 서식 차이는 판정에 쓰지 않는다.\n\n"
        f"{rubric(c['must'])}\n")
    if c["quality"]:
        files["graders/quality.md"] = (
            "---\ntype: llm\nweight: 1\n---\n\n"
            f"{MARK}\n\n아래 조건 중 **3분의 2 이상**을 충족하면 PASS, 그보다 적으면 FAIL이다. 서식 차이는 판정에 쓰지 않는다.\n\n"
            f"{rubric(c['quality'])}\n")
    files["graders/skill-fired.md"] = (
        "---\ntype: tool_used\ntool: Skill\n"
        f"input_match: '\"skill\"\\s*:\\s*\"(?:[\\w-]+:)?{c['skill']}\"'\n---\n\n{MARK}\n")
    return files


def main():
    check = "--check" in sys.argv
    if not os.path.exists(SRC):
        print("evals/cases.md 없음 — 건너뜀")
        return
    cases = parse(open(SRC, encoding="utf-8").read())
    want, skipped, bad = {}, [], []
    for c in cases:
        if not c["plugin"]:
            bad.append(f"{c['id']}: target 주석 없음")
            continue
        if not os.path.isdir(os.path.join(ROOT, "plugins", c["plugin"])):
            bad.append(f"{c['id']}: 플러그인 없음 → {c['plugin']}")
            continue
        if c["manual"]:
            skipped.append(c["id"])
            continue
        if not c["prompt"] or not c["must"]:
            bad.append(f"{c['id']}: 입력 또는 ★ 기준이 없음")
            continue
        for rel, body in render(c).items():
            want[os.path.join("plugins", c["plugin"], "evals", c["id"].lower(), rel)] = body
    # 현재 생성본 (results/ 제외)
    have = {}
    for f in glob.glob(os.path.join(ROOT, "plugins", "*", "evals", "**", "*.md"), recursive=True):
        r = os.path.relpath(f, ROOT)
        if os.sep + "results" + os.sep in r or os.path.basename(r) == "README.md":
            continue
        have[r] = open(f, encoding="utf-8").read()
    stale = sorted(k for k in want if have.get(k) != want[k]) + sorted(k for k in have if k not in want)
    for b in bad:
        print("  [!]", b)
    if check:
        for s in stale:
            print("  [!] 낡음", s)
        if stale or bad:
            sys.exit(f"평가 사례 생성본이 최신이 아닙니다 — python tools/build_evals.py 실행 ({len(stale)}건)")
        print(f"평가 사례 — {len(want)}개 파일 최신, 수동 시험 {len(skipped)}건")
        return
    for k in sorted(have):
        if k not in want:
            os.remove(os.path.join(ROOT, k))
            print("  removed", k)
    for k, body in sorted(want.items()):
        p = os.path.join(ROOT, k)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if have.get(k) != body:
            open(p, "w", encoding="utf-8", newline="\n").write(body)
            print("  wrote  ", k)
    for d in sorted({os.path.join(ROOT, *k.split(os.sep)[:3]) for k in want}):
        readme = os.path.join(d, "README.md")
        text = ("# 자동 시험 사례 (claude plugin eval)\n\n"
                f"{MARK}\n\n원본은 저장소 루트의 `evals/cases.md`다. 실행 방법은 루트 `evals/README.md`.\n")
        if not os.path.exists(readme) or open(readme, encoding="utf-8").read() != text:
            open(readme, "w", encoding="utf-8", newline="\n").write(text)
    print(f"완료 — 자동 {len({k.split(os.sep)[3] for k in want})}건, 수동 {len(skipped)}건 ({', '.join(skipped) or '없음'})")
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
