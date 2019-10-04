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
import logging
import websocket
from typing import Dict, Any, Optional
from threading import Thread
from samsung_ru7179_remote.config import load_config, write_config

logger = logging.getLogger("samsung-ru7179-remote")


def control_tv(
        command: Dict[str, Any],
        wait_for_response: bool = False,
        timeout: int = 10
) -> Optional[Dict[str, Any]]:
    """
    Controls the TV.
    Authentication is automatically handled here as well
    :param command: The command to send
    :param wait_for_response: Waits for a response from the TV after connecting
    :param timeout: Time before a timeout is recognized
    :return: Potential response message from the TV
    """
    config = load_config()
    state = {
        "connected": False,
        "response": None
    }

    app_name = config["remote_name"]
    app_name = str(base64.b64encode(app_name.encode("utf-8")), "utf-8")

    url = \
        "wss://{}:8002/api/v2/channels/samsung.remote.control?name={}&token={}"
    url = url.format(config["tv_ip"], app_name, config["token"])

    def on_message(socket: websocket.WebSocket, message: str):
        """
        Handles messages from the TV
        This is where authentication and responses are handled
        :param socket: The websocket
        :param message: The received message
        :return: None
        """
        logger.debug(message)
        data = json.loads(message)

        if data["event"] in [
            "ms.remote.touchDisable",
            "ms.remote.touchEnable"
        ]:
            logger.info("Ignoring event {}".format(data["event"]))
            return

        if data["event"] == "ms.channel.connect":
            state["connected"] = True
            if "token" in data["data"]:
                config["token"] = data["data"]["token"]
                socket.close()
        else:
            state["response"] = data
            socket.close()

    def on_open(socket: websocket.WebSocket):
        """
        Sends the command over the websocket and checks for timeouts
        :param socket: The websocket
        :return: None
        """
        def run():
            logger.info("Websocket connected")
            start = time.time()
            socket.send(json.dumps(command))

            logger.debug("Waiting for connection...")
            while not state["connected"] and time.time() - start < timeout:
                time.sleep(0.1)

            if not state["connected"]:
                logger.warning("Connection timed out")

            if not wait_for_response or not state["connected"]:
                socket.close()

        Thread(target=run).start()

    websocket.WebSocketApp(
        url,
        on_message=on_message,
        on_open=on_open
    ).run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    write_config(config)
    return state["response"]


def execute_keypress(key_command: str):
    """
    Executes a remote keypress on the TV
    A valid token must be in the configuration file
    :param key_command: The command to send. Should be one of the strings in
                        the valid_keys set in the commands module
    """
    logger.info("Sending key {}".format(key_command))
    control_tv({
        "method": "ms.remote.control",
        "params": {
            "Cmd": "Click",
            "Option": "false",
            "TypeOfRemote": "SendRemoteKey",
            "DataOfCmd": "KEY_" + key_command
        }
    })


def start_app(app_name: str):
    """
    Starts an app on the TV
    :param app_name: The name of the app to start
    :return: None
    """
    apps = list_apps()

    try:
        app_id = str(apps[app_name])
        command = {
            "method": "ms.channel.emit",
            "params": {
                "event": "ed.apps.launch",
                "to": "host",
                "data": {
                    "appId": app_id,
                    "action_type": "NATIVE_LAUNCH"
                }
            }
        }
        control_tv(command)
        logger.info("Started app {}".format(app_name))
    except KeyError:
        logger.warning("App does not exist")


def list_apps() -> Dict[str, str]:
    """
    Lists available apps on the TV
    :return: A dictionary mapping app names to app IDs
    """
    resp = control_tv({
        "method": "ms.channel.emit",
        "params": {"event": "ed.installedApp.get", "to": "host"}
    }, wait_for_response=True)
    app_info = {}
    for app in resp["data"]["data"]:
        app_info[app["name"]] = app["appId"]
    return app_info
