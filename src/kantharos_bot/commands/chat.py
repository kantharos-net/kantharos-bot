# Copyright 2023 andremmfaria
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

import os
import pathlib
from typing import Dict, List

import openai
from discord.ext.commands.context import Context
from kantharos_bot.bot import bot_client
from kantharos_bot.utils.config import settings
from kantharos_bot.utils.load_help import load_help
from kantharos_bot.utils.logging import logging


@bot_client.command(name="chat", help=load_help("chat"))
async def chat(ctx: Context, *prompt: str):
    openai.api_key = settings.openai_token

    clean = False
    prompt_string = " ".join(prompt)
    temp_file = pathlib.Path(settings.openchat.temp_file_path)

    if prompt_string == settings.openchat.clean_history_command:
        logging.info("History clean command given")
        temp_file.unlink(missing_ok=True)  # Deletes temp file if clean history command is given
        clean = True
    else:
        if temp_file.exists():
            logging.info("History file exists. Reading it for context.")
            with open(temp_file.resolve(), mode="r") as fp:
                assistant_content = fp.read()
        else:
            logging.info(f"History file not found. Creating history file {temp_file.resolve()}.")
            open(temp_file.resolve(), mode="a").close()  # Creates temp file if it does not exist
            assistant_content = f"{settings.openchat.default_assistant_content} \n\n"

        with open(temp_file.resolve(), mode="a") as fp:
            fp.write(f"{prompt_string} \n\n")

    if not clean:
        prompt_list: List[Dict[str, str]] = [
            {"role": "user", "content": prompt_string},
            {"role": "system", "content": settings.openchat.default_system_content},
            {"role": "assistant", "content": assistant_content},
        ]

        async with ctx.typing():
            completion = await openai.ChatCompletion.acreate(
                model=settings.openchat.default_model,
                messages=prompt_list,
            )

        content: str = completion.choices[0].message.content

        with open(temp_file.resolve(), mode="a") as fp:
            fp.write(f"{content} \n\n")

        logging.info(completion.__str__())

        await ctx.send(content)
    else:
        await ctx.send("Chat history cleaned")

    if (
        temp_file.exists()
        and os.path.getsize(settings.openchat.temp_file_path) > settings.openchat.history_max_size
    ):
        logging.info(
            f"History file reached max size of {settings.openchat.history_max_size} bytes. Deleting."
        )
        temp_file.unlink(missing_ok=True)  # Deletes temp file if it reaches max size
        await ctx.send(
            "\n".join(
                [
                    f"History file reached max size of {settings.openchat.history_max_size} bytes.",
                    "It has been deleted. Please restart the prompt chain.",
                ]
            )
        )
