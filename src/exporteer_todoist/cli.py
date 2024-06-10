"""Command-line interface for exporteer_todoist tool."""


import argparse
import os
import requests
import sys
from operator import itemgetter


def _get_token():
    token = os.environ.get('TODOIST_API_TOKEN', None)
    if not token:
        print('TODOIST_API_TOKEN must be set', file=sys.stderr)
        sys.exit(1)
    return token


def _full_sync(args):
    token = _get_token()
    params = {'sync_token': '*', 'resource_types': '["all"]'}
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get('https://api.todoist.com/sync/v9/sync', params=params, headers=headers)
    resp.raise_for_status()
    print(resp.text)
    return 0


def _latest_backup(args):
    token = _get_token()
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get('https://api.todoist.com/sync/v9/backups/get',
                        headers=headers)
    resp.raise_for_status()

    versions = sorted(resp.json(), key=itemgetter('version'), reverse=True)
    if len(versions) <= 0:
        print('no backups available', file=sys.stderr)
        return 2

    if args.output == '-':
        output_file = sys.stdout.buffer
    else:
        output_file = open(args.output, 'wb')

    url = versions[0]['url']
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    output_file.write(resp.content)
    output_file.flush()

    return 0


def main(args=None):
    """Runs the tool and returns its exit code.

    args may be an array of string command-line arguments; if absent,
    the process's arguments are used.
    """
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=None)

    subs = parser.add_subparsers(title='Commands')

    p_full_sync = subs.add_parser('full_sync', help='export the json output' +
                                                    ' of the sync endpoint')
    p_full_sync.set_defaults(func=_full_sync)

    p_latest_backup = subs.add_parser('latest_backup',
                                      help='download latest backup zip')
    p_latest_backup.add_argument('--output', '-o', default='-',
                                 help='path to write the zip file to (defaults to "-" for stdout)')
    p_latest_backup.set_defaults(func=_latest_backup)

    args = parser.parse_args(args)
    if not args.func:
        parser.print_help()
        return 1
    return args.func(args)
