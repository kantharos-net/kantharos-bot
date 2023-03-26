# Copyright 2022 andremmfaria
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime as dt
from datetime import timedelta as td
from typing import Any, Dict, List

import pytz
from discord.ext.commands.context import Context
from fuzzywuzzy import fuzz
from kantharos_bot.bot import bot_client
from kantharos_bot.utils.config import settings
from kantharos_bot.utils.load_help import load_help
from kantharos_bot.utils.logging import logging
from pandascore import Client


@bot_client.command(name="matches", help=load_help("matches"))
async def matches(ctx: Context, game_name: str = "dota-2", matches_max: int = 10):
    fuzz_score = 0
    for game_slug in settings.games.keys():
        temp = fuzz.ratio(game_slug, game_name)
        if temp > fuzz_score:
            fuzz_score = temp
            game_slug_selected = game_slug

    log_string: List[str] = [
        f"Game: {game_slug_selected}",
        f"Game id: {settings.games.get(game_slug_selected)}",
    ]
    logging.info(" ; ".join(log_string))

    ps_client = Client(access_token=settings.pandascore_token)

    now: dt = dt.now()
    range_end: str = (now + td(days=10)).strftime(settings.default_datetime_format)
    range_begin: str = (now + td(hours=-3)).strftime(settings.default_datetime_format)

    response_data: List[Dict[str, Any]] = ps_client.all_games.get_matches(
        filter=f"videogame={game_slug_selected};finished=false",
        range=f"scheduled_at={range_begin},{range_end}",
        sort="begin_at",
    )

    if response_data:
        matches_message = ["Upcoming and running matches: "]
        for item in response_data:
            if item["begin_at"]:
                utc_time: dt = pytz.utc.localize(
                    dt.strptime(item["begin_at"], settings.default_datetime_format)
                )
                bst_time: str = utc_time.astimezone(
                    pytz.timezone(settings.default_timezone)
                ).strftime("%d/%m/%Y %H:%M Brazil time")
            else:
                bst_time: str = "No match time defined yet"

            official_stream_url = next(
                (stream["raw_url"] for stream in item["streams_list"] if stream["main"]),
                "No official stream url",
            )

            m_pat: str = "{league_n} - {tournm_n} - {status}\n{match_n}\n{time}\n{stream_url}\n"
            matches_message.append(
                m_pat.format(
                    league_n=item["league"]["name"],
                    tournm_n=item["tournament"]["name"],
                    status=item["status"].title().replace("_", " "),
                    match_n=item["name"],
                    time=bst_time,
                    stream_url=f"<{official_stream_url}>",
                )
            )

        response = "\n".join(matches_message[:matches_max])
    else:
        response = "No matches found"

    await ctx.send(response)
