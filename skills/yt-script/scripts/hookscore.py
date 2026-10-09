#!/usr/bin/env python3
"""hookscore.py - score a YouTube hook before you waste a take on it.

Five properties, 0-100 each, and a verdict that is 60% the mean and 40% the weakest one. The
weakest-link weighting is deliberate: a hook with four strong properties and one dead one is a hook
that leaks at the dead one, and averaging hides that.

    python3 hookscore.py hooks.txt            # one hook per line, ranked
    python3 hookscore.py --hook "one line"    # score a single hook
    python3 hookscore.py --json hooks.txt     # machine-readable

WHAT THIS CAN AND CANNOT TELL YOU. Measured against 74 real short-form hooks (first 15 seconds of
auto-captions, top-8 and bottom-8 by views across five channels): it separates deliberately bad
hooks from real ones well, and it separates a creator's own hits from their own misses barely at
all. Treat a low score as a reason to look again, never a high score as a promise.
"""
# Adapted from Jakeschincariol/youtube-agent-skill (MIT) for the Uplika plugin. The English panel
# below is the original, unchanged. Korean support (2026-10-10) is a separate path, chosen when the
# hook contains Hangul; see the Korean section further down. The module docstring above is left as
# the original because the CLI prints it as its usage text.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORMULAS = json.load(open(os.path.join(HERE, "hooks.json")))["hooks"]

FILLER = {"basically","actually","literally","just","really","very","so","kind","sort","like",
          "guys","hey","welcome","today","video","subscribe","channel"}
VAGUE = {"amazing","incredible","insane","crazy","huge","massive","game","changer","secret",
         "powerful","ultimate","best","revolutionary","mind","blowing","unbelievable"}
CONCRETE = re.compile(r"\b(\d[\d,.]*\s?(%|k|m|x|s|m|h)?|\$\d|\d+\s?(second|minute|hour|day|week|month|year)s?)\b", re.I)
YOU = re.compile(r"\b(you|your|you're|youre|yourself)\b", re.I)
STAKE = re.compile(r"\b(lose|lost|wasting|waste|quit|fail|broke|cost|risk|before|stop|never|die|dying|dead)\b", re.I)
CURIOSITY = re.compile(r"\b(why|how|what|which|until|before|but|nobody|almost|except|reason|actually)\b", re.I)

# The original tokenizer was [a-z0-9'%$.]+. Adding the Hangul range changes nothing for text without
# Hangul, and text with Hangul goes down the Korean path anyway.
def words(t): return re.findall(r"[가-힣a-z0-9'%$.]+", t.lower())

def specificity(t):
    w = words(t)
    if not w: return 0
    nums = len(CONCRETE.findall(t))
    vague = sum(1 for x in w if x in VAGUE)
    filler = sum(1 for x in w if x in FILLER)
    s = 34 + nums * 22 - vague * 16 - filler * 5
    # proper nouns that are not sentence-initial read as named things
    s += min(18, 6 * sum(1 for x in t.split()[1:] if x[:1].isupper()))
    return max(0, min(100, s))

def address(t):
    n = len(YOU.findall(t))
    first = 30 if YOU.search(" ".join(t.split()[:6])) else 0
    return max(0, min(100, 26 + n * 20 + first))

def stakes(t):
    n = len(STAKE.findall(t))
    return max(0, min(100, 22 + n * 26 + (14 if CONCRETE.search(t) else 0)))

def curiosity(t):
    n = len(CURIOSITY.findall(t))
    q = 18 if t.strip().endswith("?") else 0
    # a hook that resolves itself has no gap left
    closed = -18 if re.search(r"\b(because|so that|which means)\b", t, re.I) else 0
    return max(0, min(100, 24 + n * 17 + q + closed))

def brevity(t):
    n = len(words(t))
    if n == 0: return 0
    # 9-24 words is the band a spoken hook lands in at ~150wpm inside 10 seconds
    if 9 <= n <= 24: return 100
    if n < 9:  return max(30, 100 - (9 - n) * 11)
    return max(10, 100 - (n - 24) * 7)

PROPS = [("SPECIFICITY", specificity), ("ADDRESS", address), ("STAKES", stakes),
         ("CURIOSITY", curiosity), ("BREVITY", brevity)]

# ---- Korean: heuristic, NOT calibrated ------------------------------------------------------------
# The English panel was calibrated on 74 English hooks. Nothing like that exists for Korean yet, so a
# hook with Hangul in it is scored on the same five properties with Korean word lists, its length is
# counted in syllables, and the result carries calibration "none" and no STRONG/WORKABLE/WEAK band.
# Words are space-separated eojeol; particles stay attached (no morphological analyser, no
# dependency), so the word lists match at the start of each word: 여러분은, 손해를, 버립니다.
HANGUL = re.compile(r"[가-힣]")
# One English word is taken as two Hangul syllables. Provisional: it converts the English brevity
# band (9-24 words) into syllables until the band is measured on real Korean hooks.
KO_SYLLABLES_PER_WORD = 2.0
# No \b: Python counts Hangul as a word character, so there is no boundary inside 1000명 or 100개를.
# The unit is optional, so a bare number (1000명, 100개) still counts.
KO_CONCRETE = re.compile(r"\$\d|\d[\d,.]*\s?(?:만|억|원|초|분|시간|일|주|개월|년|배|%)?")
KO_YOU = re.compile(r"^(?:여러분|당신|너(?:$|희|는|도|의|를|가|한테|에게|만|랑|와)|넌$|널$)|님")  # 너무 is not 너
# Verb stems list the syllables their endings fold into: 버립니다 is 버 + 립, not 버 + 리 + ㅂ.
KO_STAKE = re.compile(r"^(?:손해|망[하한할합해했]|실패|포기|버[리린릴립려렸림])")
KO_CURIOSITY = re.compile(r"^(?:왜(?!냐)|어떻게|비밀|사실은|아무도)")  # 왜냐하면 answers the question
# Split like the English lists: intensifiers are FILLER (really, very), hype words are VAGUE (crazy, insane).
KO_VAGUE = re.compile(r"^(?:대박|미쳤|레전드)")
KO_FILLER = re.compile(r"^(?:진짜|완전|엄청)")

# Verdict bands per language: (STRONG at or above, WORKABLE at or above). None = not calibrated, no band.
THRESHOLDS = {"en": (72, 55), "ko": None}

def is_korean(t): return bool(HANGUL.search(t))

def syllables(t):
    """Hangul syllables, plus each Latin word or number counted as one word (KO_SYLLABLES_PER_WORD)."""
    rest = re.sub(r"[가-힣]", " ", t.lower())
    return len(HANGUL.findall(t)) + KO_SYLLABLES_PER_WORD * len(re.findall(r"[a-z]+|\d[\d,.]*", rest))

def specificity_ko(t):
    w = words(t)
    if not w: return 0
    nums = len(KO_CONCRETE.findall(t))
    vague = sum(1 for x in w if KO_VAGUE.match(x))
    filler = sum(1 for x in w if KO_FILLER.match(x))
    s = 34 + nums * 22 - vague * 16 - filler * 5
    s += min(18, 6 * sum(1 for x in t.split()[1:] if x[:1].isupper()))
    return max(0, min(100, s))

def address_ko(t):
    w = words(t)
    n = sum(1 for x in w if KO_YOU.search(x))
    first = 30 if any(KO_YOU.search(x) for x in w[:6]) else 0
    return max(0, min(100, 26 + n * 20 + first))

def stakes_ko(t):
    n = sum(1 for x in words(t) if KO_STAKE.match(x))
    return max(0, min(100, 22 + n * 26 + (14 if KO_CONCRETE.search(t) else 0)))

def curiosity_ko(t):
    n = sum(1 for x in words(t) if KO_CURIOSITY.match(x))
    q = 18 if t.strip().endswith("?") else 0
    return max(0, min(100, 24 + n * 17 + q))

def brevity_ko(t):
    n = syllables(t) / KO_SYLLABLES_PER_WORD  # in English-word equivalents
    if n == 0: return 0
    if 9 <= n <= 24: return 100
    if n < 9:  return max(30, round(100 - (9 - n) * 11))
    return max(10, round(100 - (n - 24) * 7))

PROPS_KO = [("SPECIFICITY", specificity_ko), ("ADDRESS", address_ko), ("STAKES", stakes_ko),
            ("CURIOSITY", curiosity_ko), ("BREVITY", brevity_ko)]

# ---------------------------------------------------------------------------------------------------

def classify(t, lang="en"):
    best, hits = None, 0
    for f in FORMULAS:
        if lang == "ko":  # one Korean pattern per formula, so count its matches rather than patterns
            n = sum(1 for p in f.get("ko", []) for _ in re.finditer(p, t, re.I))
        else:
            n = sum(1 for p in f["match"] if re.search(p, t, re.I))
        if n > hits: best, hits = f, n
    return (best["name"] if best else "Unclassified"), hits

def band(v, lang="en"):
    cut = THRESHOLDS.get(lang)
    if cut is None: return None
    return "STRONG" if v >= cut[0] else "WORKABLE" if v >= cut[1] else "WEAK"

def score(t):
    """The panel for one hook, as a dict: the five properties (lowercase keys), total (the verdict),
    band, formula, language, and calibration ("none" for Korean)."""
    lang = "ko" if is_korean(t) else "en"
    parts = {n: fn(t) for n, fn in (PROPS_KO if lang == "ko" else PROPS)}
    vals = list(parts.values())
    verdict = round(0.6 * (sum(vals) / len(vals)) + 0.4 * min(vals))
    name, hits = classify(t, lang)
    r = {"hook": t.strip(), "properties": parts, "verdict": verdict, "band": band(verdict, lang),
         "formula": name, "matched": hits, "language": lang, "total": verdict,
         "calibration": "none" if lang == "ko" else "74 English short-form hooks"}
    r.update({k.lower(): v for k, v in parts.items()})
    return r

FIX = {
 "SPECIFICITY": "swap one adjective for a number, a name or a date",
 "ADDRESS": "say 'you' in the first six words",
 "STAKES": "name what it costs them to keep doing it the current way",
 "CURIOSITY": "cut the half of the sentence that answers itself",
 "BREVITY": "9 to 24 words. Read it out loud and stop where you run out of breath",
}
FIX_KO = {
 "SPECIFICITY": "swap a hype word (대박, 미쳤다, 레전드) for a number, a name or a date",
 "ADDRESS": "name the viewer early: 여러분, 당신, or who they are with -님",
 "STAKES": "name what it costs them to keep doing it the current way (손해, 포기, 버리다)",
 "CURIOSITY": "open a question the line does not answer (왜, 어떻게, 아무도)",
 "BREVITY": "provisional band of about 18 to 48 syllables (9 to 24 words at 2 syllables each). Read it out loud",
}

def render(r):
    """The text report for one hook. Takes a score() result or the hook text."""
    if isinstance(r, str): r = score(r)
    t, parts, verdict = r["hook"], r["properties"], r["verdict"]
    name, hits, ko = r["formula"], r["matched"], r["language"] == "ko"
    out = [f"\n  {t.strip()}", f"  {'-' * min(72, max(20, len(t.strip())))}"]
    for k, v in parts.items():
        out.append(f"    {k:<12} {v:3d}  {'#' * (v // 5)}")
    if ko:
        out.append(f"    {'VERDICT':<12} {verdict:3d}  (no band)")
        out.append("    Korean: heuristic, not calibrated. Rank hooks against each other; do not call one strong or weak.")
    else:
        out.append(f"    {'VERDICT':<12} {verdict:3d}  {r['band']}")
    found = f"{hits} Korean match{'es' if hits != 1 else ''}" if ko else f"{hits} pattern{'s' if hits != 1 else ''} matched"
    out.append(f"    formula      {name}" + (f"  ({found})" if hits else "  (no formula matched - that is usually a summary, not a hook)"))
    low = min(parts, key=parts.get)
    out.append(f"    weakest      {low} - {(FIX_KO if ko else FIX)[low]}")
    return "\n".join(out)

def json_row(r):
    row = {"hook": r["hook"], "properties": r["properties"], "verdict": r["verdict"],
           "band": r["band"], "formula": r["formula"]}
    if r["language"] == "ko":
        row["language"] = "ko"
        row["calibration"] = "none"
    return row

def main():
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    if "--hook" in a:
        lines = [a[a.index("--hook") + 1]]
    elif a and os.path.exists(a[0]):
        lines = [l for l in open(a[0]).read().splitlines() if l.strip()]
    else:
        print(__doc__); sys.exit(1 if not a else 0)
    out = [score(t) for t in lines]
    out.sort(key=lambda r: -r["verdict"])
    if as_json:
        print(json.dumps([json_row(r) for r in out], indent=1)); return
    for r in out:
        print(render(r))
    if len(out) > 1:
        print(f"\n  winner: {out[0]['hook'].strip()}  ({out[0]['verdict']}, {out[0]['band'] or 'Korean, not calibrated'})\n")

if __name__ == "__main__":
    main()
