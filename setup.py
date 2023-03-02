from setuptools import setup
from pathlib import Path

# Load README from README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="yokkaichi",
    version="1.2",
    description="Shodan-like server scanner for Minecraft (formely mcserverscanner)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Oreeeee",
    url="https://github.com/Oreeeee/yokkaichi",
    install_requires=[
        "colorama",
        "mcstatus",
        "ip2location",
        "python-masscan",
        "requests",
    ],
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
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
