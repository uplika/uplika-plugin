"""Korean calibration of hookscore.py (heuristic, not calibrated). Standard library only.

    python3 -m unittest discover -s plugin/skills/yt-script/tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import hookscore  # noqa: E402

KO = "구독자 1000명 전에 이걸 모르면 영상 100개를 버립니다"
EN = "If you don't know this before 1,000 subscribers, you will waste 100 videos"


def score(t):
    return hookscore.score(t)


def render(t):
    return hookscore.render(t)


class KoreanHook(unittest.TestCase):
    def test_korean_hook_is_not_zero(self):
        r = score(KO)
        self.assertGreater(r["brevity"], 0)
        self.assertGreater(r["specificity"], 0)

    def test_korean_hook_without_digits_is_not_zero(self):
        # The original reads no word at all in Hangul, so a digit-free hook scored 0 on both
        r = score("여러분이 유튜브를 포기하는 진짜 이유는 따로 있습니다")
        self.assertGreater(r["brevity"], 0)
        self.assertGreater(r["specificity"], 0)

    def test_length_is_counted_in_syllables(self):
        # 19 Hangul syllables plus two numbers (one word each, 2.0 syllables) sit inside the converted band
        self.assertEqual(score(KO)["brevity"], 100)
        self.assertLess(score("이거 보세요")["brevity"], 100)
        self.assertLess(score("가" * 120)["brevity"], 100)

    def test_numbers_glued_to_korean_units_are_concrete(self):
        # 1000명 and 100개를: Python's \b sees no boundary between a digit and Hangul
        self.assertEqual(score(KO)["specificity"], 34 + 2 * 22)
        self.assertGreater(score("3일 만에 100만 원")["specificity"], score("며칠 만에 큰돈")["specificity"])

    def test_korean_word_lists(self):
        self.assertGreater(score("여러분 이거 모르면 손해입니다")["address"], score("이거 모르면 손해입니다")["address"])
        self.assertGreater(score("구독자님들 이거 보세요")["address"], score("구독자들 이거 보세요")["address"])
        self.assertEqual(score("너무 좋아요")["address"], score("정말 좋아요")["address"])  # 너무 is not 너
        self.assertGreater(score("영상 100개를 버립니다")["stakes"], score("영상 100개를 올립니다")["stakes"])
        self.assertGreater(score("이러다 채널 망합니다")["stakes"], score("이러다 채널 큽니다")["stakes"])
        self.assertGreater(score("왜 아무도 이걸 말 안 해줄까?")["curiosity"], score("이걸 말해 드립니다")["curiosity"])
        self.assertEqual(score("왜냐하면 쉽거든요")["curiosity"], score("그러니까 쉽거든요")["curiosity"])
        self.assertLess(score("진짜 대박 미쳤다 레전드 영상")["specificity"], score("영상 하나 올렸습니다")["specificity"])

    def test_korean_hook_gets_a_formula(self):
        self.assertEqual(score(KO)["formula"], "The Direct Address")
        self.assertEqual(score("유튜브 쇼츠 만드는 7가지 방법")["formula"], "The List")
        self.assertEqual(score("클로드 vs 챗GPT, 대본은 뭐가 더 나을까")["formula"], "The Comparison")

    def test_korean_result_is_labeled_uncalibrated(self):
        self.assertIn("not calibrated", render(KO))
        self.assertIn("Korean: heuristic, not calibrated", render(KO))
        r = score(KO)
        self.assertEqual(r["calibration"], "none")
        self.assertIsNone(r["band"])

    def test_threshold_slot_per_language(self):
        self.assertIn("en", hookscore.THRESHOLDS)
        self.assertIsNone(hookscore.THRESHOLDS["ko"])


class EnglishUnchanged(unittest.TestCase):
    def test_english_scores_unchanged(self):
        # The original hookscore.py prints 65 WORKABLE for this hook (run 2026-10-10)
        r = score(EN)
        self.assertEqual(r["total"], 65)

    def test_english_panel_unchanged(self):
        r = score(EN)
        self.assertEqual(
            [r["specificity"], r["address"], r["stakes"], r["curiosity"], r["brevity"]], [78, 96, 88, 41, 100]
        )
        self.assertEqual(r["band"], "WORKABLE")
        self.assertEqual(r["formula"], "The Direct Address")
        self.assertNotIn("calibrated", render(EN))


if __name__ == "__main__":
    unittest.main()
