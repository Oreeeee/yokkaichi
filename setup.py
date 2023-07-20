import sys
from pathlib import Path

from setuptools import setup

from yokkaichi import __version__ as yokkaichi_ver

# Load README from README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Enforce Python version (3.8+)
if sys.version_info[1] < 8:
    print(
        "NOTICE: Yokkaichi requires Python 3.8 or newer to run. Python 3.7 and older are not supported, and bugs might happen."
    )

setup(
    name="yokkaichi",
    version=yokkaichi_ver,
    description="Shodan-like server scanner for Minecraft (formely mcserverscanner)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Oreeeee",
    license="MIT",
    url="https://github.com/Oreeeee/yokkaichi",
    install_requires=[
        "rich==13.4.2",
        "mcstatus==11.0.0",
        "IP2Location==8.10.0",
        "tomli==2.0.1",
        "pyScannerWrapper==0.2.0",
    ],
    extras_require={"testing": ["pytest"]},
    entry_points={"console_scripts": ["yokkaichi=yokkaichi.__main__:main"]},
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    packages=[
        "yokkaichi",
        "yokkaichi.constants",
        "yokkaichi.structs",
        "yokkaichi.enums",
    ],
)
