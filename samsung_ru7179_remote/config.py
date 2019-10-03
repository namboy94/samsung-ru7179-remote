"""LICENSE
Copyright 2019 Hermann Krumrey <hermann@krumreyh.com>

This file is part of samsung-ru7179-remote.

samsung-ru7179-remote is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

samsung-ru7179-remote is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with samsung-ru7179-remote.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import os
import json
from typing import Dict

config_dir = os.path.join(
    os.path.expanduser("~"),
    ".config/samsung-ru7179-remote"
)
"""
The config directory path
"""

config_file = os.path.join(config_dir, "config.json")
"""
The config file path
"""


def load_config() -> Dict[str, str]:
    """
    Loads the config
    :return: The config
    """
    if not os.path.isfile(config_file):
        print("Configuration invalid. Please run the init command")
        exit(1)

    with open(config_file, "r") as f:
        return json.load(f)


def write_config(config: Dict[str, str]):
    """
    Writes the config
    :param config: The config to write
    :return: None
    """
    with open(config_file, "w") as f:
        json.dump(config, f)
