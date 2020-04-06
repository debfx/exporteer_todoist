import argparse
import contextlib
import csv
import json
import io
import unittest
from middling_export_todoist import cli
from pathlib import Path
from tempfile import TemporaryDirectory


class ExportsTestCase(unittest.TestCase):
    def test_full_sync(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            cli.full_sync(None)
        result = out.getvalue()
        parsed = json.loads(result)
        keys = parsed.keys()
        self.assertIn('projects', keys)
        self.assertIn('items', keys)
        self.assertIn('notes', keys)
        self.assertGreater(len(parsed['projects']), 1)
        self.assertGreater(len(parsed['items']), 1)

    def test_latest_backup(self):
        with TemporaryDirectory() as rawpath:
            args = argparse.Namespace()
            args.target_dir = [rawpath]
            cli.latest_backup(args)
            path = Path(rawpath)
            cpaths = list(path.glob('*.csv'))
            self.assertGreater(len(cpaths), 1)
            maxlen = 0
            for cpath in cpaths:
                with open(cpath) as file:
                    maxlen = max(maxlen, len(list(csv.reader(file))))
            self.assertGreater(maxlen, 1)


if __name__ == '__main__':
    unittest.main()
