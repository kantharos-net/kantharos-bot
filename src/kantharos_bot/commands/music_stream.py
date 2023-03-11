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
from typing import Any, Dict

from discord import FFmpegPCMAudio
from discord.ext.commands.context import Context
from kantharos_bot.bot import bot_client
from kantharos_bot.utils.config import settings
from kantharos_bot.utils.load_help import load_help
from kantharos_bot.utils.yt_source import YTDLSource
from pytube import YouTube


@bot_client.command(name="music", help=load_help("music"))
async def music(ctx: Context, link: str = ""):
    logging.info("Provided yt link: {}".format(link))
    logging.info("Config: {}".format(settings))

    if link == "":
        await ctx.send("Please provide a valid link")
        return

    video: YouTube = YouTube(link)

    m: str = "Video data:\nTitle: {title}\nChannel: {author}\nDuration: {length} seconds"
    response: str = m.format(
        title=video.title,
        author=video.author,
        length=video.length,
    )

    await ctx.send(response)


@bot_client.command(name="play", help="To play song")
async def play(ctx: Context, url: str):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot_client.loop)
            voice_channel.play(FFmpegPCMAudio(executable="ffmpeg", source=filename))
        await ctx.send("**Now playing:** {}".format(filename))
    except Exception as e:
        await ctx.send("The bot is not connected to a voice channel. Exception: {}".format(e))


@bot_client.command(name="pause", help="This command pauses the song")
async def pause(ctx: Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot_client.command(name="resume", help="Resumes the song")
async def resume(ctx: Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play command")


@bot_client.command(name="stop", help="Stops the song")
async def stop(ctx: Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
