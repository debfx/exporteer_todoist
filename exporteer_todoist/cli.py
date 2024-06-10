"""Command-line interface for exporteer_todoist tool."""


import argparse
import csv
import io
import json
import os
import re
import requests
import sys
import typing
import zipfile
from operator import itemgetter


class AttachmentInfo(typing.NamedTuple):
    name: str
    url: str


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

    if args.output == '-':
        output_file = sys.stdout
    else:
        output_file = open(args.output, 'w')

    output_file.write(resp.text)

    return 0


def _extract_attachments(csv_bytes: bytes) -> list[AttachmentInfo]:
    attachments = []

    csv_reader = csv.DictReader(csv_bytes.decode().split('\n'))
    for row in csv_reader:
        for match in re.finditer(r'\[\[file\s+({.*?})\]\]', row['CONTENT']):
            attachment_data = json.loads(match.group(1))
            attachment_info = AttachmentInfo(name=attachment_data['file_name'], url=attachment_data['file_url'])
            if attachment_info.url.startswith('https://files.todoist.com/'):
                attachments.append(attachment_info)

    return attachments


def _backup_attachments(backup_file, download_headers) -> None:
    backup_file.seek(0)
    zip_file = zipfile.ZipFile(backup_file, mode='a')

    for path in zip_file.namelist():
        if not path.endswith('.csv'):
            continue

        # strip .csv file extension
        project_name = path[:-4]

        with zip_file.open(path, mode='r') as file_csv:
            attachments = _extract_attachments(file_csv.read())

        for attachment in attachments:
            resp = requests.get(attachment.url, headers=download_headers)
            with zip_file.open(f'attachments/{project_name}/{attachment.name}', mode='w') as file_attachment:
                file_attachment.write(resp.content)


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
        output_file = io.BytesIO()
    else:
        output_file = open(args.output, 'w+b')

    url = versions[0]['url']
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    output_file.write(resp.content)

    if args.attachments:
        _backup_attachments(output_file, headers)

    if args.output == '-':
        sys.stdout.buffer.write(output_file.getbuffer())
        sys.stdout.buffer.flush()

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
    p_full_sync.add_argument('--output', '-o', default='-',
                             help='path to write the json file to (defaults to "-" for stdout)')
    p_full_sync.set_defaults(func=_full_sync)

    p_latest_backup = subs.add_parser('latest_backup',
                                      help='download latest backup zip')
    p_latest_backup.add_argument('--output', '-o', default='-',
                                 help='path to write the zip file to (defaults to "-" for stdout)')
    p_latest_backup.add_argument('--attachments', action='store_true',
                                 help='Download attachments in addition to the task CSVs')
    p_latest_backup.set_defaults(func=_latest_backup)

    args = parser.parse_args(args)
    if not args.func:
        parser.print_help()
        return 1
    return args.func(args)
