#!/usr/bin/env python3
"""deadair.py - an edit decision list from a timestamped transcript.

    python3 deadair.py transcript.srt            # or .vtt, or whisper .json
    python3 deadair.py transcript.srt --floor 0.35 --json

Finds three things and prints the cuts as a list you can act on, newest problem first:
  DEAD    gaps between spoken cues longer than the floor
  FILLER  cues that are only filler ("um", "so yeah", "basically")
  REPEAT  a sentence restarted - the second take of the same opening

WHAT IT DOES NOT DO. It does not cut the file. It prints an EDL, the total it would remove, and the
runtime you would land on, and you apply it in whatever editor you use. Nothing here touches media.
"""
# Adapted from Jakeschincariol/youtube-agent-skill (MIT) for the Uplika plugin. English behaviour is
# the original; the loop moved from main() into cuts_for() so it can be tested, with the same output.
# Korean (2026-10-10) is heuristic, NOT calibrated: the original norm() kept only [a-z ], so every
# Korean cue normalised to nothing and no Korean retake was ever found. Korean cues keep their
# Hangul, Korean fillers count as FILLER, and a cue that is only the retake marker 다시 or 아니
# (with fillers) cuts the take before it. The module docstring above is the CLI's usage text.
import json, os, re, sys

FILLER_ONLY = re.compile(r"^[\s,.-]*((um+|uh+|er+|ah+|so|okay|ok|right|yeah|like|anyway|basically|"
                         r"actually|you know|i mean|let me see|hold on)[\s,.-]*)+$", re.I)

HANGUL = re.compile(r"[가-힣]")
# Korean hesitations and filler words (um, uh, like, now, so, anyway, you know, hold on, yeah), and
# the retake markers: 다시 (again), 아니 (no), 다시 할게요 (let me do that again).
FILLER_ONLY_KO = re.compile(r"^[\s,.?!~…-]*((다시\s*(할게요|갈게요|하겠습니다|가겠습니다|할게|갈게)|다시|아니|음+|어+|아+|으+|에+|"
                            r"그+|뭐|막|이제|약간|그러니까|그니까|아무튼|있잖아요|있잖아|잠깐만요|잠깐만|잠깐|네|예)[\s,.?!~…-]*)+$")
RETAKE_KO = re.compile(r"다시|아니")
# A restart is the same opening twice. English compares the first five words; a Korean word carries
# its particle and ending, so Korean compares the first syllables instead, at the same provisional
# two syllables per English word as hookscore.py: 5 words -> 10 syllables, at least 3 -> 6.
KO_SYLLABLES_PER_WORD = 2.0
KO_OPENING = int(5 * KO_SYLLABLES_PER_WORD)
KO_OPENING_MIN = int(3 * KO_SYLLABLES_PER_WORD)

def parse_ts(s):
    s = s.strip().replace(",", ".")
    p = s.split(":")
    return int(p[0]) * 3600 + int(p[1]) * 60 + float(p[2]) if len(p) == 3 else int(p[0]) * 60 + float(p[1])

def load(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    if path.endswith(".json"):
        d = json.loads(raw)
        segs = d.get("segments", d if isinstance(d, list) else [])
        return [(float(s["start"]), float(s["end"]), (s.get("text") or "").strip()) for s in segs]
    cues, cur = [], None
    for line in raw.splitlines():
        m = re.match(r"\s*(\d[\d:.,]+)\s*-->\s*(\d[\d:.,]+)", line)
        if m:
            cur = [parse_ts(m.group(1)), parse_ts(m.group(2)), []]
            cues.append(cur)
        elif cur is not None and line.strip() and not line.strip().isdigit():
            cur[2].append(line.strip())
    return [(a, b, " ".join(t)) for a, b, t in cues if t]

# The original kept [a-z ] only. Keeping Hangul too changes nothing for text without Hangul.
def norm(t): return re.sub(r"[^a-z가-힣 ]", "", t.lower()).split()

def filler_only(t):
    return bool(FILLER_ONLY.match(t)) or (bool(HANGUL.search(t)) and bool(FILLER_ONLY_KO.match(t)))

def ko_opening(t): return "".join(norm(t))[:KO_OPENING]

def previous_speech(cues, i):
    # A restart is compared against the last cue that was actually SPEECH. Comparing against
    # the literal previous cue misses every retake with an "um" between the two attempts, which
    # is most of them.
    j = i - 1
    while j >= 0 and (filler_only(cues[j][2]) or not cues[j][2].strip()): j -= 1
    return j

def cuts_for(cues, floor=0.45):
    cuts, repeated = [], set()
    for i, (s, e, t) in enumerate(cues):
        if filler_only(t):
            cuts.append({"kind": "FILLER", "start": s, "end": e, "why": t.strip()[:48]})
            if HANGUL.search(t) and RETAKE_KO.search(t):
                # 다시 / 아니 on its own: the speaker dropped the take before it
                j = previous_speech(cues, i)
                if j >= 0 and j not in repeated:
                    repeated.add(j)
                    cuts.append({"kind": "REPEAT", "start": cues[j][0], "end": cues[j][1],
                                 "why": f'retake marker "{t.strip()[:24]}" after it'})
        if i:
            gap = s - cues[i - 1][1]
            if gap > floor:
                keep = floor / 2
                cuts.append({"kind": "DEAD", "start": round(cues[i - 1][1] + keep, 3),
                             "end": round(s - keep, 3), "why": f"{gap:.2f}s gap"})
        if t.strip() and not filler_only(t):
            j = previous_speech(cues, i)
            if j >= 0 and j not in repeated:
                if HANGUL.search(t) or HANGUL.search(cues[j][2]):
                    a1, b1 = ko_opening(cues[j][2]), ko_opening(t)
                    if len(a1) >= KO_OPENING_MIN and a1 == b1:
                        repeated.add(j)
                        cuts.append({"kind": "REPEAT", "start": cues[j][0], "end": cues[j][1],
                                     "why": f'restart of "{" ".join(cues[j][2].split()[:4])}"'})
                else:
                    a1, b1 = norm(cues[j][2])[:5], norm(t)[:5]
                    if len(a1) >= 3 and a1 == b1:
                        repeated.add(j)
                        cuts.append({"kind": "REPEAT", "start": cues[j][0], "end": cues[j][1],
                                     "why": f'restart of "{" ".join(a1)}"'})
    cuts = [c for c in cuts if c["end"] > c["start"]]
    cuts.sort(key=lambda c: c["start"])
    return cuts

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    floor = float(a[a.index("--floor") + 1]) if "--floor" in a else 0.45
    a = [x for x in a if not x.startswith("--") and not re.match(r"^[\d.]+$", x)]
    if not a or not os.path.exists(a[0]): print(__doc__); sys.exit(1)
    cues = load(a[0])
    if not cues: print("no cues found - is this an srt, vtt or whisper json?"); sys.exit(1)
    dur = cues[-1][1]
    cuts = cuts_for(cues, floor)
    removed = sum(c["end"] - c["start"] for c in cuts)
    ko = any(HANGUL.search(c[2]) for c in cues)
    if as_json:
        out = {"source": a[0], "duration": dur, "cuts": cuts,
               "removed": round(removed, 3), "out": round(dur - removed, 3)}
        if ko: out.update({"language": "ko", "calibration": "none"})
        print(json.dumps(out, indent=1)); return
    print(f"\n  {a[0]}   {dur:.2f}s in, {len(cues)} cues, dead-air floor {floor}s\n")
    for c in cuts:
        print(f"    {c['kind']:<7} {c['start']:8.2f} -> {c['end']:8.2f}   {c['end']-c['start']:5.2f}s   {c['why']}")
    if ko:
        print("\n  Korean: heuristic, not calibrated (fillers and the retake markers 다시 / 아니 are a word list).")
    print(f"\n  {len(cuts)} cuts, {removed:.2f}s removed, {dur - removed:.2f}s out "
          f"({removed / dur * 100:.1f}% shorter)\n")

if __name__ == "__main__":
    main()
