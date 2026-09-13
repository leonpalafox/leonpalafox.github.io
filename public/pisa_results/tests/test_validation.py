"""Ensure incorrect data and stale published pages cannot pass the audit gate."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'build'))
import validate_data

class ValidationGate(unittest.TestCase):
    def run_case(self, mutate=None, stale=False):
        actual = validate_data.HERE
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build = root / 'build'
            build.mkdir()
            (build / 'sources').symlink_to(actual / 'sources', target_is_directory=True)
            data = json.loads((actual / 'pisa_data.json').read_text())
            if mutate: mutate(data)
            (build / 'pisa_data.json').write_text(json.dumps(data))
            (root / 'index.html').write_text('<!doctype html>stale' if stale else (actual.parent / 'index.html').read_text())
            with patch.object(validate_data, 'HERE', build), contextlib.redirect_stdout(io.StringIO()):
                validate_data.validate()

    def test_published_dataset_passes(self):
        self.run_case()

    def test_changed_mean_is_rejected(self):
        with self.assertRaises(AssertionError):
            self.run_case(lambda d: d['rows'][0]['m'].__setitem__('sci', 598))

    def test_false_significance_is_rejected(self):
        with self.assertRaises(AssertionError):
            self.run_case(lambda d: d['oecd']['s'].__setitem__('sci', [-2.8, True]))

    def test_stale_html_is_rejected(self):
        with self.assertRaises(AssertionError):
            self.run_case(stale=True)

if __name__ == '__main__':
    unittest.main()
