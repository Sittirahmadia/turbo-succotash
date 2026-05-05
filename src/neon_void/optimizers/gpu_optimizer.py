"""
GPU Overclocking for NEON VOID OPTIMIZER.
Real-time monitoring, core/memory offsets, fan curves, stability monitoring.
"""

import logging
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

logger = logging.getLogger("NEON_VOID")


@dataclass
class GPUMetrics:
    """GPU performance metrics."""
    core_clock_mhz: float = 0.0
    memory_clock_mhz: float = 0.0
    temperature_c: Optional[float] = None
    usage_percent: float = 0.0
    power_draw_w: float = 0.0
    fan_speed_percent: float = 0.0
    vram_used_mb: float = 0.0
    vram_total_mb: float = 0.0


class GPUOverclocker:
    """
    GPU overclocking management.
    Provides monitoring, profile management, and safe overclocking guidance.
    """

    SAFETY_PRESETS = {
        "Gaming": {
            "description": "Moderate boost for stable gaming",
            "core_offset_mhz": 100,
            "memory_offset_mhz": 200,
            "power_limit_percent": 100,
            "temp_limit_c": 83,
            "voltage_offset_mv": 0,
        },
        "High_Performance": {
            "description": "Aggressive overclock with increased power",
            "core_offset_mhz": 150,
            "memory_offset_mhz": 400,
            "power_limit_percent": 110,
            "temp_limit_c": 85,
            "voltage_offset_mv": 20,
        },
        "Extreme": {
            "description": "Maximum overclock - experienced users only",
            "core_offset_mhz": 200,
            "memory_offset_mhz": 600,
            "power_limit_percent": 120,
            "temp_limit_c": 88,
            "voltage_offset_mv": 50,
        },
    }

    def __init__(self) -> None:
        self.current_profile: Optional[str] = None
        self._fan_curve: List[tuple] = []
        self._stability_score = 100.0

    def get_metrics(self) -> GPUMetrics:
        """Get current GPU metrics."""
        metrics = GPUMetrics()

        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                metrics.usage_percent = gpu.load * 100
                metrics.temperature_c = gpu.temperature
                metrics.vram_used_mb = gpu.memoryUsed
                metrics.vram_total_mb = gpu.memoryTotal

                # Estimate clocks (GPUtil doesn't provide these directly)
                # In production, use NVAPI/ADL
                metrics.core_clock_mhz = 1500  # Placeholder
                metrics.memory_clock_mhz = 6000  # Placeholder
                metrics.power_draw_w = gpu.load * 250  # Rough estimate
                metrics.fan_speed_percent = min(100, max(0, (gpu.temperature - 40) * 2))

        except ImportError:
            logger.debug("GPUtil not available")
        except Exception as e:
            logger.debug(f"GPU metrics error: {e}")

        return metrics

    def apply_preset(self, preset_name: str) -> Dict[str, str]:
        """Apply a GPU overclock preset."""
        preset = self.SAFETY_PRESETS.get(preset_name)
        if not preset:
            return {"error": f"Unknown preset: {preset_name}"}

        results = {
            "preset": preset_name,
            "description": preset["description"],
            "core_offset": f"+{preset['core_offset_mhz']} MHz",
            "memory_offset": f"+{preset['memory_offset_mhz']} MHz",
            "power_limit": f"{preset['power_limit_percent']}%",
            "temp_limit": f"{preset['temp_limit_c']}\u00b0C",
            "note": "Use MSI Afterburner or vendor tool to apply",
        }

        self.current_profile = preset_name
        logger.info(f"GPU preset applied: {preset_name}")
        return results

    def set_manual_oc(self, core_offset: Optional[int] = None,
                      memory_offset: Optional[int] = None,
                      voltage_offset: Optional[int] = None,
                      power_limit: Optional[int] = None) -> Dict[str, str]:
        """Set manual GPU overclock parameters."""
        results = {}

        if core_offset is not None:
            results["core_offset"] = f"+{core_offset} MHz"
        if memory_offset is not None:
            results["memory_offset"] = f"+{memory_offset} MHz"
        if voltage_offset is not None:
            results["voltage_offset"] = f"+{voltage_offset} mV"
        if power_limit is not None:
            results["power_limit"] = f"{power_limit}%"

        results["note"] = "Use MSI Afterburner to apply these settings"
        logger.info(f"Manual GPU OC configured: {results}")
        return results

    def set_fan_curve(self, points: List[tuple]) -> str:
        """Set custom fan curve as list of (temp, fan_speed%) tuples."""
        if len(points) < 2:
            return "Need at least 2 points for fan curve"

        self._fan_curve = sorted(points, key=lambda x: x[0])
        logger.info(f"Fan curve set with {len(points)} points")
        return f"Fan curve set with {len(points)} points"

    def get_default_fan_curve(self) -> List[tuple]:
        """Get a reasonable default fan curve."""
        return [
            (30, 30),   # 30% at 30C
            (40, 40),   # 40% at 40C
            (50, 50),   # 50% at 50C
            (60, 60),   # 60% at 60C
            (70, 75),   # 75% at 70C
            (80, 90),   # 90% at 80C
            (85, 100),  # 100% at 85C
        ]

    def get_stability_status(self) -> Dict:
        """Check GPU stability based on recent metrics."""
        metrics = self.get_metrics()
        status = {
            "score": 100,
            "stable": True,
            "warnings": [],
        }

        if metrics.temperature_c and metrics.temperature_c > 85:
            status["score"] -= 20
            status["warnings"].append(f"High temperature: {metrics.temperature_c}\u00b0C")
            status["stable"] = False

        if metrics.temperature_c and metrics.temperature_c > 90:
            status["score"] -= 40
            status["warnings"].append("CRITICAL: Thermal throttling likely!")

        if metrics.power_draw_w > 300:
            status["warnings"].append("High power draw - check PSU capacity")

        status["score"] = max(0, status["score"])
        return status

    def get_gpu_info(self) -> Dict:
        """Get GPU information."""
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                return {
                    "name": gpu.name,
                    "driver": gpu.driver,
                    "vram_total_mb": gpu.memoryTotal,
                    "uuid": gpu.uuid,
                }
        except Exception:
            pass

        return {"name": "Unknown", "driver": "Unknown"}
