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
from typing import Dict

import toml

DEFAULT_CONFIG_PARAM: str = "general_cfg"
CONFIG_PATH: str = "../../../config"
CONFIG_PARAM_FILE = "{}.toml"


def load_config(config_param: str = "") -> Dict[str, str]:
    if config_param:
        cfg_path: str = op.join(
            op.dirname(op.abspath(__file__)), CONFIG_PATH, CONFIG_PARAM_FILE.format(config_param)
        )
    else:
        cfg_path: str = op.join(
            op.dirname(op.abspath(__file__)),
            CONFIG_PATH,
            CONFIG_PARAM_FILE.format(DEFAULT_CONFIG_PARAM),
        )

    logging.info(f"Loading config file on path {cfg_path}")
    toml.load(cfg_path)

    return toml.load(cfg_path)
