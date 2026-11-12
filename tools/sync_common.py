#!/usr/bin/env python3
"""COMMON_CONTROLS.md의 공통 블록을 모든 SKILL.md에 반영하고, shared/*.md를 각 스킬 references/에 복사한다.

사용법:  python tools/sync_common.py        (저장소 루트에서 실행)
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "COMMON_CONTROLS.md")

m = re.search(r"<!-- BEGIN COMMON -->\n(.*?)<!-- END COMMON -->",
              open(SRC, encoding="utf-8").read(), re.S)
if not m:
    sys.exit("COMMON_CONTROLS.md에 BEGIN/END COMMON 마커가 없습니다.")
block = m.group(1).rstrip() + "\n"

targets = glob.glob(os.path.join(ROOT, "plugins", "*", "skills", "*", "SKILL.md"))
pat = re.compile(r"## 실행 통제 \(공통\).*?<!-- 이 블록은 COMMON_CONTROLS\.md에서 생성됨.*?-->\n", re.S)

changed = 0
for p in sorted(targets):
    t = open(p, encoding="utf-8").read()
    if not pat.search(t):
        print(f"  [!] 공통 블록 미발견: {p}")
        continue
    new = pat.sub(block, t)
    if new != t:
        open(p, "w", encoding="utf-8").write(new)
        changed += 1
        print(f"  updated: {os.path.relpath(p, ROOT)}")
print(f"완료 — 대상 {len(targets)}개 중 {changed}개 갱신")

# shared/*.md 를 각 스킬의 references/ 로 복사한다 (스킬마다 단독 배포되므로 사본이 필요).
import shutil
shared = sorted(glob.glob(os.path.join(ROOT, "shared", "*.md")))
copied = 0
for p in sorted(targets):
    ref = os.path.join(os.path.dirname(p), "references")
    os.makedirs(ref, exist_ok=True)
    for s in shared:
        dst = os.path.join(ref, os.path.basename(s))
        src_t = open(s, encoding="utf-8").read()
        if not os.path.exists(dst) or open(dst, encoding="utf-8").read() != src_t:
            shutil.copy(s, dst)
            copied += 1
            print(f"  copied: {os.path.relpath(dst, ROOT)}")
print(f"공통 참조 파일 — 원본 {len(shared)}개, 갱신 {copied}건")
