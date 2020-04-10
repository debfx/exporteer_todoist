import argparse
import csv
import json
from exporteer_todoist import cli
from pathlib import Path
from tempfile import TemporaryDirectory


def test_full_sync(capsys):
    assert cli.main(['full_sync']) == 0
    cap = capsys.readouterr()
    parsed = json.loads(cap.out)
    keys = parsed.keys()
    assert 'projects' in keys
    assert 'items' in keys
    assert 'notes' in keys
    assert len(parsed['projects']) > 1
    assert len(parsed['items']) > 1


def test_latest_backup():
    with TemporaryDirectory() as rawpath:
        cli.main(['latest_backup', rawpath])
        path = Path(rawpath)
        cpaths = list(path.glob('*.csv'))
        assert len(cpaths) > 1
        maxlen = 0
        for cpath in cpaths:
            with open(cpath) as file:
                maxlen = max(maxlen, len(list(csv.reader(file))))
        assert maxlen > 1
