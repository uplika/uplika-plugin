"""swipe.py reads the hook formulas and the hook scorer from the ig-reel skill.

The plugin keeps scripts in scripts/ folders, so swipe.py looks in
../../ig-reel/scripts/. If either skill folder moves, the formulas stop being
named and the scores disappear without an error, which is what this catches.
"""

import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SWIPE = os.path.join(HERE, "..", "scripts", "swipe.py")

ROWS = (
    "account\tfollowers\tmedian\tviews\thook\n"
    "@a\t48000\t11000\t412000\tnobody tells you your first 30 reels are supposed to flop\n"
    "@b\t2000000\t900000\t1200000\tin this video I am going to show you my morning routine\n"
    "@c\t9000\t3000\t180000\tsteal this four line follow up it took me two years\n"
)


class SwipePaths(unittest.TestCase):
    def run_swipe(self, *args):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        with tempfile.TemporaryDirectory() as tmp:
            tsv = os.path.join(tmp, "captured.tsv")
            with open(tsv, "w", encoding="utf-8") as fh:
                fh.write(ROWS)
            done = subprocess.run(
                [sys.executable, SWIPE, tsv, *args],
                cwd=tmp, env=env, capture_output=True, text=True, check=False,
            )
            written = os.path.exists(os.path.join(tmp, "swipe.md"))
        return done, written

    def test_formulas_and_scores_come_from_ig_reel(self):
        done, _ = self.run_swipe()
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("Nobody Tells You", done.stdout)
        self.assertIn("The Steal", done.stdout)
        self.assertNotIn("hooks.json not found", done.stderr)
        self.assertNotIn("hookscore.py not importable", done.stderr)

    def test_out_takes_a_bare_file_name(self):
        done, written = self.run_swipe("--out", "swipe.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertTrue(written)


if __name__ == "__main__":
    unittest.main()
