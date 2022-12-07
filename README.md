# Minecraft server scanner - find Minecraft servers with port scanning!
## Usage
```
usage: mcserverscanner.py [-h] [-j] [-b] [--ip-list IP_LIST] [--masscan] [--masscan-ip-list MASSCAN_IP_LIST] [--masscan-countries MASSCAN_COUNTRIES [MASSCAN_COUNTRIES ...]]
                          [--masscan-args MASSCAN_ARGS] [-p PORTS [PORTS ...]] [--query] [--ip2location-db CHECK_COUNTRY] [-t THREAD_COUNT] -o OUTPUT_FILE

options:
  -h, --help            show this help message and exit
  -j, --java            Scan for Java servers
  -b, --bedrock         Scan for Bedrock servers
  --ip-list IP_LIST     Location to IP List
  --masscan             Enable scanning with masscan
  --masscan-ip-list MASSCAN_IP_LIST
                        Location to IP (or CIDR) list to scan by masscan before scanning with mcserver scanner
  --masscan-countries MASSCAN_COUNTRIES [MASSCAN_COUNTRIES ...]
                        Countries to scan in 2-letter format
  --masscan-args MASSCAN_ARGS
                        Arguments for masscan (example: --max-rate 1000)
  -p PORTS [PORTS ...], --ports PORTS [PORTS ...]
                        Ports to scan on
  --query               Query servers, required for player list but slows down the script
  --ip2location-db CHECK_COUNTRY
                        Check server location, provide IP2Location BIN database location
  -t THREAD_COUNT, --threads THREAD_COUNT
                        Number of threads (default: 100)
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        Output JSON file
```
## Example
`python mcserverscanner.py --java --masscan --masscan-countries US -p 25565 25566 --ip2location data/IP2LOCATION-LITE-DB11.BIN --output data/servers.json`

## Big Thanks
- [herrbischoff/country-ip-blocks](https://github.com/herrbischoff/country-ip-blocks) for providing CIDR blocks for countries
- [IP2Location](https://www.ip2location.com/) and [IP2Location Lite](https://lite.ip2location.com/) for providing accurate offline IP to Location service.