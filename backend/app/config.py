from pydantic import BaseSettings, BaseModel


class Settings(BaseSettings):
    environment: str = "dev"
    title: str = "GQRX Controller API"
    description: str = "GQRX Controller API"
    version: str = "0.1.0"
    telnet_host: str = "127.0.0.1"
    telnet_port: int = 7356

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "gqrx"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }