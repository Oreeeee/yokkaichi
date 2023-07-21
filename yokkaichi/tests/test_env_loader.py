import yokkaichi.env_loader
from yokkaichi.structs import EnvVariables

FAKE_TOKEN = "dummy"


def test_getting_variables(monkeypatch):
    def mock_os_environ_get(var_name: str):
        if var_name == "IP2LOCATION_LITE_TOKEN":
            return "dummy"

    monkeypatch.setattr("os.environ.get", mock_os_environ_get)

    assert yokkaichi.env_loader.load_env() == EnvVariables(
        ip2location_lite_token=FAKE_TOKEN
    )
