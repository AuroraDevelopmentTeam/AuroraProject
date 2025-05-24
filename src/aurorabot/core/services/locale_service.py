import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging


class LocaleService:
    """Service for handling localization."""
    
    _instance = None
    _locales = {}
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, logger: logging.Logger) -> None:
        """Initialize the locale service.
        
        Args:
            logger: The logger instance
        """
        if not self._initialized:
            self.logger = logger
            self._load_locales()
            self._initialized = True

    def _load_locales(self) -> None:
        """Load all locale files from the locales directory."""
        try:
            # Try multiple possible paths
            possible_paths = [
                Path(__file__).parent.parent.parent.parent / "src" / "aurorabot" / "locales",
                Path(__file__).parent.parent.parent / "locales",
                Path.cwd() / "src" / "aurorabot" / "locales",
                Path.cwd() / "locales"
            ]
            
            locales_path = None
            for path in possible_paths:
                if path.exists():
                    locales_path = path
                    break
                    
            if not locales_path:
                self.logger.error("Could not find locales directory in any of the expected locations")
                return
                
            self.logger.info(f"Found locales directory at: {locales_path}")
            
            for locale_file in locales_path.glob("*.yaml"):
                try:
                    with open(locale_file, 'r', encoding='utf-8') as f:
                        self._locales[locale_file.stem] = yaml.safe_load(f)
                    self.logger.info(f"Loaded locale file: {locale_file.name}")
                except Exception as e:
                    self.logger.error(f"Error loading locale file {locale_file.name}: {e}")
                    
            if not self._locales:
                self.logger.error("No locale files were loaded successfully")
            else:
                self.logger.info(f"Successfully loaded {len(self._locales)} locale files")
                
        except Exception as e:
            self.logger.error(f"Error in _load_locales: {e}", exc_info=True)

    @classmethod
    def get_command_localizations(cls, command_key: str) -> Dict[str, Dict[str, str]]:
        """Get command localizations for all available languages.
        
        Args:
            command_key: The command key (e.g., 'ping', 'user', 'server')
            
        Returns:
            Dict[str, Dict[str, str]]: Dictionary with localizations for each language
        """
        if not cls._instance or not cls._instance._locales:
            return {
                'name_localizations': {},
                'description_localizations': {}
            }
            
        # Map our locale codes to Discord's locale codes
        locale_mapping = {
            'en': 'en-US',
            'ru': 'ru'
        }
            
        localizations = {
            'name_localizations': {},
            'description_localizations': {}
        }
        
        for locale, data in cls._instance._locales.items():
            try:
                command_data = data.get('commands', {}).get(command_key, {})
                discord_locale = locale_mapping.get(locale)
                if not discord_locale:
                    continue
                    
                if 'name' in command_data:
                    localizations['name_localizations'][discord_locale] = command_data['name']
                if 'description' in command_data:
                    localizations['description_localizations'][discord_locale] = command_data['description']
            except Exception as e:
                cls._instance.logger.error(f"Error getting localizations for command {command_key} in {locale}: {e}")
                
        return localizations

    def get_text(self, key: str, **kwargs) -> str:
        """Get localized text for a key.
        
        Args:
            key: The localization key
            **kwargs: Format arguments
            
        Returns:
            str: The localized text
        """
        try:
            # Split the key into parts
            parts = key.split('.')
            
            # Get the locale (default to 'en')
            locale = 'en'
            if not self._locales:
                self.logger.warning(f"No locales loaded, using key as fallback: {key}")
                return key
                
            # Navigate through the nested dictionary
            value = self._locales[locale]
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part)
                    if value is None:
                        self.logger.warning(f"Missing translation for key: {key}")
                        # Return a more user-friendly fallback
                        return key.split('.')[-1].replace('_', ' ').title()
                else:
                    self.logger.warning(f"Invalid translation structure for key: {key}")
                    return key.split('.')[-1].replace('_', ' ').title()
                    
            # If we got a string, format it with the kwargs
            if isinstance(value, str):
                try:
                    return value.format(**kwargs)
                except KeyError as e:
                    self.logger.warning(f"Missing format argument {e} for key: {key}")
                    return value
                    
            # If we got a dictionary or list, convert to string
            return str(value)
            
        except Exception as e:
            self.logger.error(f"Error getting localized text for key '{key}': {e}")
            return key.split('.')[-1].replace('_', ' ').title()

    def get_available_locales(self) -> list[str]:
        """Get list of available locales.
        
        Returns:
            list[str]: List of available locale codes
        """
        return list(self._locales.keys()) 