"""Korean calibration of chapters.py (heuristic, not calibrated). Standard library only.

    python3 -m unittest discover -s plugin/skills/yt-chapters/tests -v
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
sys.path.insert(0, SCRIPTS)
import chapters  # noqa: E402

TOPICS = [
    "오늘은 유튜브 쇼츠 첫 문장을 어떻게 쓰는지 알려드릴게요",
    "썸네일은 작은 화면에서도 읽히게 글자를 세 단어 안으로 줄입니다",
    "댓글은 처음 몇 시간 안에 답하면 대화가 길어집니다",
]


def srt(cues):
    def ts(t):
        h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
        return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")

    out = []
    for i, (a, b, text) in enumerate(cues, 1):
        out += [str(i), f"{ts(a)} --> {ts(b)}", text, ""]
    return "\n".join(out)


def korean_transcript():
    cues, t = [], 0.0
    for line in TOPICS:
        for _ in range(6):
            cues.append((round(t, 2), round(t + 3.0, 2), line))
            t += 3.2
        t += 3.0
    return cues


class KoreanChapters(unittest.TestCase):
    def test_korean_subtitles_yield_a_keyword(self):
        self.assertGreaterEqual(len(chapters.keywords(TOPICS[0])), 1)
        self.assertIn("썸네일은", chapters.keywords(TOPICS[1]))

    def test_korean_chapters_get_korean_draft_titles(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ko.srt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(srt(korean_transcript()))
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
            out = subprocess.run(
                [sys.executable, os.path.join(SCRIPTS, "chapters.py"), path, "--json"],
                capture_output=True, text=True, env=env, check=True,
            ).stdout
        data = json.loads(out)
        self.assertTrue(data["valid"])
        self.assertEqual(data["calibration"], "none")
        titles = [c["draft_title"] for c in data["chapters"]]
        self.assertNotIn("Section", titles)
        self.assertTrue(all(any("가" <= ch <= "힣" for ch in t) for t in titles))


class EnglishUnchanged(unittest.TestCase):
    def test_english_keywords_unchanged(self):
        self.assertEqual(
            chapters.keywords("The thumbnail needs contrast at feed size, and that is it"),
            {"thumbnail", "needs", "contrast", "feed", "size"},
        )


if __name__ == "__main__":
    unittest.main()
