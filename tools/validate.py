#!/usr/bin/env python3
"""배포 전 점검. 하나라도 실패하면 종료코드 1.

사용법:  python tools/validate.py            (저장소 루트에서 실행)

점검 항목
  1. SKILL.md frontmatter — name이 폴더명과 같은지, description 길이
  2. SKILL.md·모듈이 가리키는 하위 파일(modules/·templates/·references/·agents/)이 실재하는지
  3. 공통 실행 통제 블록이 COMMON_CONTROLS.md와 같은지
  4. 「입력 점검표」 절이 있는지
  5. 버전 일치 — plugin.json · marketplace.json · CHANGELOG 최신 항목
  6. dist/*.zip이 최신인지
  7. 민감정보 패턴(주민등록번호·이메일·전화번호)이 섞이지 않았는지
"""
import glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errs, warns = [], []


def rd(p):
    return open(p, encoding="utf-8").read()


def rel(p):
    return os.path.relpath(p, ROOT)


skills = sorted(glob.glob(os.path.join(ROOT, "plugins", "*", "skills", "*", "SKILL.md")))
if not skills:
    errs.append("SKILL.md를 찾지 못했습니다")

m = re.search(r"<!-- BEGIN COMMON -->\n(.*?)<!-- END COMMON -->", rd(os.path.join(ROOT, "COMMON_CONTROLS.md")), re.S)
common = m.group(1).rstrip() + "\n" if m else None
if common is None:
    errs.append("COMMON_CONTROLS.md에 BEGIN/END COMMON 마커가 없습니다")

for p in skills:
    d = os.path.dirname(p)
    name = os.path.basename(d)
    t = rd(p)
    fm = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", t)
    if not fm:
        errs.append(f"{rel(p)}: frontmatter 형식 오류 (name/description 2줄)")
        continue
    if fm.group(1).strip() != name:
        errs.append(f"{rel(p)}: name '{fm.group(1)}' ≠ 폴더명 '{name}'")
    dl = len(fm.group(2))
    if dl > 1024:
        errs.append(f"{rel(p)}: description {dl}자 — 1024자 초과")
    elif dl > 200:
        warns.append(f"{name}: description {dl}자 (공식 안내는 200자 이내 — 업로드가 거부되면 줄일 것)")
    if common and common not in t:
        errs.append(f"{rel(p)}: 공통 블록이 COMMON_CONTROLS.md와 다릅니다 — tools/sync_common.py 실행")
    if "## 입력 점검표" not in t:
        errs.append(f"{rel(p)}: 「입력 점검표」 절이 없습니다")
    for f in glob.glob(os.path.join(d, "**", "*.md"), recursive=True):
        for ref in set(re.findall(r"(?<![\w/.-])((?:modules|templates|references|agents)/[\w.\-]+\.md)", rd(f))):
            if not os.path.exists(os.path.join(d, ref)):
                errs.append(f"{rel(f)}: 가리키는 파일 없음 → {ref}")

# 버전
mk = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
ver = mk["metadata"]["version"]
for pl in mk["plugins"]:
    if pl["version"] != ver:
        errs.append(f"marketplace.json: {pl['name']} 버전 {pl['version']} ≠ {ver}")
    pj = os.path.join(ROOT, pl["source"], ".claude-plugin", "plugin.json")
    if not os.path.exists(pj):
        errs.append(f"plugin.json 없음: {rel(pj)}")
    elif json.load(open(pj, encoding="utf-8"))["version"] != ver:
        errs.append(f"{rel(pj)}: 버전 ≠ {ver}")
cl = re.search(r"^## \[(\d+\.\d+\.\d+)\]", rd(os.path.join(ROOT, "CHANGELOG.md")), re.M)
if not cl or cl.group(1) != ver:
    errs.append(f"CHANGELOG 최신 항목({cl.group(1) if cl else '없음'}) ≠ 버전 {ver}")

# dist
r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build_dist.py"), "--check"], capture_output=True, text=True)
if r.returncode != 0:
    errs.append("dist/*.zip이 최신이 아닙니다 — tools/build_dist.py 실행")

# 민감정보 패턴
PAT = {
    "주민등록번호": re.compile(r"\b\d{6}-[1-4]\d{6}\b"),
    "이메일": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    "전화번호": re.compile(r"\b01[016789]-\d{3,4}-\d{4}\b"),
}
for f in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True):
    if not os.path.isfile(f) or "/.git/" in f or f.endswith(".zip") or rel(f) == os.path.join("tools", "validate.py"):
        continue
    try:
        t = rd(f)
    except UnicodeDecodeError:
        continue
    for label, pat in PAT.items():
        for hit in pat.findall(t):
            errs.append(f"{rel(f)}: {label} 패턴 발견 → {hit}")

for w in warns:
    print("  [참고]", w)
for e in errs:
    print("  [실패]", e)
print(f"점검 — 스킬 {len(skills)}개, 버전 {ver}, 실패 {len(errs)}건, 참고 {len(warns)}건")
sys.exit(1 if errs else 0)
