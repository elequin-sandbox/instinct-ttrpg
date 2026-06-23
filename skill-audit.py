#!/usr/bin/env python3
"""
skill-audit.py - Single-Source-of-Truth auditor for the Instinct RPG project.

Passes:
  1. DRIFT     - does every skill in skill-sources/ match the INSTALLED skill?
  2. STRUCTURE - is every skill a folder containing SKILL.md (no flat singletons)?
  3. SPRAWL    - are there stray skill copies anywhere outside skill-sources/?
  4. REFERENCE - do references/ paths named in a SKILL.md exist?
  5. DOCTRINE  - is design/INDEX.md wired into CLAUDE.md and does the manifest match files?

Run from the repo root:  python skill-audit.py
Exit code 0 = clean, 1 = violations found.

Installed-skills dir is auto-detected (sibling `skills/` mount). Override with:
  INSTINCT_SKILLS_DIR=/path/to/installed/skills  python skill-audit.py
"""
import os, sys, hashlib, re

REPO = os.path.dirname(os.path.abspath(__file__))
SOURCES = os.path.join(REPO, "skill-sources")

def find_installed_dir():
    env = os.environ.get("INSTINCT_SKILLS_DIR")
    if env and os.path.isdir(env):
        return env
    cand = os.path.join(os.path.dirname(REPO), "skills")
    if os.path.isdir(cand):
        return cand
    return None

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def list_skill_dirs(root):
    if not root or not os.path.isdir(root):
        return []
    return sorted(d for d in os.listdir(root)
                  if os.path.isdir(os.path.join(root, d)) and d.startswith("at-"))

def main():
    installed = find_installed_dir()
    drift, structure, sprawl, refs, doctrine = [], [], [], [], []

    # ---- STRUCTURE ----
    if os.path.isdir(SOURCES):
        for name in sorted(os.listdir(SOURCES)):
            p = os.path.join(SOURCES, name)
            if name == "README.md":
                continue
            if os.path.isfile(p) and name.endswith(".md"):
                structure.append(f"flat singleton in skill-sources/: {name} (should be a folder with SKILL.md)")
            elif os.path.isdir(p) and not os.path.isfile(os.path.join(p, "SKILL.md")):
                structure.append(f"skill folder missing SKILL.md: skill-sources/{name}/")
    else:
        structure.append("skill-sources/ folder not found")

    # ---- DRIFT ----
    if installed:
        src_skills = list_skill_dirs(SOURCES)
        inst_skills = list_skill_dirs(installed)
        for name in src_skills:
            s = os.path.join(SOURCES, name, "SKILL.md")
            i = os.path.join(installed, name, "SKILL.md")
            if not os.path.isfile(i):
                drift.append(f"{name}: in skill-sources/ but NOT installed (install the .skill)")
            elif sha(s) != sha(i):
                drift.append(f"{name}: skill-sources/ differs from installed (reinstall the repackaged .skill)")
        for name in inst_skills:
            if name not in src_skills:
                drift.append(f"{name}: installed but missing from skill-sources/ (add it to the mirror)")
    else:
        drift.append("installed skills dir not found - set INSTINCT_SKILLS_DIR to enable drift check")

    # ---- SPRAWL ----
    for dirpath, dirnames, filenames in os.walk(REPO):
        if any(seg in dirpath for seg in (os.sep + ".git", os.sep + "skill-sources", os.sep + ".claude")):
            continue
        rel = os.path.relpath(dirpath, REPO)
        for fn in filenames:
            low = fn.lower()
            if low == "skill.md":
                sprawl.append(f"stray SKILL.md outside skill-sources/: {os.path.join(rel, fn)}")
            elif low.endswith(".skill"):
                sprawl.append(f"packaged .skill committed in repo: {os.path.join(rel, fn)} (build to outputs, don't commit)")
            elif re.search(r"-updated\.md$", fn, re.IGNORECASE) and fn.startswith("at-"):
                sprawl.append(f"stray skill copy: {os.path.join(rel, fn)}")
        for dn in dirnames:
            if dn.startswith("at-") and rel == ".":
                sprawl.append(f"stray skill folder at repo root: {dn}/ (skills live in skill-sources/)")

    # ---- REFERENCE ----
    if os.path.isdir(SOURCES):
        for name in list_skill_dirs(SOURCES):
            skill_md = os.path.join(SOURCES, name, "SKILL.md")
            if not os.path.isfile(skill_md):
                continue
            text = open(skill_md, encoding="utf-8", errors="ignore").read()
            for m in re.findall(r"references/[A-Za-z0-9_\-./]+\.\w+", text):
                if not os.path.isfile(os.path.join(SOURCES, name, m)):
                    refs.append(f"{name}: SKILL.md references missing file {m}")

    # ---- DOCTRINE / MANIFEST ----
    design_dir = os.path.join(REPO, "design")
    index = os.path.join(design_dir, "INDEX.md")
    claude = os.path.join(REPO, "CLAUDE.md")
    if not os.path.isdir(design_dir):
        doctrine.append("design/ doctrine folder not found")
    elif not os.path.isfile(index):
        doctrine.append("design/INDEX.md manifest missing")
    if os.path.isfile(claude):
        if "design/INDEX.md" not in open(claude, encoding="utf-8", errors="ignore").read():
            doctrine.append("CLAUDE.md does not reference design/INDEX.md (router not wired)")
    if os.path.isfile(index):
        itext = open(index, encoding="utf-8", errors="ignore").read()
        for fn in sorted(os.listdir(design_dir)):
            if fn.endswith(".md") and fn != "INDEX.md" and fn not in itext:
                doctrine.append(f"design/{fn} exists but is not listed in design/INDEX.md")
        for m in sorted(set(re.findall(r"design/[A-Za-z0-9_\-]+\.md", itext))):
            if not os.path.isfile(os.path.join(REPO, m)):
                doctrine.append(f"INDEX.md lists {m} but it does not exist")

    # ---- REPORT ----
    def score(viol):
        return 10 if not viol else max(0, 10 - len(viol))
    print("=" * 56)
    print("  Instinct RPG - Skill SSOT Audit")
    print("=" * 56)
    print(f"  Installed skills dir: {installed or 'NOT FOUND'}")
    for label, viol in (("Reference integrity", refs),
                        ("Drift (mirror = installed)", drift),
                        ("Structure (folder shape)", structure),
                        ("Sprawl (no stray copies)", sprawl),
                        ("Doctrine / manifest wiring", doctrine)):
        print(f"\n  {label}: {score(viol)}/10")
        for v in viol:
            print(f"     - {v}")
    total = refs + drift + structure + sprawl + doctrine
    print("\n" + "=" * 56)
    if not total:
        print("  CLEAN - 0 violations. Safe to close the session.")
    else:
        print(f"  {len(total)} violation(s). (Drift 'reinstall' warnings clear once the .skill files are installed.)")
    print("=" * 56)
    sys.exit(0 if not total else 1)

if __name__ == "__main__":
    main()
