## Yokkaichi (formely mcserverscanner) - Shodan-like server scanner for Minecraft.

## Renaming notice!
This project used to be named mcserverscanner, but on 2023-01-15 it got renamed to Yokkaichi.

### Features
- Scanning for Java and Bedrock servers
- Masscan integration
- IP2Location integration
- Query integration

### Planned features
- WWW interface
- Bot joining the servers
- Cleaning up the code

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
You can use this script by invoking `python -m yokkaichi` and passing in arguments in the CLI. You can get the list of availible options by invoking `python -m yokkaichi -h`

### Example
`python -m yokkaichi --java --masscan --masscan-countries US CA CN -p 25565 25566 --ip2location-db data/IP2LOCATION-LITE-DB11.BIN --ip2location-cache --output data/servers.json`

### Big Thanks
- [herrbischoff/country-ip-blocks](https://github.com/herrbischoff/country-ip-blocks) for providing CIDR blocks for countries
- [IP2Location](https://www.ip2location.com/) and [IP2Location Lite](https://lite.ip2location.com/) for providing accurate offline IP to Location service.