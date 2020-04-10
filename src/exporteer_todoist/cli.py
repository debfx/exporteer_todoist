import argparse
import json
import os
import requests
import sys
from io import BytesIO
from operator import itemgetter
from pathlib import Path
from zipfile import ZipFile


def get_token():
    token = os.environ.get('TODOIST_API_TOKEN', None)
    if not token:
        print('TODOIST_API_TOKEN must be set', file=sys.stderr)
        sys.exit(1)
    return token


def full_sync(args):
    token = get_token()
    params = {'token': token, 'sync_token': '*', 'resource_types': '["all"]'}
    resp = requests.get('https://api.todoist.com/sync/v8/sync', params=params)
    resp.raise_for_status()
    print(json.dumps(resp.json(), indent=2))
    return 0


def latest_backup(args):
    token = get_token()
    params = {'token': token}
    resp = requests.get('https://api.todoist.com/sync/v8/backups/get',
                        params=params)
    resp.raise_for_status()

    versions = sorted(resp.json(), key=itemgetter('version'), reverse=True)
    if len(versions) <= 0:
        print('no backups available', file=sys.stderr)
        return 2

    url = versions[0]['url']
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    zipdata = BytesIO(resp.content)

    target_dir = Path(args.target_dir[0])
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
    elif target_dir.is_file():
        print(f'expected a directory: {target_dir}', file=sys.stderr)
        return 1

    with ZipFile(zipdata, 'r') as zf:
        zf.extractall(target_dir)

    return 0


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=None)

    subs = parser.add_subparsers(title='Commands')

    p_full_sync = subs.add_parser('full_sync', help='export the json output' +
                                                    ' of the sync endpoint')
    p_full_sync.set_defaults(func=full_sync)

    p_latest_backup = subs.add_parser('latest_backup',
                                      help='download and unpack the latest' +
                                      ' backup zip to specified directory')
    p_latest_backup.set_defaults(func=latest_backup)
    p_latest_backup.add_argument('target_dir', nargs=1,
                                 help='directory to write contents of zip' +
                                 'file to (will be created if necessary)')

    args = parser.parse_args(args)
    if not args.func:
        parser.print_help()
        return 1
    return args.func(args)
