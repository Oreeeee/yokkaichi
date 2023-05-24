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
- Query integration

### Planned features (not in a specific order)
- WWW interface
- Bot joining the servers
- Cleaning up the code
- Docker support
- Optimization
- Scanning for pre-Netty (<1.7) servers

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
1. Using a config file
Instead of passing in arguments, you can pass the configuration file with `--config` argument. When no additional file name is provided, Yokkaichi will use `yokkaichi.toml` for the file name. When the config file name you provided doesn't exist, Yokkaichi will create an example file for you. Modify it how you like and rerun Yokkaichi. Configuration files are not forwards or backwards compatible and you will have to adjust it every major change. 
2. You can also use this script by passing in arguments in the CLI. You can get the list of availible options by invoking `python -m yokkaichi -h`.

### Using the masscan integration
You need to have [masscan](https://github.com/robertdavidgraham/masscan) in your PATH, or in the same directory from which you are running this software. Make sure that the binary is named `masscan` (Unix) or `masscan.exe` (Windows).
