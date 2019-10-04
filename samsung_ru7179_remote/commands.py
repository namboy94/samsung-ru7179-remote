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


valid_keys = {
    # Power Keys
    "POWER",

    # Sources
    "SOURCE",
    "HDMI",
    "TV",

    # Numbers
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",

    # Channels
    "CHUP",
    "CHDOWN",
    "PRECH",
    "CH_LIST",

    # Volume Keys
    "VOLUP",
    "VOLDOWN",
    "MUTE",

    # Direction Keys
    "UP",
    "DOWN",
    "RIGHT",
    "LEFT",
    "ENTER",
    "RETURN",

    # Media Keys
    "REWIND",
    "STOP",
    "PAUSE",
    "PLAY",
    "FF",

    # Color Keys
    "GREEN",
    "YELLOW",
    "CYAN",
    "RED",
    
    # Menus
    "MENU",
    "HOME",
    "GUIDE"
}
"""
Valid keypresses
"""


shortcuts = {
    "HDMI1": [
        "SOURCE", "SOURCE",
        "LEFT", "LEFT", "LEFT",
        "RIGHT",
        "ENTER"
    ],
    "HDMI2": [
        "SOURCE", "SOURCE",
        "LEFT", "LEFT", "LEFT",
        "RIGHT", "RIGHT",
        "ENTER"
    ],
    "HDMI3": [
        "SOURCE", "SOURCE",
        "LEFT", "LEFT", "LEFT",
        "RIGHT", "RIGHT", "RIGHT",
        "ENTER"
    ]
}
"""
Custom commands that use multiple commands
"""

for shortcut in shortcuts:
    valid_keys.add(shortcut)
