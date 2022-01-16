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

import logging
from datetime import datetime as dt
from datetime import timedelta as td
from typing import Any, Dict, List

import pytz
from discord.ext.commands.context import Context
from fuzzywuzzy import fuzz
from kantharos_bot.bot.bot import bot
from kantharos_bot.utils.load_config import load_config
from kantharos_bot.utils.load_help import load_help
from pandascore import Client


@bot.command(name="matches", help=load_help("matches"))
async def matches(ctx: Context, game: str = "dota-2", matches_max: int = 10):
    cfg: Dict[str, Any] = load_config()

    fuzzy_scores: List[float] = [fuzz.ratio(item["slug"], game) for item in cfg["games"]]
    max_score_index: int = fuzzy_scores.index(max(fuzzy_scores))

    log_string: List[str] = [
        f'Selected game: {cfg["games"][max_score_index]["slug"]}',
        f'Selected game id: {cfg["games"][max_score_index]["id"]}',
    ]
    logging.info(" ; ".join(log_string))

    ps_client = Client(access_token=cfg["pandascore_token"])

    now: dt = dt.now()
    range_end: str = (now + td(days=10)).strftime(cfg["default_datetime_format"])
    range_begin: str = (now + td(hours=-3)).strftime(cfg["default_datetime_format"])

    response_data: List[Dict[str, Any]] = ps_client.all_games.get_matches(
        filter=f'videogame={cfg["games"][max_score_index]["slug"]};finished=false',
        range=f"scheduled_at={range_begin},{range_end}",
        sort="begin_at",
    )

    if response_data:
        matches_message = ["Upcoming and running matches: "]
        for item in response_data:
            if item["begin_at"]:
                utc_time: dt = pytz.utc.localize(
                    dt.strptime(item["begin_at"], cfg["default_datetime_format"])
                )
                bst_time: str = utc_time.astimezone(
                    pytz.timezone(cfg["default_timezone"])
                ).strftime("%d/%m/%Y %H:%M Brazil time")
            else:
                bst_time: str = "No match time defined yet"

            m_pat: str = "{league_n} - {tournm_n} - {status}\n{match_n}\n{time}\n{stream_url}\n"
            matches_message.append(
                m_pat.format(
                    league_n=item["league"]["name"],
                    tournm_n=item["tournament"]["name"],
                    status=item["status"].title().replace("_", " "),
                    match_n=item["name"],
                    time=bst_time,
                    stream_url=item["official_stream_url"],
                )
            )

        response = "\n".join(matches_message[:matches_max])
    else:
        response = "No matches found"

    await ctx.send(response)
