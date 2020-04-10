import argparse
import contextlib
import csv
import json
import io
from exporteer_todoist import cli
from pathlib import Path
from tempfile import TemporaryDirectory


def test_full_sync():
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        cli.full_sync(None)
    result = out.getvalue()
    parsed = json.loads(result)
    keys = parsed.keys()
    assert 'projects' in keys
    assert 'items' in keys
    assert 'notes' in keys
    assert len(parsed['projects']) > 1
    assert len(parsed['items']) > 1


def test_latest_backup():
    with TemporaryDirectory() as rawpath:
        args = argparse.Namespace()
        args.target_dir = [rawpath]
        cli.latest_backup(args)
        path = Path(rawpath)
        cpaths = list(path.glob('*.csv'))
        assert len(cpaths) > 1
        maxlen = 0
        for cpath in cpaths:
            with open(cpath) as file:
                maxlen = max(maxlen, len(list(csv.reader(file))))
        assert maxlen > 1
