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
- Cleaning up the code
- Docker support
- Scanning for pre-Netty (<1.7) servers
- Query integration

### Installation
- Easy installation (from PyPI)
```
pip install yokkaichi
```
- Manual installation (from git)
```
git clone https://github.com/Oreeeee/yokkaichi
cd yokkaichi
pip install .
```

### Usage
When starting the script for the first time, `yokkaichi.toml` will get created. You will have to adjust it to your preferences. Optionally, you can also pass in `-c` to set a different name or location of the config file.


### Using the masscan integration
You need to have [masscan](https://github.com/robertdavidgraham/masscan) in your PATH, or in the same directory from which you are running this software. Make sure that the binary is named `masscan` (Unix) or `masscan.exe` (Windows).
