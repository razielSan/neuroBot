from typing import List
from pathlib import Path

from pydantic import BaseModel


class SeleniumSettings(BaseModel):
    PATH_CHROME_DRIVER: Path = (
        Path(__file__).resolve().parent.parent
        / "static"
        / "files"
        / "browser_drivers"
        / "chromedriver_109"
        / "chromedriver.exe"
    )

    # USER_DATA_DIR: str = "--user-data-dir=C:\\Users\\name\\AppData\\Local\\Google\\Chrome\\User Data"
    USER_DATA_DIR: str = (
        r"user-data-dir=C:\Пользователи\Raz\AppData\Local\Google\Chrome\User Data"
    )
    USER_AGENT: str = (
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36"
    )  # user-agent
    PROFILE_DIRECTORY: str = "profile-directory=Default"  # тип профиля
    LOG_LEVEL: str = "--log-level=3"  # убираем лишние логи
    HEADLESS: str = "--headless=new"  # режим без интерфейса

    # Избегаем лишних окон/уведомлений
    DISABLE_GPU: str = "--disable-gpu"
    SANDBOX: str = "--no-sandbox"
    SHM_USAGE: str = "--disable-dev-shm-usage"
    LIST_ADD_ARGUMENT: List[str] = [
        USER_DATA_DIR,
        USER_AGENT,
        PROFILE_DIRECTORY,
        LOG_LEVEL,
        HEADLESS,
        DISABLE_GPU,
        SHM_USAGE,
        SANDBOX,
    ]
