from io import BytesIO
import json
from exporteer_todoist import cli
from zipfile import ZipFile


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


def test_latest_backup(capfdbinary):
    assert cli.main(['latest_backup']) == 0
    cap = capfdbinary.readouterr()
    data = BytesIO(cap.out)
    zf = ZipFile(data)
    assert len([n for n in zf.namelist() if n.endswith('.csv')]) > 0

