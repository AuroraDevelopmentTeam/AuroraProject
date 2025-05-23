import i18n
from pathlib import Path
import yaml
from typing import Dict, Any

class I18nManager:
    def __init__(self):
        # Load configuration
        config_path = Path(__file__).parent.parent.parent.parent / "config" / "settings.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        # Set up i18n
        self.locales_dir = Path(__file__).parent.parent / "locales"
        i18n.load_path.append(str(self.locales_dir))
        i18n.set("fallback", self.config["bot"]["default_locale"])
        i18n.set("skip_locale_root_data", True)
        i18n.set("enable_memoization", True)

    def t(self, key: str, locale: str = None, **kwargs) -> str:
        """Translate a key to the specified locale."""
        if locale is None:
            locale = self.config["bot"]["default_locale"]
        return i18n.t(key, locale=locale, **kwargs)

    def get_available_locales(self) -> Dict[str, Any]:
        """Get all available locales and their names."""
        locales = {}
        for locale_file in self.locales_dir.glob("*.yaml"):
            locale = locale_file.stem
            with open(locale_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                locales[locale] = data.get("locale_name", locale)
        return locales

# Create a global instance
i18n_manager = I18nManager() 