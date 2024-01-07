from litestar import Litestar
from litestar.static_files.config import StaticFilesConfig

app = Litestar(
    static_files_config=[
        StaticFilesConfig(directories=["www"], path="/", html_mode=True)
    ]
)
