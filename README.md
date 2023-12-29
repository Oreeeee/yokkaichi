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
- Docker support

### Planned features (not in a specific order)
- WWW interface
- Bot joining the servers
- Scanning for pre-Netty (<1.7) servers
- Query integration

### Installation
```
git clone https://github.com/Oreeeee/yokkaichi
git checkout tags/version # Select a specific tag here
sudo docker-compose up --force-recreate --build
```

### Usage
When starting the script for the first time, `yokkaichi.toml` will get created in the data directory. You will have to adjust it to your preferences. Then, you can just start the container.

### How to get geolocating to work?
Yokkaichi uses IP2Location LITE for anything geolocation related. This includes getting the location of the server, and generating the CIDR ranges for scanning. It is a offline, free to use download, so there are no rate limits. However, the database is not redistributed with Yokkaichi, due to IP2Location updating their LITE databases every month. Instead, you will have to update the database every month (you will get notified by Yokkaichi).
#### Getting a token
1. Go to IP2Location LITE website and register (or log into) an account (which is completly free forever).
2. Click on the name in the upper right corner and select "Database Download".
3. Copy your Download Token.
#### Updating the database
`python ip2l_updater.py TOKEN`
