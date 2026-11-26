#!/usr/bin/env python3
"""배포 전 점검. 하나라도 실패하면 종료코드 1.

사용법:  python tools/validate.py            (저장소 루트에서 실행 — Windows·macOS·Linux 공통)

점검 항목
  1. SKILL.md frontmatter — name이 폴더명과 같은지, description 길이
  2. SKILL.md·모듈이 가리키는 하위 파일(modules/·templates/·references/·agents/)이 실재하는지
  3. 공통 실행 통제 블록이 COMMON_CONTROLS.md와 같은지
  4. 「입력 점검표」·「최신 동향 탐색」 절이 있는지, references/ 사본이 shared/ 원본과 같은지,
     스킬 간 미러 사본(tools/sync_common.py의 MIRRORS)이 원본과 같은지
  5. 버전 일치 — plugin.json · marketplace.json · CHANGELOG 최신 항목, 플러그인 의존성이 같은 마켓플레이스에 있는지
  6. dist/*.zip, 플러그인 평가 사례(plugins/*/evals)가 최신인지
  7. 민감정보 패턴(주민등록번호·이메일·전화번호)이 섞이지 않았는지
  8. 다른 AI 호환 — name 형식(Agent Skills 표준), 스킬 본문에 특정 AI 환경 이름이 없는지
  9. 플러그인 전용 구성요소(agents/·commands/) — frontmatter, ${CLAUDE_PLUGIN_ROOT} 경로 실재
 10. 줄바꿈 — 텍스트 파일에 CRLF가 없는지 (Windows 체크아웃 대비, .gitattributes와 짝)
 11. claude CLI가 있으면 `claude plugin validate`로 마켓플레이스·플러그인 매니페스트 점검
"""
import glob, json, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errs, warns = [], []


def rd(p):
    return open(p, encoding="utf-8").read()


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def parts(p):
    return rel(p).split("/")


skills = sorted(glob.glob(os.path.join(ROOT, "plugins", "*", "skills", "*", "SKILL.md")))
if not skills:
    errs.append("SKILL.md를 찾지 못했습니다")

m = re.search(r"<!-- BEGIN COMMON -->\n(.*?)<!-- END COMMON -->", rd(os.path.join(ROOT, "COMMON_CONTROLS.md")), re.S)
common = m.group(1).rstrip() + "\n" if m else None
if common is None:
    errs.append("COMMON_CONTROLS.md에 BEGIN/END COMMON 마커가 없습니다")

# 1~4. 스킬
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
    if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        errs.append(f"{rel(p)}: name '{name}' — 소문자·숫자·하이픈, 64자 이하 (Agent Skills 표준)")
    if common and common not in t:
        errs.append(f"{rel(p)}: 공통 블록이 COMMON_CONTROLS.md와 다릅니다 — tools/sync_common.py 실행")
    if "## 입력 점검표" not in t:
        errs.append(f"{rel(p)}: 「입력 점검표」 절이 없습니다")
    if "## 최신 동향 탐색" not in t:
        errs.append(f"{rel(p)}: 「최신 동향 탐색」 절이 없습니다")
    for s in glob.glob(os.path.join(ROOT, "shared", "*.md")):
        dst = os.path.join(d, "references", os.path.basename(s))
        if not os.path.exists(dst) or rd(dst) != rd(s):
            errs.append(f"{rel(dst)}: shared/ 원본과 다릅니다 — tools/sync_common.py 실행")
    for f in glob.glob(os.path.join(d, "**", "*.md"), recursive=True):
        for ref in set(re.findall(r"(?<![\w/.-])((?:modules|templates|references|agents)/[\w.\-]+\.md)", rd(f))):
            if not os.path.exists(os.path.join(d, ref)):
                errs.append(f"{rel(f)}: 가리키는 파일 없음 → {ref}")

# 스킬 간 미러
_src = rd(os.path.join(ROOT, "tools", "sync_common.py"))
_mm = re.search(r"MIRRORS = \[(.*?)\n\]", _src, re.S)
for a, b in re.findall(r'\("([^"]+)",\s*"([^"]+)"\)', _mm.group(1) if _mm else ""):
    pa, pb = os.path.join(ROOT, a), os.path.join(ROOT, b)
    if not os.path.exists(pa):
        errs.append(f"미러 원본 없음: {a}")
    elif not os.path.exists(pb) or rd(pa) != rd(pb):
        errs.append(f"{b}: 원본({a})과 다릅니다 — tools/sync_common.py 실행")

# 5. 버전·의존성
mk = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
ver = mk["metadata"]["version"]
names = {pl["name"] for pl in mk["plugins"]}
for pl in mk["plugins"]:
    if pl["version"] != ver:
        errs.append(f"marketplace.json: {pl['name']} 버전 {pl['version']} ≠ {ver}")
    pj = os.path.join(ROOT, pl["source"], ".claude-plugin", "plugin.json")
    if not os.path.exists(pj):
        errs.append(f"plugin.json 없음: {rel(pj)}")
        continue
    pd = json.load(open(pj, encoding="utf-8"))
    if pd.get("version") != ver:
        errs.append(f"{rel(pj)}: 버전 ≠ {ver}")
    if pd.get("name") != pl["name"]:
        errs.append(f"{rel(pj)}: name '{pd.get('name')}' ≠ 마켓플레이스 항목 '{pl['name']}'")
    for dep in pd.get("dependencies", []):
        dn = dep if isinstance(dep, str) else dep.get("name")
        if "@" not in dn and dn not in names:
            errs.append(f"{rel(pj)}: 의존 플러그인 '{dn}'이 이 마켓플레이스에 없습니다")
cl = re.search(r"^## \[(\d+\.\d+\.\d+)\]", rd(os.path.join(ROOT, "CHANGELOG.md")), re.M)
if not cl or cl.group(1) != ver:
    errs.append(f"CHANGELOG 최신 항목({cl.group(1) if cl else '없음'}) ≠ 버전 {ver}")

# 6. 생성물 최신 여부
for tool, msg in (("build_dist.py", "dist/*.zip"), ("build_evals.py", "plugins/*/evals")):
    tp = os.path.join(ROOT, "tools", tool)
    if not os.path.exists(tp):
        continue
    r = subprocess.run([sys.executable, tp, "--check"], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        errs.append(f"{msg}이 최신이 아닙니다 — tools/{tool} 실행\n{r.stdout.strip()}")

# 8. 다른 AI 호환 — 스킬 본문은 환경 이름이 아니라 능력으로 쓴다 ("병렬 실행 도구가 있는 환경")
# 같은 SKILL.md를 Claude·ChatGPT·Gemini가 함께 읽기 때문. 출처 인용이 담기는 지식 원장은 제외.
# 플러그인 전용 구성요소(agents/·commands/·evals/)는 스킬 업로드 묶음(dist)에 들어가지 않으므로 제외.
ENV = re.compile(r"Claude\.ai|Claude Code|Cowork|Task 도구|Task 서브에이전트|ChatGPT|Gemini|Codex")
for f in glob.glob(os.path.join(ROOT, "plugins", "*", "skills", "**", "*.md"), recursive=True):
    if os.path.basename(f) == "knowledge_ledger.md":
        continue
    for i, line in enumerate(rd(f).splitlines(), 1):
        for hit in sorted(set(ENV.findall(line))):
            errs.append(f"{rel(f)}:{i}: 특정 AI 환경 이름 '{hit}' — 능력으로 쓸 것 (예: 병렬 실행 도구가 있는 환경)")

# 9. 플러그인 전용 구성요소
AGENT_KEYS = {"name", "description", "model", "effort", "maxTurns", "tools", "disallowedTools", "skills", "memory",
              "background", "omitClaudeMd", "isolation", "color", "experimental"}
for f in sorted(glob.glob(os.path.join(ROOT, "plugins", "*", "agents", "*.md")) +
                glob.glob(os.path.join(ROOT, "plugins", "*", "commands", "*.md"))):
    t = rd(f)
    fm = re.match(r"---\n(.*?)\n---\n", t, re.S)
    if not fm:
        errs.append(f"{rel(f)}: frontmatter 없음")
        continue
    keys = re.findall(r"^([\w-]+):", fm.group(1), re.M)
    if "description" not in keys:
        errs.append(f"{rel(f)}: description 없음")
    if parts(f)[2] == "agents":
        for k in keys:
            if k not in AGENT_KEYS:
                errs.append(f"{rel(f)}: 플러그인 에이전트에서 지원하지 않는 필드 '{k}'")
    plug = os.path.join(ROOT, *parts(f)[:2])
    for ref in set(re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([\w./-]+[\w])", t)):
        if not os.path.exists(os.path.join(plug, ref)):
            errs.append(f"{rel(f)}: 가리키는 파일 없음 → ${{CLAUDE_PLUGIN_ROOT}}/{ref}")

# 7·10. 민감정보 패턴, 줄바꿈
PAT = {
    "주민등록번호": re.compile(r"\b\d{6}-[1-4]\d{6}\b"),
    "이메일": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    "전화번호": re.compile(r"\b01[016789]-\d{3,4}-\d{4}\b"),
}
SKIP_DIRS = {".git", "node_modules", "__pycache__", "outputs"}
for base, dirs, files in os.walk(ROOT):
    dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not (x == "results" and os.path.basename(base) == "evals")]
    for fn in files:
        f = os.path.join(base, fn)
        if fn.endswith((".zip", ".png", ".jpg")) or rel(f) == "tools/validate.py":
            continue
        try:
            raw = open(f, "rb").read()
            t = raw.decode("utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if b"\r\n" in raw:
            errs.append(f"{rel(f)}: CRLF 줄바꿈 — LF로 저장할 것 (.gitattributes 적용 후 `git add --renormalize .`)")
        for label, pat in PAT.items():
            for hit in pat.findall(t):
                errs.append(f"{rel(f)}: {label} 패턴 발견 → {hit}")

# 11. Claude Code 매니페스트 점검 (CLI가 있을 때만)
claude = shutil.which("claude")
if claude:
    targets = ["."] + [pl["source"] for pl in mk["plugins"]]
    for tg in targets:
        r = subprocess.run([claude, "plugin", "validate", tg], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0 or "Validation failed" in r.stdout:
            errs.append(f"claude plugin validate {tg} 실패:\n{(r.stdout + r.stderr).strip()[-800:]}")
else:
    warns.append("claude CLI 없음 — 매니페스트 점검(claude plugin validate)을 건너뜀")

for w in warns:
    print("  [참고]", w)
for e in errs:
    print("  [실패]", e)
print(f"점검 — 스킬 {len(skills)}개, 버전 {ver}, 실패 {len(errs)}건, 참고 {len(warns)}건")
sys.exit(1 if errs else 0)
