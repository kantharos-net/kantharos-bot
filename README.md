<!--
 Copyright 2022 andremmfaria

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->

# Kantharos-bot

A Discord bot with fun and helpful commands:

- E-sports matches from Pandascore
- Basic music features (YouTube)
- Jokes, insults, and random facts
- Simple chat powered by OpenAI

The entry point is `kantharos_bot.main:main`, which starts the bot defined in `kantharos_bot.bot`. Configuration is handled with Dynaconf via `kantharos_bot.utils.config.settings`.

## Features

Commands (prefix: `.`):

- Voice
    - `.join` — join the author’s voice channel
    - `.leave` — leave the current voice channel
    - `.music <youtube_url>` — show YouTube video info (title, channel, duration)
    - `.play <youtube_url>` — download and play audio via FFmpeg + youtube-dl
    - `.pause` / `.resume` / `.stop` — control playback
- Content
    - `.joke [lang] [search]` — random jokes via JokeAPI
    - `.insult [lang]` — insult via Evil Insult Generator
    - `.fact [lang]` — random true fact
- E-sports
    - `.matches [game_name] [matches_max]` — upcoming/running matches from Pandascore
- Chat
    - `.chat <prompt>` — ask ChatGPT (OpenAI)
    - `.chat clear` — clear local chat history

Modules of interest:

- Voice/music: `kantharos_bot/commands/music_stream.py`, `kantharos_bot/utils/yt_source.py`
- Content: `kantharos_bot/commands/joke.py`, `kantharos_bot/commands/insult.py`, `kantharos_bot/commands/fact.py`
- E-sports: `kantharos_bot/commands/esports_match.py`
- Chat: `kantharos_bot/commands/chat.py`

## Requirements

- Python >= 3.13
- FFmpeg (required for voice/music)
- Tokens/keys:
    - Discord bot token (required)
    - Pandascore token (for `.matches`)
    - OpenAI token (for `.chat`)

## Configuration

Base settings live in `config/settings.toml`. Secrets come from `config/.secrets.toml` (do not commit). Dynaconf also supports environment variables prefixed with `KANTHAROS_BOT_` (e.g., `KANTHAROS_BOT_DISCORD_TOKEN`).

Copy and fill secrets:

```bash
cp config/.secrets_template.toml config/.secrets.toml
# Edit config/.secrets.toml with your tokens:
# pandascore_token, discord_token, openai_token
```

Optionally set environment variables:

```bash
export KANTHAROS_BOT_DISCORD_TOKEN="..."
export KANTHAROS_BOT_PANDASCORE_TOKEN="..."
export KANTHAROS_BOT_OPENAI_TOKEN="..."
```

Help strings are loaded from `help_texts/` by `kantharos_bot.utils.load_help.load_help`.

## Install

This project uses PDM (see `pyproject.toml`).

```bash
pdm install
```

Ensure FFmpeg is installed on your system for voice playback.

## Run

```bash
pdm run kantharos-bot
```

The CLI invokes `kantharos_bot.main:main`, which sets up logging and runs the bot.

## Usage

- Invite the bot with proper permissions (including voice/connect/speak).
- In a text channel:
    - Voice
        - `.join`, then `.play <youtube_url>` to start playback
        - Use `.pause`, `.resume`, `.stop`, and `.leave` accordingly
    - Content
        - `.joke en banana`
        - `.insult pt`
        - `.fact en`
    - E-sports
        - `.matches dota-2 5`
    - Chat
        - `.chat how do I bake bread?`
        - `.chat clear` to reset local history

Notes:

- Music playback depends on FFmpeg and youtube-dl/pytube. Large or geo-blocked content may fail.
- Chat history is stored at `openchat.temp_file_path` (`/tmp/chat_history` by default) and auto-cleans when exceeding `openchat.history_max_size`.

## Development

Formatting and linting:

```bash
pdm run isort .
pdm run black .
pdm run pylint ./**/*.py
```

Tests and coverage:

```bash
pdm run pytest
pdm run coverage run -m pytest
pdm run coverage report
```

There is a minimal version test in `tests/test_kantharos_bot.py` checking `kantharos_bot.__version__`.

Pre-commit:

```bash
pdm run pre-commit run --all-files
```

## Docker

A reproducible image is defined in `Dockerfile` (Alpine + FFmpeg). Build and run:

```bash
docker build -t kantharos-bot .
docker run --rm \
    -e KANTHAROS_BOT_DISCORD_TOKEN="..." \
    -e KANTHAROS_BOT_PANDASCORE_TOKEN="..." \
    -e KANTHAROS_BOT_OPENAI_TOKEN="..." \
    kantharos-bot
```

## License

See [LICENSE.md](LICENSE.md).
