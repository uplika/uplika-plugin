"""Korean calibration of deadair.py (heuristic, not calibrated). Standard library only.

    python3 -m unittest discover -s plugin/skills/yt-edit/tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import deadair  # noqa: E402


def cuts(cues, floor=0.45):
    return deadair.cuts_for(cues, floor)


def kinds_at(result, start):
    return sorted(c["kind"] for c in result if c["start"] == start)


class KoreanTranscript(unittest.TestCase):
    def test_korean_lines_are_not_deleted(self):
        # The original kept only [a-z ], so every Korean cue normalised to nothing
        self.assertEqual(deadair.norm("오늘은 쇼츠를 만드는 법"), ["오늘은", "쇼츠를", "만드는", "법"])

    def test_retake_marker_dasi_cuts_the_abandoned_take(self):
        result = cuts([
            (0.0, 2.0, "자 오늘은 클로드 코드로"),
            (2.1, 2.8, "아 다시"),
            (3.0, 6.0, "자 오늘은 클로드 코드로 쇼츠를 만들어 볼게요"),
        ])
        self.assertEqual(kinds_at(result, 0.0), ["REPEAT"])
        self.assertEqual(kinds_at(result, 2.1), ["FILLER"])
        self.assertEqual(kinds_at(result, 3.0), [])

    def test_retake_marker_ani_is_caught(self):
        result = cuts([
            (0.0, 2.0, "썸네일은 세 단어가"),
            (2.1, 2.6, "아니 아니"),
            (2.8, 6.0, "썸네일 글자는 세 단어 안으로 줄입니다"),
        ])
        self.assertEqual(kinds_at(result, 0.0), ["REPEAT"])
        self.assertEqual(kinds_at(result, 2.1), ["FILLER"])

    def test_korean_restart_with_the_same_opening(self):
        result = cuts([
            (0.0, 2.0, "오늘은 쇼츠를 만드는 법을"),
            (2.2, 6.0, "오늘은 쇼츠를 만드는 법을 알려드릴게요"),
        ])
        self.assertEqual(kinds_at(result, 0.0), ["REPEAT"])
        self.assertEqual(len([c for c in result if c["kind"] == "REPEAT"]), 1)

    def test_korean_fillers_and_plain_speech(self):
        result = cuts([
            (0.0, 0.6, "음"),
            (0.7, 3.0, "다시 말해서 첫 문장이 전부입니다"),
            (3.1, 3.6, "아니요"),
            (3.7, 6.0, "그래서 썸네일이 중요합니다"),
        ])
        self.assertEqual(kinds_at(result, 0.0), ["FILLER"])
        self.assertEqual(kinds_at(result, 0.7), [])  # 다시 inside a sentence is not a retake
        self.assertEqual(kinds_at(result, 3.1), [])  # 아니요 is an answer, not a marker
        self.assertEqual(kinds_at(result, 3.7), [])


class EnglishUnchanged(unittest.TestCase):
    def test_english_cuts_unchanged(self):
        result = cuts([
            (0.0, 2.1, "So the first thing you need to know"),
            (2.3, 3.0, "um"),
            (3.2, 6.0, "So the first thing you need to know is the hook"),
            (7.4, 9.0, "the hook is the first fifteen seconds"),
        ])
        self.assertEqual(
            [(c["kind"], c["start"], c["end"], c["why"]) for c in result],
            [
                ("REPEAT", 0.0, 2.1, 'restart of "so the first thing you"'),
                ("FILLER", 2.3, 3.0, "um"),
                ("DEAD", 6.225, 7.175, "1.40s gap"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
