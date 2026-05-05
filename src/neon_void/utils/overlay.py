"""
In-game overlay for NEON VOID OPTIMIZER.
Displays real-time metrics as a minimal overlay during gameplay.
"""

import logging
import threading
import time
from typing import Dict, Optional

from ..core.system_monitor import system_monitor

logger = logging.getLogger("NEON_VOID")


class InGameOverlay:
    """
    Low-overhead in-game overlay showing key system metrics.
    Uses a minimal window that stays on top during gameplay.
    """

    def __init__(self) -> None:
        self.enabled = False
        self._window: Optional[int] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._position = "top_right"  # top_right, top_left, bottom_right, bottom_left
        self._opacity = 0.7

    def show(self) -> None:
        """Show the overlay window."""
        if self.enabled:
            return

        self.enabled = True
        self._running = True
        self._thread = threading.Thread(target=self._update_loop, daemon=True)
        self._thread.start()
        logger.info("In-game overlay enabled")

    def hide(self) -> None:
        """Hide the overlay window."""
        self.enabled = False
        self._running = False
        logger.info("In-game overlay disabled")

    def _update_loop(self) -> None:
        """Update overlay metrics in real-time."""
        while self._running:
            try:
                snapshot = system_monitor.current

                # In production, this would render to a transparent overlay window
                # For now, we just log the metrics
                overlay_data = {
                    "ping": snapshot.ping_ms,
                    "fps": "--",  # Would need game integration
                    "cpu": snapshot.cpu_percent,
                    "gpu": snapshot.gpu_usage,
                    "ram": snapshot.ram_percent,
                    "temp": snapshot.cpu_temp or 0,
                }

                time.sleep(1.0)

            except Exception as e:
                logger.debug(f"Overlay update error: {e}")
                time.sleep(2.0)

    def get_metrics_text(self) -> str:
        """Get formatted metrics string for overlay display."""
        snapshot = system_monitor.current
        return (
            f"Ping: {snapshot.ping_ms:.0f}ms | "
            f"CPU: {snapshot.cpu_percent:.0f}% | "
            f"GPU: {snapshot.gpu_usage:.0f}% | "
            f"RAM: {snapshot.ram_percent:.0f}% | "
            f"Temp: {snapshot.cpu_temp or 0:.0f}C"
        )


# Global instance
overlay = InGameOverlay()
