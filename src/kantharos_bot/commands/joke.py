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

from typing import Coroutine, List

from discord.ext.commands.context import Context
from jokeapi import Jokes
from kantharos_bot.bot import bot_client
from kantharos_bot.utils.load_help import load_help


@bot_client.command(name="joke", help=load_help("joke"))
async def joke(ctx: Context, lang: str = "en", search: str = None):
    jk_obj = await Jokes()

    joke: Coroutine = await jk_obj.get_joke(response_format="json", search_string=search, lang=lang)

    template: str = "Here is your joke:\n{ask}\n{punchline}"

    if joke["error"] is True:
        response: str = template.format(ask=joke["message"], punchline=", ".join(joke["causedBy"]))
    elif joke["type"] == "single":
        response: str = template.format(ask=joke["joke"], punchline="")
    else:
        response: str = template.format(ask=joke["setup"], punchline=joke["delivery"])

    await ctx.send(response)
