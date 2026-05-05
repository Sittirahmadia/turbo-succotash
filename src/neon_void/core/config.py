"""
Configuration management for NEON VOID OPTIMIZER.
Handles user preferences, feature flags, and per-game profiles.
"""

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .i18n import Language
from .logger import logger


@dataclass
class AppConfig:
    """Main application configuration."""

    # Language
    language: str = "en"

    # UI Settings
    theme: str = "cyberpunk"
    enable_3d_background: bool = True
    enable_crt_effect: bool = False
    enable_glitch_effect: bool = False
    enable_sound_effects: bool = False
    window_width: int = 1400
    window_height: int = 900

    # Feature Toggles
    enable_overlay: bool = False
    start_with_windows: bool = False
    minimize_to_tray: bool = True
    enable_ai_prediction: bool = True
    ai_void_mode_auto: bool = False

    # Network Defaults
    default_mtu: int = 1500
    preferred_dns_primary: str = "1.1.1.1"
    preferred_dns_secondary: str = "1.0.0.1"

    # Safety
    require_confirmation: bool = True
    auto_backup: bool = True
    temperature_limit_cpu: int = 85
    temperature_limit_gpu: int = 83

    # Update
    check_updates_on_start: bool = True
    last_update_check: Optional[str] = None

    # Konami Code Easter Egg
    konami_activated: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AppConfig':
        # Filter only known fields
        known = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in known}
        return cls(**filtered)


class ConfigManager:
    """Manages loading, saving, and accessing application configuration."""

    CONFIG_DIR = Path("config")
    CONFIG_FILE = CONFIG_DIR / "user_config.json"
    PROFILES_DIR = Path("profiles")

    def __init__(self) -> None:
        self.CONFIG_DIR.mkdir(exist_ok=True)
        self.PROFILES_DIR.mkdir(exist_ok=True)

        self._config = AppConfig()
        self._profiles: Dict[str, Dict[str, Any]] = {}

        self.load()
        self._load_profiles()

    @property
    def config(self) -> AppConfig:
        return self._config

    def load(self) -> None:
        """Load configuration from file."""
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self._config = AppConfig.from_dict(data)
                logger.info("Configuration loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load config: {e}. Using defaults.")
                self._config = AppConfig()
        else:
            logger.info("No existing config found. Using defaults.")
            self.save()

    def save(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._config.to_dict(), f, indent=2, default=str)
            logger.debug("Configuration saved")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        self._config = AppConfig()
        self.save()
        logger.info("Configuration reset to defaults")

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        if hasattr(self._config, key):
            setattr(self._config, key, value)
            self.save()
        else:
            logger.warning(f"Unknown config key: {key}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return getattr(self._config, key, default)

    def _load_profiles(self) -> None:
        """Load all game profiles."""
        if not self.PROFILES_DIR.exists():
            return

        for file in self.PROFILES_DIR.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    self._profiles[file.stem] = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load profile {file}: {e}")

    def get_profile(self, game_name: str) -> Optional[Dict[str, Any]]:
        """Get a game profile by name."""
        return self._profiles.get(game_name.lower().replace(" ", "_"))

    def save_profile(self, game_name: str, profile: Dict[str, Any]) -> None:
        """Save a game profile."""
        key = game_name.lower().replace(" ", "_")
        self._profiles[key] = profile

        profile_file = self.PROFILES_DIR / f"{key}.json"
        try:
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2)
            logger.info(f"Profile saved: {game_name}")
        except Exception as e:
            logger.error(f"Failed to save profile: {e}")

    def delete_profile(self, game_name: str) -> None:
        """Delete a game profile."""
        key = game_name.lower().replace(" ", "_")
        if key in self._profiles:
            del self._profiles[key]

        profile_file = self.PROFILES_DIR / f"{key}.json"
        if profile_file.exists():
            profile_file.unlink()
            logger.info(f"Profile deleted: {game_name}")

    def list_profiles(self) -> List[str]:
        """List all saved profile names."""
        return list(self._profiles.keys())

    def get_language(self) -> Language:
        """Get current language enum."""
        lang_map = {
            "en": Language.ENGLISH,
            "id": Language.INDONESIA
        }
        return lang_map.get(self._config.language, Language.ENGLISH)


# Global config instance
config = ConfigManager()
