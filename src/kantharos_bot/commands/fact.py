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


from typing import Any, Dict

import requests
from discord.ext.commands.context import Context
from kantharos_bot.bot import bot_client
from kantharos_bot.utils.config import settings
from kantharos_bot.utils.load_help import load_help
from kantharos_bot.utils.logging import logging


@bot_client.command(name="fact", help=load_help("fact"))
async def fact(ctx: Context, lang: str = "en"):
    response = requests.get(f"{settings.facts_url}?language={lang}").json()

    fact: str = f"Here is your fact:\n{response['text']}\nFact URL: {response['permalink']}"

    logging.info(fact)

    await ctx.send(fact)
