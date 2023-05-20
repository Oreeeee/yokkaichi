import yokkaichi.port_parser


def test_parse_port_range():
    assert yokkaichi.port_parser.parse_port_range(
        "25560-25563,25567,25569-25571,49999"
    ) == [25560, 25561, 25562, 25563, 25567, 25569, 25570, 25571, 49999]


def test_parse_port_range_duplicates():
    assert yokkaichi.port_parser.parse_port_range("25563-25566,25565") == [
        25563,
        25564,
        25565,
        25566,
    ]
