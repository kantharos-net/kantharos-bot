# Copyright 2021 andremmfaria
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

import logging
from datetime import datetime as dt
from datetime import timedelta as td
from typing import Any, Dict, List

import pytz
from discord.ext.commands.context import Context
from fuzzywuzzy import fuzz
from kantharos_bot.bot import bot_client
from kantharos_bot.utils.config import settings
from kantharos_bot.utils.load_help import load_help
from pandascore import Client


@bot_client.command(name="tournaments", help=load_help("tournaments"))
async def tournaments(ctx: Context, game: str = "dota-2"):

    fuzzy_scores: List[float] = [fuzz.ratio(item["slug"], game) for item in settings["games"]]
    max_score_index: int = fuzzy_scores.index(max(fuzzy_scores))

    log_string: List[str] = [
        f'Selected game: {settings["games"][max_score_index]["slug"]}',
        f'Selected game id: {settings["games"][max_score_index]["id"]}',
    ]
    logging.info(" ; ".join(log_string))

    ps_client = Client(access_token=settings["pandascore_token"])

    now: dt = dt.now()
    range_end: str = (now + td(days=10)).strftime(settings["default_datetime_format"])
    range_begin: str = (now + td(hours=-3)).strftime(settings["default_datetime_format"])

    response_data: List[Dict[str, Any]] = ps_client.all_games.get_matches(
        filter=f'videogame={settings["games"][max_score_index]["slug"]};finished=false',
        range=f"scheduled_at={range_begin},{range_end}",
        sort="begin_at",
    )

    if response_data:
        matches_message = ["Running and upcoming matches: "]
        for item in response_data:
            utc_time: dt = pytz.utc.localize(
                dt.strptime(item["begin_at"], settings["default_datetime_format"])
            )
            bst_time: dt = utc_time.astimezone(pytz.timezone(settings["default_timezone"]))

            m_pat: str = "{league_n} - {tournm_n} - {status}\n{match_n}\n{time}\n{stream_url}\n"
            matches_message.append(
                m_pat.format(
                    league_n=item["league"]["name"],
                    tournm_n=item["tournament"]["name"],
                    status=item["status"].title().replace("_", " "),
                    match_n=item["name"],
                    time=bst_time.strftime("%d/%m/%Y %H:%M Brazil time"),
                    stream_url=item["official_stream_url"],
                )
            )

        response = "\n".join(matches_message)
    else:
        response = "No matches found"

    await ctx.send(response)
