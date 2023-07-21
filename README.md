<div align="center">

# Yokkaichi (formely mcserverscanner) - Shodan-like server scanner for Minecraft.
![downloads](https://img.shields.io/pypi/dm/yokkaichi) ![issues](https://img.shields.io/github/issues/Oreeeee/yokkaichi) ![pull requests](https://img.shields.io/github/issues-pr/Oreeeee/yokkaichi) ![license](https://img.shields.io/github/license/Oreeeee/yokkaichi) ![release](https://img.shields.io/github/v/release/Oreeeee/yokkaichi) ![commits since release](https://img.shields.io/github/commits-since/Oreeeee/yokkaichi/latest) ![code style](https://img.shields.io/badge/code%20style-black-black) ![stars](https://img.shields.io/github/stars/Oreeeee/yokkaichi?style=social)
</div>

## Renaming notice!
This project used to be named mcserverscanner, but on 2023-01-15 it got renamed to Yokkaichi.

### Features
- Scanning for Java and Bedrock servers
- Masscan integration
- IP2Location integration

### Planned features (not in a specific order)
- WWW interface
- Bot joining the servers
- Docker support
- Scanning for pre-Netty (<1.7) servers
- Query integration

### Installation
#### Releases
- Installing the latest version with pipx (recommended)
```
pipx install yokkaichi --include-deps
yokkaichi -v
```
- Installing the latest version in a virtual environment
```
virtualenv .venv
source .venv/bin/activate # for Linux
.venv\bin\activate.bat # for Windows
pip install yokkaichi
yokkaichi -v
```
#### Development versions (not recommended!)
Check out [DEVELOPMENT_INSTALL.md](https://github.com/Oreeeee/yokkaichi/blob/master/DEVELOPMENT_INSTALL.md)

### 3rd party dependencies (optional)
- `masscan` (for faster scanning)

### Usage
When starting the script for the first time, `yokkaichi.toml` will get created. You will have to adjust it to your preferences. Optionally, you can also pass in `-c` to set a different name or location of the config file.

### How to get geolocating to work?
Yokkaichi uses IP2Location LITE for anything geolocation related. This includes getting the location of the server, and generating the CIDR ranges for scanning. It is a offline, free to use download, so there are no rate limits. However, the database is not redistributed with Yokkaichi, due to IP2Location updating their LITE databases every month. Instead, it will be downloaded and updated automatically everytime you run this script for the first time in the month. To get the downloading to work, you need to have an IP2Location LITE Download Token. To get one, follow these steps.

1. Go to [IP2Location LITE](https://lite.ip2location.com/) website and register (or log into) an account (which is completly free forever).
2. Click on the name in the upper right corner and select "Database Download".
3. Copy your Download Token.
4. Set the `IP2LOCATION_LITE_TOKEN` environment variable to your token.
5. Now, you will be able to use the automatic downloads feature.

### Using the masscan integration
You need to have [masscan](https://github.com/robertdavidgraham/masscan) in your PATH, or in the same directory from which you are running this software. Make sure that the binary is named `masscan` (Unix) or `masscan.exe` (Windows).
