from .constants import console


def parse_port_range(unparsed_args: str) -> list:
    def verify_ints(port: any) -> None:
        try:
            int(port)
        except TypeError:
            console.print(
                f"Couldn't parse: [bold white]{port}[/bold white]", style="red"
            )
            exit(1)

    ports: list[int] = []
    # Parse all separate port/ranges, separated by commas
    separate_values: list[str] = unparsed_args.split(",")
    # Parse all ranges
    for value in separate_values:
        # Check if it's a range
        if "-" in value:
            # Parse the range
            port_range: list[str] = value.split("-")
            range_start: str = port_range[0]
            range_end: str = port_range[1]
            for port in (range_start, range_end):
                verify_ints(port)
            for port in range(
                int(range_start), int(range_end) + 1
            ):  # Range end needs to be offset by 1 to make the range inclusive
                ports.append(port)
        else:
            verify_ints(value)
            ports.append(int(value))

    return list(sorted(set(ports)))
