"""
Update checker for NEON VOID OPTIMIZER.
Checks GitHub releases for new versions.
"""

import json
import logging
import time
from typing import Optional

import requests

from ..core.config import config

logger = logging.getLogger("NEON_VOID")

CURRENT_VERSION = "1.0.0"
GITHUB_REPO = "yourusername/neon-void-optimizer"  # Update this
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


class UpdateChecker:
    """Checks for application updates from GitHub releases."""

    def __init__(self) -> None:
        self._last_check: Optional[float] = None
        self._cached_result: Optional[dict] = None

    def check_for_updates(self, force: bool = False) -> dict:
        """Check if a newer version is available."""
        # Use cached result if checked recently
        if not force and self._cached_result and self._last_check:
            if time.time() - self._last_check < 3600:  # 1 hour cache
                return self._cached_result

        try:
            response = requests.get(
                GITHUB_API_URL,
                timeout=10,
                headers={"Accept": "application/vnd.github.v3+json"}
            )
            response.raise_for_status()

            release = response.json()
            latest_version = release.get("tag_name", "v0.0.0").lstrip("v")

            # Simple version comparison
            current_parts = CURRENT_VERSION.split(".")
            latest_parts = latest_version.split(".")

            update_available = False
            for i in range(max(len(current_parts), len(latest_parts))):
                c = int(current_parts[i]) if i < len(current_parts) else 0
                l = int(latest_parts[i]) if i < len(latest_parts) else 0
                if l > c:
                    update_available = True
                    break
                elif l < c:
                    break

            result = {
                "current_version": CURRENT_VERSION,
                "latest_version": latest_version,
                "update_available": update_available,
                "download_url": release.get("html_url", ""),
                "release_notes": release.get("body", ""),
                "checked_at": time.time(),
            }

            self._cached_result = result
            self._last_check = time.time()

            if update_available:
                logger.info(f"Update available: {latest_version}")

            return result

        except requests.exceptions.RequestException as e:
            logger.debug(f"Update check failed (network): {e}")
            return {"error": f"Network error: {e}"}
        except Exception as e:
            logger.error(f"Update check failed: {e}")
            return {"error": str(e)}

    def get_status_line(self) -> str:
        """Get a one-line update status."""
        result = self._cached_result
        if not result:
            return "Update status unknown"

        if "error" in result:
            return f"Update check failed: {result['error']}"

        if result.get("update_available"):
            return f"Update available: v{result['latest_version']}"

        return f"Up to date (v{CURRENT_VERSION})"


# Global instance
updater = UpdateChecker()
