from setuptools import setup

setup(
    name="yokkaichi",
    version="1.0",
    description="Shodan-like server scanner for Minecraft (Formely mcserverscanner)",
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
