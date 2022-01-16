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

from asyncio import AbstractEventLoop, get_event_loop
from typing import Any, Dict

from discord import PCMVolumeTransformer
from discord.player import AudioSource
from kantharos_bot.utils.load_config import load_config
from youtube_dl import YoutubeDL

ytdl: YoutubeDL = YoutubeDL(load_config("youtube_dl_cfg")["ytdl_format_options"])


class YTDLSource(PCMVolumeTransformer):
    def __init__(self, source: AudioSource, *, data: Dict[str, Any], volume: float = 0.5):
        super().__init__(source, volume)
        self.data: Dict[str, Any] = data
        self.title: str = data.get("title")
        self.url: str = ""

    @classmethod
    async def from_url(
        cls, url: str, *, loop: AbstractEventLoop = None, stream: str = False
    ) -> str:

        loop: AbstractEventLoop = loop or get_event_loop()
        data: Dict[str, Any] = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            # take first item from a playlist
            data: Dict[str, Any] = data["entries"][0]

        return data["title"] if stream else ytdl.prepare_filename(data)
