#!/usr/bin/env python3
"""title.py - lint a YouTube title and thumbnail pairing before you publish it.

    python3 title.py --title "..." --thumb "AI RAN IT"
    python3 title.py titles.txt            # one per line, ranked
    python3 title.py --title "..." --json

The pairing is the unit, not the title. A title that repeats the thumbnail text wastes half the
click surface, and that is the single most common mistake this checks for.

Length: YouTube truncates around 60 characters on desktop search and around 40 on a mobile home
feed. Both limits are reported because they are different failures - a desktop truncation loses the
tail, a mobile one can lose the subject.
"""
# Adapted from Jakeschincariol/youtube-agent-skill (MIT) for the Uplika plugin. English behaviour is
# the original. Korean (2026-10-10) is heuristic, NOT calibrated: words are space-separated eojeol
# with particles attached, the capitals check skips Hangul words (Hangul has no capitals, and an
# acronym with a particle such as GPT로 is not shouting), and the cut points stay the ones measured
# on Latin text. The module docstring above is the CLI's usage text, so it stays the original.
import json, re, sys, os

DESKTOP, MOBILE, HARD = 60, 40, 100
VAGUE = {"amazing","incredible","insane","crazy","huge","massive","ultimate","best","powerful",
         "secret","revolutionary","mindblowing","epic","perfect","complete","everything"}
STOP = {"the","a","an","of","for","to","in","on","and","or","is","are","with","your","you","my","i",
        "this","that","it","how","what","why"}

HANGUL = re.compile(r"[가-힣]")
# Hype and intensifier words, matched at the start of a word because endings attach (미쳤다, 엄청난)
KO_VAGUE = re.compile(r"^(?:진짜|완전|대박|미쳤|레전드|엄청)")

# The original tokenizer was [a-z0-9']+. Adding the Hangul range changes nothing for text without Hangul.
def words(t): return re.findall(r"[가-힣a-z0-9']+", t.lower())

def ko_shared(a_words, b_words):
    """Korean words two texts share, allowing a particle on one side: 자동화 and 자동화하는, 쇼츠 and 쇼츠를."""
    return {min(a, b, key=len) for a in a_words for b in b_words
            if HANGUL.search(a) and HANGUL.search(b) and min(len(a), len(b)) >= 2
            and (a.startswith(b) or b.startswith(a))}

def check(title, thumb=None):
    t = title.strip()
    ko = bool(HANGUL.search(t) or (thumb and HANGUL.search(thumb)))
    n = len(t)
    issues, good = [], []
    if n > HARD: issues.append(("length", f"{n} characters - YouTube's hard limit is {HARD}"))
    elif n > DESKTOP: issues.append(("length", f"{n} characters - desktop search cuts near {DESKTOP}"))
    else: good.append(f"{n} characters, inside the {DESKTOP}-character desktop cut")
    if n > MOBILE:
        head = t[:MOBILE].rsplit(" ", 1)[0]
        issues.append(("mobile", f'a mobile feed shows about "{head}..." - check the subject survives'))
    caps = [w for w in t.split() if len(w) > 2 and w.isupper() and not HANGUL.search(w)]
    if len(caps) > 2: issues.append(("shouting", f"{len(caps)} all-caps words - two is the ceiling before it reads as spam"))
    elif caps: good.append(f"{len(caps)} all-caps word for emphasis")
    v = [w for w in words(t) if w in VAGUE]
    if ko: v += [w for w in words(t) if KO_VAGUE.match(w)]
    if v: issues.append(("vague", f"{', '.join(sorted(set(v)))} - swap for a number, a name or a date"))
    nums = re.findall(r"\d[\d,.]*%?", t)
    if nums: good.append(f"carries a concrete figure ({', '.join(nums[:3])})")
    else: issues.append(("no-number", "no number, date or name - the most reliable single fix"))
    if t.endswith("?"): good.append("open question in the title")
    front = [w for w in words(t)[:3] if w not in STOP]
    if not front: issues.append(("front-load", "the first three words are all filler - move the subject forward"))
    if thumb:
        tw, hw = set(words(t)) - STOP, set(words(thumb)) - STOP
        shared = tw & hw
        if ko: shared |= ko_shared(tw, hw)
        if shared:
            issues.append(("duplicate", f"thumbnail repeats the title on {', '.join(sorted(shared))} - "
                                        "the thumbnail should say what the title does not"))
        else:
            good.append("thumbnail and title carry different words")
        if len(words(thumb)) > 4:
            issues.append(("thumb-length", f"{len(words(thumb))} words on the thumbnail - three is the ceiling at feed size"))
    score = max(0, min(100, 100 - 14 * len(issues) + 4 * len(good)))
    r = {"title": t, "chars": n, "score": score, "issues": issues, "good": good}
    if ko: r["calibration"] = "none"
    return r

def show(r):
    print(f'\n  "{r["title"]}"')
    print(f"  {r['chars']} chars   score {r['score']}/100")
    for k, m in r["issues"]: print(f"    x  {k:<12} {m}")
    for m in r["good"]:      print(f"    ok              {m}")
    if r.get("calibration") == "none":
        print("    Korean: heuristic, not calibrated (the cut points were measured on Latin text, and Hangul is wider)")

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    thumb = a[a.index("--thumb") + 1] if "--thumb" in a else None
    if "--title" in a:
        rows = [check(a[a.index("--title") + 1], thumb)]
    elif a and os.path.exists(a[0]):
        rows = [check(l, thumb) for l in open(a[0]).read().splitlines() if l.strip()]
    else:
        print(__doc__); sys.exit(1)
    rows.sort(key=lambda r: -r["score"])
    if as_json: print(json.dumps(rows, indent=1)); return
    for r in rows: show(r)
    print()

if __name__ == "__main__":
    main()
