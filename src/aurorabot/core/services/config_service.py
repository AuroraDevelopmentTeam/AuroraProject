import yaml
import os
from typing import Any, Dict, Optional
from aurorabot.core.services.logger_service import LoggerService


class ConfigService:
    """Service for handling configuration."""
    
    def __init__(self):
        self.logger = LoggerService().get_logger()
        self.config: Dict[str, Any] = {}
        
    def load_config(self) -> 'ConfigService':
        """Load configuration from file."""
        # Get the project root directory (2 levels up from this file)
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        config_path = os.path.join(root_dir, "config", "settings.yaml")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            self.logger.info("Configuration loaded successfully")
            self.logger.debug(f"Loaded config: {self.config}")  # Debug log to see the structure
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found at {config_path}")
            raise
        except yaml.YAMLError:
            self.logger.error(f"Invalid YAML in configuration file at {config_path}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            raise
            
        return self
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        # Handle nested keys (e.g., "bot.token")
        if "." in key:
            parts = key.split(".")
            value = self.config
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    return default
            return value if value is not None else default
        return self.config.get(key, default)
        
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        # Handle nested keys (e.g., "bot.token")
        if "." in key:
            parts = key.split(".")
            current = self.config
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value
        else:
            self.config[key] = value
        
    def save(self) -> None:
        """Save configuration to file."""
        # Get the project root directory (2 levels up from this file)
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        config_path = os.path.join(root_dir, "config", "settings.yaml")
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            self.logger.info("Configuration saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            raise 