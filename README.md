# exporteer\_todoist

This is a very simple tool for exporting data from Todoist via their API.

## Getting Started

1. Install python3 and pip
2. `git clone https://github.com/debfx/exporteer_todoist.git`
3. `pip install requests`
4. [Look up your API token](https://todoist.com/prefs/integrations)

To download the latest backup (i.e., what you would get by going to 'Backups' in 'Settings' in Todoist) as a zip file:

```bash
export TODOIST_API_TOKEN=your_token_here
python3 -m exporteer_todoist latest_backup --output backup.zip
```

To include all file attachments in the zip file backup:

```bash
export TODOIST_API_TOKEN=your_token_here
python3 -m exporteer_todoist latest_backup --output backup.zip --attachments
```

To download JSON representing a [full sync](https://developer.todoist.com/sync/v9/#sync):

```bash
export TODOIST_API_TOKEN=your_token_here
python3 -m exporteer_todoist full_sync --output backup.json
```

Note that the latter is essentially equivalent to just running this curl command:

```bash
curl https://api.todoist.com/sync/v9/sync \
    -H 'Bearer: your_token_here' \
    -d sync_token='*' \
    -d resource_types='["all"]' \
    > backup.json
```

## Development

Setup:

1. Install python3 and pip
2. Clone the repo
3. I recommend creating a venv:
    ```bash
    cd exporteer_todoist
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Install dependencies:
    ```bash
   pip install .
   pip install -r requirements-dev.txt
    ```

To run integration tests (these will download real data from your Todoist account, so a token is required):

```bash
export TODOIST_API_TOKEN=your_api_token
PYTHONPATH=src pytest
```

(Overriding PYTHONPATH as shown ensures the tests run against the code in the src/ directory rather than the installed copy of the package.)

To run the CLI:

```bash
export TODOIST_API_TOKEN=your_api_token
PYTHONPATH=src python -m exporteer_todoist ...
```

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/brokensandals/exporteer_todoist.

## License

This is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
