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

import ssl
import json
import base64
import websocket
from samsung_ru7179_remote.config import load_config


def execute_keypress(key_command: str):
    """
    Executes a keypress on the TV
    A valid token must be in the configuration file
    :param key_command: The command to send. Should be one of the strings in
                        the valid_keys set in the commands module
    """
    config = load_config()

    app_name = config["remote_name"]
    app_name = str(base64.b64encode(app_name.encode("utf-8")), "utf-8")

    url = \
        "wss://{}:8002/api/v2/channels/samsung.remote.control?name={}&token={}"
    url = url.format(config["tv_ip"], app_name, config["token"])

    socket = websocket.create_connection(
        url, sslopt={"cert_reqs": ssl.CERT_NONE}
    )

    command = {
        "method": "ms.remote.control",
        "params": {
            "Cmd": "Click",
            "Option": "false",
            "TypeOfRemote": "SendRemoteKey",
            "DataOfCmd": "KEY_" + key_command
        }
    }
    socket.send(json.dumps(command))
    socket.close()
