from dotenv import load_dotenv, find_dotenv
from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    ENV: str = "DEV"
    SYSTEM_TYPE: str = 'AWS_MACHINE'

    PROJECT_DIR_NAME: str

    POSTGRESQL_USERNAME: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: int
    POSTGRESQL_DATABASE: str

    POSTGRESQL_LOCAL_USERNAME: str = ''
    POSTGRESQL_LOCAL_PASSWORD: str = ''
    POSTGRESQL_LOCAL_HOST: str = ''
    POSTGRESQL_LOCAL_PORT: int = ''
    POSTGRESQL_LOCAL_DATABASE: str = ''

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRESQL_USERNAME,
            password=self.POSTGRESQL_PASSWORD,
            host=self.POSTGRESQL_HOST,
            port=self.POSTGRESQL_PORT,
            path=self.POSTGRESQL_DATABASE,
        )

    @computed_field
    @property
    def LOCAL_SQLALCHEMY_DATABASE_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRESQL_LOCAL_USERNAME,
            password=self.POSTGRESQL_LOCAL_PASSWORD,
            host=self.POSTGRESQL_LOCAL_HOST,
            port=self.POSTGRESQL_LOCAL_PORT,
            path=self.POSTGRESQL_LOCAL_DATABASE,
        )

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_DEFAULT_OWNER_ID: int

    GMAIL_APP_PASSWORD: str
    GMAIL_ACCOUNT: str

    OPENAI_API_KEY: str
    GEMINI_API_KEY: str

    REQUEST_HEADERS: dict[str, str] = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }


settings = Settings()  # type: ignore
