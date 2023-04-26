from setuptools import setup
from pathlib import Path
import sys

# Load README from README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Get version from yokkaichi/_version.py
with open("yokkaichi/_version.py", "r") as f:
    file_contents = f.read().strip()
    no_var_name = file_contents.replace("__version__ = ", "")
    version = no_var_name.replace('"', "")

# Enforce Python version (3.7+)
if sys.version_info[1] < 7:
    sys.exit(
        "Yokkaichi will NOT run on Python 3.6 and older. You can build the package yourself and remove the check, but don't report bugs that happen!"
    )

setup(
    name="yokkaichi",
    version=version,
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
    ],
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
    packages=["yokkaichi"],
)
