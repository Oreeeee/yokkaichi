import sys
from pathlib import Path

from setuptools import setup

from yokkaichi import __version__ as yokkaichi_ver

# Load README from README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Enforce Python version (3.8+)
if sys.version_info[1] < 8:
    sys.exit(
        "Yokkaichi will NOT run on Python 3.7 and older. You can build the package yourself and remove the check, but don't report bugs that happen!"
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
        "rich",
        "mcstatus",
        "ip2location",
        "python-masscan",
        "requests",
        "tomli >= 1.1.0",
    ],
    extras_require={"testing": ["pytest"]},
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
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
