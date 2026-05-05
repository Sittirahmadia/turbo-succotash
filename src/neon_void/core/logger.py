"""
Advanced logging system for NEON VOID OPTIMIZER.
Features: colored console output, file logging, log rotation, and in-app log window.
"""

import logging
import logging.handlers
import os
import sys
import time
import traceback
from datetime import datetime
from enum import Enum
from pathlib import Path
from threading import Lock
from typing import Callable, List, Optional

from .i18n import tr


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class CyberpunkFormatter(logging.Formatter):
    """Custom formatter with cyberpunk-style colored output."""

    # ANSI color codes matching the cyberpunk theme
    COLORS = {
        "DEBUG": "\033[38;5;39m",      # Electric Cyan
        "INFO": "\033[38;5;82m",       # Acid Green
        "WARNING": "\033[38;5;220m",   # Amber
        "ERROR": "\033[38;5;196m",     # Neon Red
        "CRITICAL": "\033[38;5;201m",  # Hot Magenta
        "RESET": "\033[0m",
        "TIMESTAMP": "\033[38;5;244m", # Gray
        "MODULE": "\033[38;5;147m",    # Light Purple
    }

    def __init__(self, use_colors: bool = True) -> None:
        super().__init__()
        self.use_colors = use_colors
        self.fmt_string = (
            "{timestamp}[{time}] {reset}"
            "{module_color}[{module:<20}]{reset} "
            "{level_color}[{level:<8}]{reset} "
            "{message}"
        )

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S.%f")[:-3]
        module = f"{record.module}:{record.lineno}"
        if len(module) > 20:
            module = module[-20:]

        if self.use_colors and sys.stdout.isatty():
            formatted = self.fmt_string.format(
                timestamp=self.COLORS["TIMESTAMP"],
                time=timestamp,
                reset=self.COLORS["RESET"],
                module_color=self.COLORS["MODULE"],
                module=module,
                level_color=self.COLORS.get(record.levelname, ""),
                level=record.levelname,
                message=record.getMessage()
            )
        else:
            formatted = f"[{timestamp}] [{module:<20}] [{record.levelname:<8}] {record.getMessage()}"

        if record.exc_info:
            formatted += "\n" + traceback.format_exc()

        return formatted


class LogBuffer:
    """Circular buffer for in-app log display."""

    def __init__(self, max_size: int = 1000) -> None:
        self._buffer: List[str] = []
        self._max_size = max_size
        self._callbacks: List[Callable[[str], None]] = []
        self._lock = Lock()

    def append(self, message: str) -> None:
        with self._lock:
            self._buffer.append(message)
            if len(self._buffer) > self._max_size:
                self._buffer.pop(0)

        # Notify callbacks
        for callback in self._callbacks:
            try:
                callback(message)
            except Exception:
                pass

    def get_logs(self, count: Optional[int] = None) -> List[str]:
        with self._lock:
            if count is None:
                return self._buffer.copy()
            return self._buffer[-count:]

    def clear(self) -> None:
        with self._lock:
            self._buffer.clear()

    def register_callback(self, callback: Callable[[str], None]) -> None:
        self._callbacks.append(callback)

    def unregister_callback(self, callback: Callable[[str], None]) -> None:
        if callback in self._callbacks:
            self._callbacks.remove(callback)


class AppLogger:
    """Centralized logging manager for the application."""

    _instance: Optional['AppLogger'] = None

    def __new__(cls) -> 'AppLogger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True

        # Create logs directory
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)

        self.log_buffer = LogBuffer(max_size=2000)
        self._handlers: List[logging.Handler] = []

        # Main logger
        self._logger = logging.getLogger("NEON_VOID")
        self._logger.setLevel(logging.DEBUG)
        self._logger.propagate = False

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(CyberpunkFormatter(use_colors=True))
        self._logger.addHandler(console_handler)
        self._handlers.append(console_handler)

        # File handler with rotation
        log_file = self.log_dir / f"neon_void_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(CyberpunkFormatter(use_colors=False))
        self._logger.addHandler(file_handler)
        self._handlers.append(file_handler)

        # Custom handler to fill the in-app buffer
        class BufferHandler(logging.Handler):
            def __init__(self, buffer: LogBuffer):
                super().__init__()
                self.buffer = buffer

            def emit(self, record: logging.LogRecord) -> None:
                msg = self.format(record)
                self.buffer.append(msg)

        buffer_handler = BufferHandler(self.log_buffer)
        buffer_handler.setLevel(logging.DEBUG)
        buffer_handler.setFormatter(CyberpunkFormatter(use_colors=False))
        self._logger.addHandler(buffer_handler)
        self._handlers.append(buffer_handler)

        # Session log
        self.session_log: List[dict] = []

    def debug(self, message: str) -> None:
        self._logger.debug(message)
        self._add_to_session("DEBUG", message)

    def info(self, message: str) -> None:
        self._logger.info(message)
        self._add_to_session("INFO", message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)
        self._add_to_session("WARNING", message)

    def error(self, message: str) -> None:
        self._logger.error(message)
        self._add_to_session("ERROR", message)

    def critical(self, message: str) -> None:
        self._logger.critical(message)
        self._add_to_session("CRITICAL", message)

    def exception(self, message: str) -> None:
        self._logger.exception(message)
        self._add_to_session("ERROR", message + "\n" + traceback.format_exc())

    def _add_to_session(self, level: str, message: str) -> None:
        self.session_log.append({
            "timestamp": time.time(),
            "level": level,
            "message": message
        })

    def get_logs(self, count: Optional[int] = None) -> List[str]:
        return self.log_buffer.get_logs(count)

    def clear_logs(self) -> None:
        self.log_buffer.clear()
        self.info("Log buffer cleared")

    def export_logs(self, filepath: str) -> bool:
        """Export all logs to a file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("NEON VOID OPTIMIZER - LOG EXPORT\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                for entry in self.session_log:
                    ts = datetime.fromtimestamp(entry["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{ts}] [{entry['level']:<8}] {entry['message']}\n")
            return True
        except Exception as e:
            self.error(f"Failed to export logs: {e}")
            return False

    def shutdown(self) -> None:
        self.info(tr("log_app_exit"))
        for handler in self._handlers:
            handler.close()
            self._logger.removeHandler(handler)


# Global logger instance
logger = AppLogger()
