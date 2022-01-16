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
import os.path as op

HELP_TEXT_PATH: str = "../../../help_texts"


def load_help(message_to_load: str) -> str:
    cfg_path: str = op.join(op.dirname(op.abspath(__file__)), HELP_TEXT_PATH, f"{message_to_load}")
    logging.info(f"Loading config file on path {cfg_path}")
    with open(cfg_path, "r") as f:
        text: str = f.read()

    return text
