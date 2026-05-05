"""
Graphics & Driver Optimizer for NEON VOID OPTIMIZER.
GPU vendor-specific settings, shader cache management, driver updates.
"""

import logging
import subprocess
from typing import Dict, List, Optional

logger = logging.getLogger("NEON_VOID")


class GraphicsOptimizer:
    """
    Graphics driver optimization for NVIDIA, AMD, and Intel GPUs.
    Low latency modes, performance settings, shader cache management.
    """

    GPU_VENDORS = ["NVIDIA", "AMD", "Intel", "Unknown"]

    NVIDIA_SETTINGS = {
        "Low_Latency_Mode": {
            "values": ["Off", "On", "Ultra"],
            "recommended": "Ultra",
            "description": "Reduces render queue for lower input lag"
        },
        "Power_Management": {
            "values": ["Adaptive", "Maximum Performance", "Optimal"],
            "recommended": "Maximum Performance",
            "description": "Keeps GPU at maximum performance state"
        },
        "Texture_Filtering_Quality": {
            "values": ["High Quality", "Quality", "Performance", "High Performance"],
            "recommended": "Performance",
            "description": "Texture filtering optimization"
        },
        "Threaded_Optimization": {
            "values": ["Off", "On", "Auto"],
            "recommended": "On",
            "description": "Multi-threaded optimization"
        },
        "Vertical_Sync": {
            "values": ["Off", "On", "Adaptive", "Fast"],
            "recommended": "Off",
            "description": "Disable for lowest latency"
        },
    }

    AMD_SETTINGS = {
        "Anti_Lag": {
            "values": ["Disabled", "Enabled"],
            "recommended": "Enabled",
            "description": "Reduces input-to-display latency"
        },
        "Radeon_Boost": {
            "values": ["Disabled", "Enabled"],
            "recommended": "Enabled",
            "description": "Dynamic resolution scaling during motion"
        },
        "Radeon_Chill": {
            "values": ["Disabled", "Enabled"],
            "recommended": "Disabled",
            "description": "FPS limiter - disable for uncapped"
        },
        "Radeon_Super_Resolution": {
            "values": ["Disabled", "Enabled"],
            "recommended": "Enabled",
            "description": "Driver-level upscaling"
        },
        "Texture_Filtering_Quality": {
            "values": ["Performance", "Quality", "High Quality"],
            "recommended": "Performance",
            "description": "Texture filtering optimization"
        },
    }

    INTEL_SETTINGS = {
        "Low_Latency_Support": {
            "values": ["Disabled", "Enabled"],
            "recommended": "Enabled",
            "description": "Reduces render queue"
        },
        "Adaptive_Tessellation": {
            "values": ["Disabled", "Enabled"],
            "recommended": "Disabled",
            "description": "Disable for consistent performance"
        },
    }

    def __init__(self) -> None:
        self.vendor = self._detect_vendor()
        logger.info(f"GPU detected: {self.vendor}")

    def _detect_vendor(self) -> str:
        """Detect GPU vendor."""
        try:
            import wmi
            c = wmi.WMI()
            for gpu in c.Win32_VideoController():
                name = gpu.Name.upper()
                if "NVIDIA" in name:
                    return "NVIDIA"
                elif "AMD" in name or "RADEON" in name or "ATI" in name:
                    return "AMD"
                elif "INTEL" in name:
                    return "Intel"
        except Exception:
            pass

        # Fallback
        try:
            result = subprocess.run(
                "wmic path win32_VideoController get name",
                shell=True, capture_output=True, text=True
            )
            output = result.stdout.upper()
            if "NVIDIA" in output:
                return "NVIDIA"
            elif "AMD" in output or "RADEON" in output:
                return "AMD"
            elif "INTEL" in output:
                return "Intel"
        except Exception:
            pass

        return "Unknown"

    def get_settings(self) -> Dict:
        """Get settings for detected GPU vendor."""
        if self.vendor == "NVIDIA":
            return self.NVIDIA_SETTINGS
        elif self.vendor == "AMD":
            return self.AMD_SETTINGS
        elif self.vendor == "Intel":
            return self.INTEL_SETTINGS
        else:
            return {}

    def apply_recommended_settings(self) -> Dict[str, str]:
        """Apply all recommended settings for the detected GPU."""
        results = {}
        settings = self.get_settings()

        for setting_name, config in settings.items():
            recommended = config.get("recommended", "")
            results[setting_name] = f"Recommended: {recommended}"
            # Actual implementation would use vendor SDK (NVAPI/ADL)

        logger.info(f"Recommended settings prepared for {self.vendor}")
        return results

    def clear_shader_cache(self) -> str:
        """Clear shader cache for all GPU vendors."""
        cache_paths = {
            "NVIDIA": [
                "%LOCALAPPDATA%\\NVIDIA\\DXCache",
                "%LOCALAPPDATA%\\NVIDIA\\GLCache",
            ],
            "AMD": [
                "%LOCALAPPDATA%\\AMD\\DxCache",
                "%LOCALAPPDATA%\\AMD\\GLCache",
            ],
            "Intel": [
                "%LOCALAPPDATA%\\Intel\\ShaderCache",
            ],
            "All": [
                "%LOCALAPPDATA%\\D3DSCache",
                r"%LOCALAPPDATA%\Microsoft\Windows\Explorer\ThumbCacheToDelete",
            ]
        }

        import glob
        import shutil
        cleared = 0

        for vendor, paths in cache_paths.items():
            for path in paths:
                expanded = os.path.expandvars(path)
                if os.path.exists(expanded):
                    try:
                        shutil.rmtree(expanded)
                        cleared += 1
                    except Exception:
                        pass

        logger.info(f"Shader cache cleared ({cleared} directories)")
        return f"Shader cache cleared ({cleared} directories)"

    def get_driver_info(self) -> Dict:
        """Get GPU driver information."""
        try:
            import wmi
            c = wmi.WMI()
            for gpu in c.Win32_VideoController():
                return {
                    "name": gpu.Name,
                    "driver_version": gpu.DriverVersion,
                    "video_memory": gpu.AdapterRAM,
                    "resolution": f"{gpu.CurrentHorizontalResolution}x{gpu.CurrentVerticalResolution}",
                    "refresh_rate": gpu.CurrentRefreshRate,
                    "vendor": self.vendor,
                }
        except Exception:
            pass

        return {"vendor": self.vendor, "name": "Unknown", "driver_version": "Unknown"}

    def check_driver_updates(self) -> str:
        """Check for GPU driver updates."""
        driver_info = self.get_driver_info()
        current_version = driver_info.get("driver_version", "Unknown")

        # In production, this would query vendor APIs
        logger.info(f"Driver check: {self.vendor} {current_version}")
        return f"Current driver: {current_version} - check vendor website for updates"


import os
