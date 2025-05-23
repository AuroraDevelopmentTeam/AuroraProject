from pathlib import Path
import yaml
import logging.config
import os
import sys
import logging.handlers


class Config:
    def __init__(self):
        self.config_path = Path(__file__).parent.parent.parent.parent / "config" / "settings.yaml"
        self.logging_config_path = Path(__file__).parent.parent.parent.parent / "config" / "logging.ini"
        self.logs_dir = Path(__file__).parent.parent.parent.parent / "logs"
        self.config = self._load_config()
        self._setup_logging()

    def _load_config(self) -> dict:
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _setup_logging(self) -> None:
        # Создание директории для логов, если она не существует
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Создание конфигурации логирования
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'simpleFormatter': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d] - %(funcName)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                }
            },
            'handlers': {
                'consoleHandler': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'simpleFormatter',
                    'stream': 'ext://sys.stdout'
                },
                'fileHandler': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'simpleFormatter',
                    'filename': str(self.logs_dir / "aurorabot.log"),
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 5,
                    'encoding': 'utf-8'
                }
            },
            'loggers': {
                'aurorabot': {
                    'level': 'INFO',
                    'handlers': ['consoleHandler', 'fileHandler'],
                    'propagate': False
                }
            }
        }
        
        # Применение конфигурации логирования
        logging.config.dictConfig(logging_config)
        self.logger = logging.getLogger("aurorabot")

    @property
    def bot_config(self) -> dict:
        return self.config["bot"]
