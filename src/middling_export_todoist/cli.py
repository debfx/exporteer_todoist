import argparse
import json
import os
import requests
import sys


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


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=None)

    subs = parser.add_subparsers(title='Commands')

    p_full_sync = subs.add_parser('full_sync', help='export the json output' +
                                                    ' of the sync endpoint')
    p_full_sync.set_defaults(func=full_sync)

    args = parser.parse_args()
    if not args.func:
        parser.print_help()
        return
    args.func(args)
