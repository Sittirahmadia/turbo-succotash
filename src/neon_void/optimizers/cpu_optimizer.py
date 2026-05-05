"""
CPU Overclocking for NEON VOID OPTIMIZER.
Real-time monitoring, safe presets, manual controls, temperature protection.
"""

import logging
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

import psutil

logger = logging.getLogger("NEON_VOID")


@dataclass
class CPUMetrics:
    """CPU performance metrics."""
    clock_speed_mhz: float = 0.0
    voltage_v: float = 0.0
    temperature_c: Optional[float] = None
    usage_percent: float = 0.0
    per_core_usage: List[float] = None
    power_watts: float = 0.0

    def __post_init__(self):
        if self.per_core_usage is None:
            self.per_core_usage = []


class CPUOverclocker:
    """
    CPU overclocking management with safety features.
    Note: Actual overclocking requires motherboard/BIOS-level control.
    This module provides monitoring, safety, and profile management.
    """

    SAFETY_PRESETS = {
        "Gaming": {
            "description": "Moderate all-core boost for gaming",
            "target_clock_offset": 100,  # MHz
            "voltage_offset_mv": 0,
            "power_limit_w": 125,
            "temp_limit_c": 80,
        },
        "High_Performance": {
            "description": "Aggressive all-core overclock",
            "target_clock_offset": 200,
            "voltage_offset_mv": 25,
            "power_limit_w": 150,
            "temp_limit_c": 85,
        },
        "Extreme": {
            "description": "Maximum performance with increased voltage",
            "target_clock_offset": 300,
            "voltage_offset_mv": 50,
            "power_limit_w": 200,
            "temp_limit_c": 90,
        },
    }

    def __init__(self) -> None:
        self.current_profile: Optional[str] = None
        self.safety_enabled = True
        self._stress_test_running = False

    def get_metrics(self) -> CPUMetrics:
        """Get current CPU metrics."""
        metrics = CPUMetrics()

        try:
            # Clock speed
            freq = psutil.cpu_freq()
            if freq:
                metrics.clock_speed_mhz = freq.current

            # Usage
            metrics.usage_percent = psutil.cpu_percent(interval=0.1)
            metrics.per_core_usage = psutil.cpu_percent(interval=0.1, percpu=True)

            # Temperature
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    for key in ['coretemp', 'k10temp', 'zenpower', 'cpu_thermal']:
                        if key in temps:
                            entries = temps[key]
                            if entries:
                                metrics.temperature_c = entries[0].current
                                break
            except Exception:
                pass

            # Power (estimated)
            try:
                if metrics.temperature_c and metrics.clock_speed_mhz:
                    # Rough power estimation based on clock and load
                    base_power = 65  # Typical TDP
                    load_factor = metrics.usage_percent / 100
                    clock_factor = metrics.clock_speed_mhz / 3500  # Normalize to base
                    metrics.power_watts = base_power * load_factor * clock_factor
            except Exception:
                pass

        except Exception as e:
            logger.debug(f"CPU metrics error: {e}")

        return metrics

    def apply_preset(self, preset_name: str) -> Dict[str, str]:
        """Apply a safety preset."""
        preset = self.SAFETY_PRESETS.get(preset_name)
        if not preset:
            return {"error": f"Unknown preset: {preset_name}"}

        results = {
            "preset": preset_name,
            "description": preset["description"],
            "clock_offset_mhz": f"+{preset['target_clock_offset']} MHz",
            "voltage_offset_mv": f"+{preset['voltage_offset_mv']} mV",
            "power_limit_w": f"{preset['power_limit_w']}W",
            "temp_limit_c": f"{preset['temp_limit_c']}\u00b0C",
            "note": "Apply in BIOS/UEFI or use Intel XTU/AMD Ryzen Master",
        }

        self.current_profile = preset_name
        logger.info(f"CPU preset applied: {preset_name}")
        return results

    def set_manual_oc(self, multiplier: Optional[float] = None,
                      voltage_offset_mv: Optional[float] = None,
                      power_limit: Optional[int] = None,
                      temp_limit: Optional[int] = None) -> Dict[str, str]:
        """Set manual overclock parameters."""
        results = {}

        if multiplier is not None:
            results["multiplier"] = f"{multiplier}x"
        if voltage_offset_mv is not None:
            results["voltage_offset"] = f"+{voltage_offset_mv}mV"
        if power_limit is not None:
            results["power_limit"] = f"{power_limit}W"
        if temp_limit is not None:
            results["temp_limit"] = f"{temp_limit}\u00b0C"

        results["note"] = "Use Intel XTU or AMD Ryzen Master to apply"
        logger.info(f"Manual OC configured: {results}")
        return results

    def check_safety(self) -> Dict[str, any]:
        """Check if current temperatures are within safe limits."""
        metrics = self.get_metrics()
        status = {
            "safe": True,
            "temperature": metrics.temperature_c,
            "warnings": [],
            "throttling": False,
        }

        if metrics.temperature_c is None:
            status["warnings"].append("Cannot read temperature")
            return status

        if metrics.temperature_c > 90:
            status["safe"] = False
            status["warnings"].append(f"CRITICAL: {metrics.temperature_c}\u00b0C - Stop overclock immediately!")
        elif metrics.temperature_c > 85:
            status["warnings"].append(f"WARNING: {metrics.temperature_c}\u00b0C - Reduce overclock")
        elif metrics.temperature_c > 80:
            status["warnings"].append(f"CAUTION: {metrics.temperature_c}\u00b0C - Monitor closely")

        # Check if CPU is throttling
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for key, entries in temps.items():
                    for entry in entries:
                        if hasattr(entry, 'critical') and entry.critical:
                            if entry.current >= entry.critical:
                                status["throttling"] = True
                                status["warnings"].append("CPU thermal throttling detected!")
        except Exception:
            pass

        return status

    def get_cpu_info(self) -> Dict:
        """Get CPU information."""
        try:
            import cpuinfo
            info = cpuinfo.get_cpu_info()
            return {
                "brand": info.get("brand_raw", "Unknown"),
                "cores_physical": psutil.cpu_count(logical=False),
                "cores_logical": psutil.cpu_count(logical=True),
                "base_freq": info.get("hz_advertised_friendly", "Unknown"),
                "architecture": info.get("arch", "Unknown"),
            }
        except ImportError:
            return {
                "brand": "Unknown (install py-cpuinfo)",
                "cores_physical": psutil.cpu_count(logical=False),
                "cores_logical": psutil.cpu_count(logical=True),
            }
