#!/usr/bin/env python3
"""각 스킬 폴더를 Claude.ai 업로드용 zip으로 묶어 dist/에 둔다.

사용법:  python tools/build_dist.py          (저장소 루트에서 실행)
         python tools/build_dist.py --check  (dist가 최신인지 확인만, 다르면 종료코드 1)

zip 구조: <스킬명>.zip → <스킬명>/SKILL.md ... (스킬 폴더가 zip의 최상위)
같은 내용이면 항상 같은 바이트가 나오도록 시각·순서를 고정한다.
"""
import glob, io, os, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
FIXED = (2020, 1, 1, 0, 0, 0)


def build(skill_dir):
    name = os.path.basename(skill_dir)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        files = []
        for base, dirs, fs in os.walk(skill_dir):
            dirs.sort()
            for f in sorted(fs):
                if f.startswith(".") or f.endswith(".pyc"):
                    continue
                files.append(os.path.join(base, f))
        for p in sorted(files):
            arc = name + "/" + os.path.relpath(p, skill_dir).replace(os.sep, "/")
            zi = zipfile.ZipInfo(arc, FIXED)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(p, "rb").read())
    return name, buf.getvalue()


def main():
    check = "--check" in sys.argv
    skills = sorted(glob.glob(os.path.join(ROOT, "plugins", "*", "skills", "*")))
    skills = [s for s in skills if os.path.isfile(os.path.join(s, "SKILL.md"))]
    stale = 0
    os.makedirs(DIST, exist_ok=True)
    for s in skills:
        name, data = build(s)
        out = os.path.join(DIST, name + ".zip")
        cur = open(out, "rb").read() if os.path.exists(out) else None
        if cur == data:
            print(f"  ok       dist/{name}.zip")
            continue
        stale += 1
        if check:
            print(f"  [!] 낡음  dist/{name}.zip")
        else:
            open(out, "wb").write(data)
            print(f"  built    dist/{name}.zip ({len(data):,} bytes)")
    if check and stale:
        sys.exit(f"dist가 최신이 아닙니다 — python tools/build_dist.py 실행 필요 ({stale}건)")
    print(f"완료 — 스킬 {len(skills)}개")


if __name__ == "__main__":
    main()
