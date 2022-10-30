# Minecraft server scanner - find Minecraft servers with port scanning!
## Usage
```
usage: mcserverscanner.py [-h] [-j] [-b] -l IP_LIST_FILE [-p PORTS] [-q] [-c CHECK_COUNTRY] [-t THREAD_COUNT] -o OUTPUT_FILE

options:
  -h, --help            show this help message and exit
  -j, --java            Scan for Java servers
  -b, --bedrock         Scan for Bedrock servers
  -l IP_LIST_FILE, --ip-list IP_LIST_FILE
                        Location to a file with IP addresses to scan
  -p PORTS, --ports PORTS
                        Ports to scan on
  -q, --query           Query servers, required for player list but slows down the script
  -c CHECK_COUNTRY, --check-country CHECK_COUNTRY
                        Check server location, provide IP2Location BIN database location
  -t THREAD_COUNT, --threads THREAD_COUNT
                        Number of threads (default: 100)
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        Output JSON file
```
## Example
`python mcserverscanner.py --java --ip-list data/ips.txt --ports 25565 --ports 25566 --check-country data/IP2LOCATION-LITE-DB1.BIN --output data/servers.json`