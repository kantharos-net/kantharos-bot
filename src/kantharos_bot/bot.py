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

from discord import Client, Intents
from discord.ext.commands import Bot
from discord.ext.commands.context import Context
from kantharos_bot.utils.config import settings

intents = Intents.all()
client = Client(intents=intents)
bot_client = Bot(command_prefix=".", intents=intents)


@bot_client.event
async def on_ready():
    from kantharos_bot.commands import (  # noqa F811
        chat,
        esports_match,
        fact,
        insult,
        joke,
        music_stream,
    )

    print(f"Logged in as {bot_client.user.name} - {bot_client.user.id}")


@bot_client.command(name="join", help="Tells the bot to join the voice channel")
async def join(ctx: Context):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot_client.command(name="leave", help="To make the bot leave the voice channel")
async def leave(ctx: Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


def run_bot() -> None:
    bot_client.run(settings.discord_token)
