import contextlib
import json
import io
import unittest
from middling_export_todoist import cli


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


if __name__ == '__main__':
    unittest.main()
