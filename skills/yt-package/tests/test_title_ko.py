"""Korean calibration of title.py (heuristic, not calibrated). Standard library only.

    python3 -m unittest discover -s plugin/skills/yt-package/tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import title  # noqa: E402


def kinds(result):
    return [kind for kind, _ in result["issues"]]


class KoreanTitle(unittest.TestCase):
    def test_korean_title_is_not_zero_words(self):
        self.assertEqual(title.words("유튜브 쇼츠 자동화하는 법"), ["유튜브", "쇼츠", "자동화하는", "법"])

    def test_korean_subject_is_not_filler(self):
        # With no words read, the original called every Korean opening "all filler"
        self.assertNotIn("front-load", kinds(title.check("유튜브 쇼츠 자동화하는 법")))

    def test_capitals_check_does_not_fire_on_korean(self):
        r = title.check("GPT로 SNS를 자동화하는 법, API도 필요 없다")
        self.assertNotIn("shouting", kinds(r))
        self.assertFalse(any("all-caps" in line for line in r["good"]))

    def test_thumbnail_repeating_a_korean_title_is_caught(self):
        r = title.check("유튜브 쇼츠 자동화하는 법", "쇼츠 자동화")
        self.assertIn("duplicate", kinds(r))
        self.assertNotIn("thumbnail and title carry different words", r["good"])

    def test_korean_vague_words(self):
        self.assertIn("vague", kinds(title.check("진짜 대박 미쳤다 레전드 영상")))

    def test_korean_result_is_labeled_uncalibrated(self):
        self.assertEqual(title.check("유튜브 쇼츠 자동화하는 법")["calibration"], "none")


class EnglishUnchanged(unittest.TestCase):
    def test_english_checks_unchanged(self):
        r = title.check("AI RAN MY CHANNEL FOR 30 DAYS")
        self.assertEqual(r["score"], 94)
        self.assertEqual(kinds(r), ["shouting"])
        self.assertNotIn("calibration", r)
        r = title.check("I Tried EVERY AI Video Editor (SHOCKING RESULTS)", "Every AI Editor Tested Here Today Now")
        self.assertEqual(r["score"], 34)
        self.assertEqual(kinds(r), ["mobile", "shouting", "no-number", "duplicate", "thumb-length"])


if __name__ == "__main__":
    unittest.main()
