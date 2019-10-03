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
import time
import json
import base64
import websocket
from threading import Thread
from samsung_ru7179_remote.config import load_config, write_config


def authenticate():
    """
    Authenticates the system with the TV
    :return: None
    """
    config = load_config()
    config["token"] = ""

    app_name = config["remote_name"]
    app_name = str(base64.b64encode(app_name.encode("utf-8")), "utf-8")
    url = "wss://{}:8002/api/v2/channels/samsung.remote.control?name={}"\
        .format(config["tv_ip"], app_name)

    def on_message(socket: websocket.WebSocket, message: str):
        config["token"] = json.loads(message)["data"]["token"]
        socket.close()

    def on_open(socket: websocket.WebSocket):
        def run(*_):
            start = time.time()
            socket.send("Hello!")
            while time.time() - start < 10 and config["token"] == "":
                time.sleep(1)
            socket.close()
        Thread(target=run).start()

    websocket.WebSocketApp(
        url,
        on_message=on_message,
        on_open=on_open
    ).run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    if config["token"] == "":
        print("Authentication unsuccessful")
    else:
        print("Authentication successful")
        write_config(config)
