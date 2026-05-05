"""
Real-time system monitoring for NEON VOID OPTIMIZER.
Collects CPU, GPU, RAM, VRAM, network, and temperature data.
"""

import platform
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Callable, Deque, Dict, List, Optional

import psutil

from .logger import logger


@dataclass
class SystemSnapshot:
    """A snapshot of system metrics at a point in time."""
    timestamp: float = 0.0

    # CPU
    cpu_percent: float = 0.0
    cpu_freq_mhz: float = 0.0
    cpu_temp: Optional[float] = None
    cpu_count_physical: int = 0
    cpu_count_logical: int = 0
    cpu_per_core: List[float] = field(default_factory=list)

    # Memory
    ram_used_gb: float = 0.0
    ram_total_gb: float = 0.0
    ram_percent: float = 0.0

    # GPU (if available)
    gpu_name: str = "Unknown"
    gpu_usage: float = 0.0
    gpu_temp: Optional[float] = None
    vram_used_mb: float = 0.0
    vram_total_mb: float = 0.0
    vram_percent: float = 0.0
    gpu_clock_mhz: float = 0.0
    gpu_mem_clock_mhz: float = 0.0
    gpu_power_watts: float = 0.0

    # Network
    net_download_mbps: float = 0.0
    net_upload_mbps: float = 0.0
    ping_ms: float = 0.0
    jitter_ms: float = 0.0
    packet_loss: float = 0.0

    # Disk
    disk_usage_percent: float = 0.0

    @property
    def ram_used_percent(self) -> float:
        return self.ram_percent

    @property
    def vram_used_percent(self) -> float:
        return self.vram_percent


class SystemMonitor:
    """
    Continuous system monitoring with history tracking.
    Runs in a background thread and provides real-time data.
    """

    _instance: Optional['SystemMonitor'] = None

    def __new__(cls) -> 'SystemMonitor':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True

        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._callbacks: List[Callable[[SystemSnapshot], None]] = []
        self._lock = threading.Lock()

        # History (kept for graphing)
        self._history: Deque[SystemSnapshot] = deque(maxlen=300)  # 5 min at 1 sample/sec
        self._current: SystemSnapshot = SystemSnapshot()

        # Network tracking
        self._last_net_io = psutil.net_io_counters()
        self._last_net_time = time.time()

        # GPU info cache
        self._gpu_available = False
        self._gpu_name = "Unknown"
        self._detect_gpu()

        # CPU info
        self._cpu_count_physical = psutil.cpu_count(logical=False) or 1
        self._cpu_count_logical = psutil.cpu_count(logical=True) or 1

    def _detect_gpu(self) -> None:
        """Detect GPU vendor and availability."""
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                self._gpu_available = True
                self._gpu_name = gpus[0].name
                logger.info(f"GPU detected: {self._gpu_name}")
            else:
                logger.info("No GPU detected via GPUtil")
        except ImportError:
            logger.debug("GPUtil not available")
        except Exception as e:
            logger.debug(f"GPU detection error: {e}")

        # Fallback to basic info
        if not self._gpu_available:
            self._gpu_name = self._get_basic_gpu_name()

    def _get_basic_gpu_name(self) -> str:
        """Get GPU name from system info."""
        if platform.system() == "Windows":
            try:
                import wmi
                c = wmi.WMI()
                for gpu in c.Win32_VideoController():
                    if gpu.Name:
                        return gpu.Name
            except Exception:
                pass
        return "Unknown GPU"

    @property
    def current(self) -> SystemSnapshot:
        with self._lock:
            return self._current

    @property
    def history(self) -> List[SystemSnapshot]:
        with self._lock:
            return list(self._history)

    @property
    def gpu_available(self) -> bool:
        return self._gpu_available

    @property
    def gpu_name(self) -> str:
        return self._gpu_name

    def register_callback(self, callback: Callable[[SystemSnapshot], None]) -> None:
        """Register a callback to be called on each update."""
        self._callbacks.append(callback)

    def unregister_callback(self, callback: Callable[[SystemSnapshot], None]) -> None:
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def start(self) -> None:
        """Start the monitoring thread."""
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        logger.info("System monitor started")

    def stop(self) -> None:
        """Stop the monitoring thread."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        logger.info("System monitor stopped")

    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self._running:
            try:
                snapshot = self._collect_snapshot()

                with self._lock:
                    self._current = snapshot
                    self._history.append(snapshot)

                # Notify callbacks
                for callback in self._callbacks:
                    try:
                        callback(snapshot)
                    except Exception as e:
                        logger.debug(f"Monitor callback error: {e}")

                time.sleep(1.0)

            except Exception as e:
                logger.error(f"Monitor loop error: {e}")
                time.sleep(2.0)

    def _collect_snapshot(self) -> SystemSnapshot:
        """Collect a single system snapshot."""
        snapshot = SystemSnapshot(timestamp=time.time())

        # CPU
        snapshot.cpu_percent = psutil.cpu_percent(interval=None)
        snapshot.cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)
        snapshot.cpu_count_physical = self._cpu_count_physical
        snapshot.cpu_count_logical = self._cpu_count_logical

        try:
            freq = psutil.cpu_freq()
            if freq:
                snapshot.cpu_freq_mhz = freq.current
        except Exception:
            pass

        # CPU Temperature
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                # Try common temperature keys
                for key in ['coretemp', 'k10temp', 'zenpower', 'cpu_thermal']:
                    if key in temps:
                        entries = temps[key]
                        if entries:
                            snapshot.cpu_temp = entries[0].current
                            break
        except Exception:
            pass

        # Memory
        mem = psutil.virtual_memory()
        snapshot.ram_used_gb = mem.used / (1024**3)
        snapshot.ram_total_gb = mem.total / (1024**3)
        snapshot.ram_percent = mem.percent

        # GPU
        snapshot.gpu_name = self._gpu_name
        if self._gpu_available:
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    snapshot.gpu_usage = gpu.load * 100
                    snapshot.vram_used_mb = gpu.memoryUsed
                    snapshot.vram_total_mb = gpu.memoryTotal
                    snapshot.vram_percent = (gpu.memoryUsed / gpu.memoryTotal * 100) if gpu.memoryTotal > 0 else 0
                    # Temperature if available
                    if hasattr(gpu, 'temperature'):
                        snapshot.gpu_temp = gpu.temperature
            except Exception:
                pass

        # Network
        try:
            current_net_io = psutil.net_io_counters()
            current_time = time.time()
            time_delta = current_time - self._last_net_time

            if time_delta > 0:
                bytes_per_mb = 1024 * 1024
                download_bytes = current_net_io.bytes_recv - self._last_net_io.bytes_recv
                upload_bytes = current_net_io.bytes_sent - self._last_net_io.bytes_sent

                snapshot.net_download_mbps = (download_bytes / bytes_per_mb) / time_delta
                snapshot.net_upload_mbps = (upload_bytes / bytes_per_mb) / time_delta

            self._last_net_io = current_net_io
            self._last_net_time = current_time
        except Exception:
            pass

        # Disk
        try:
            disk = psutil.disk_usage('/')
            snapshot.disk_usage_percent = disk.percent
        except Exception:
            pass

        return snapshot

    def get_health_score(self) -> int:
        """Calculate overall system health score (0-100)."""
        snapshot = self.current
        score = 100

        # Deduct for high temperatures
        if snapshot.cpu_temp and snapshot.cpu_temp > 80:
            score -= int((snapshot.cpu_temp - 80) * 1.5)
        if snapshot.gpu_temp and snapshot.gpu_temp > 80:
            score -= int((snapshot.gpu_temp - 80) * 1.5)

        # Deduct for high usage
        if snapshot.cpu_percent > 90:
            score -= 10
        elif snapshot.cpu_percent > 70:
            score -= 5

        if snapshot.ram_percent > 90:
            score -= 10
        elif snapshot.ram_percent > 80:
            score -= 5

        if snapshot.vram_percent > 90:
            score -= 10

        return max(0, min(100, score))

    def get_average_ping(self, count: int = 10) -> float:
        """Get average ping from history."""
        recent = list(self._history)[-count:]
        if not recent:
            return 0.0
        pings = [s.ping_ms for s in recent if s.ping_ms > 0]
        return sum(pings) / len(pings) if pings else 0.0

    def update_ping(self, ping_ms: float, jitter_ms: float = 0.0, packet_loss: float = 0.0) -> None:
        """Update network metrics from external ping tests."""
        with self._lock:
            self._current.ping_ms = ping_ms
            self._current.jitter_ms = jitter_ms
            self._current.packet_loss = packet_loss


# Global system monitor instance
system_monitor = SystemMonitor()
