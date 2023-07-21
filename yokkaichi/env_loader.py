import os

from .structs import EnvVariables


def load_env() -> EnvVariables:
    env_vars: EnvVariables = EnvVariables()

    env_vars.ip2location_lite_token = os.environ.get("IP2LOCATION_LITE_TOKEN")

    return env_vars
