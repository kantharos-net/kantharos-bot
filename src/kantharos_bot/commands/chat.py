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

    if temp_file.exists():
        if prompt_string == settings.openchat.clean_history_command:
            logging.info("History clean command given")
            temp_file.unlink(missing_ok=True)  # Deletes temp file if clean history command is given
            clean = True
        else:
            logging.info("File exists")
            with open(temp_file.resolve(), mode="r") as fp:
                assistant_content = fp.readlines()

            assistant_content.insert(0, settings.openchat.default_assistant_content)
    else:
        logging.info(f"History file not found. Creating history file {temp_file.resolve()}")
        open(temp_file.resolve(), mode="a").close()  # Creates temp file if it does not exist
        assistant_content = [settings.openchat.default_assistant_content]

    if not clean:
        prompt_list: List[Dict[str, str]] = [
            {"role": "user", "content": prompt_string},
            {"role": "system", "content": settings.openchat.default_system_content},
            {"role": "assistant", "content": "\n".join(assistant_content)},
        ]

        async with ctx.typing():
            completion = await openai.ChatCompletion.acreate(
                model=settings.openchat.default_model,
                messages=prompt_list,
            )

        content: str = completion.choices[0].message.content

        with open(temp_file.resolve(), mode="w") as fp:
            fp.write(f"{content}")

        logging.info(completion.__str__())

        await ctx.send(content)
    else:
        await ctx.send("Chat history cleaned")
