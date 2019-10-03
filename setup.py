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
from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="samsung-ru7179-remote",
        version=open("version", "r").read(),
        description="A remote for Samsung RU7179 TVs",
        long_description=open("README.md", "r").read(),
        long_description_content_type="text/markdown",
        author="Hermann Krumrey",
        author_email="hermann@krumreyh.com",
        classifiers=[
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        ],
        url="https://gitlab.namibsun.net/"
            "namibsun/python/samsung-ru7179-remote",
        license="GNU GPL3",
        packages=find_packages(),
        scripts=list(map(lambda x: os.path.join("bin", x), os.listdir("bin"))),
        install_requires=[
            "typing",
            "websockets"
        ],
        test_suite='nose.collector',
        tests_require=['nose'],
        include_package_data=True,
        zip_safe=False
    )
