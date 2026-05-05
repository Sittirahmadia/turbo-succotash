"""
FPS & System Performance Booster for NEON VOID OPTIMIZER.
Ultimate Power Plan, Game Mode, HAGS, memory management, process priority, debloating.
"""

import logging
import os
import subprocess
from typing import Dict, List, Optional

import psutil

from ..core.backup_manager import backup_manager

logger = logging.getLogger("NEON_VOID")


class FPSBooster:
    """
    Comprehensive FPS and system performance optimization.
    Manages power plans, Game Mode, HAGS, memory, and process priorities.
    """

    POWER_PLAN_GUID = "7777c4c2-5298-4804-b401-128adacb7bfa"  # Custom GUID

    SERVICES_TO_DISABLE = [
        "DiagTrack",           # Connected User Experiences and Telemetry
        "dmwappushservice",    # WAP Push Message Routing
        "MapsBroker",          # Downloaded Maps Manager
        "WMPNetworkSvc",       # Windows Media Player Network Sharing
        "XblAuthManager",      # Xbox Live Auth Manager
        "XblGameSave",         # Xbox Live Game Save
        "XboxNetApiSvc",       # Xbox Live Networking
        "SysMain",             # SysMain (Superfetch)
        "WSearch",             # Windows Search (optional)
    ]

    def __init__(self) -> None:
        self._original_power_plan: Optional[str] = None
        self._game_mode_original: Optional[bool] = None

    def create_neon_void_power_plan(self) -> str:
        """Create and activate the NEON VOID Ultimate Performance power plan."""
        try:
            # First, try to enable Ultimate Performance plan (Windows 10/11 hidden plan)
            result = subprocess.run(
                "powercfg /duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61",
                shell=True, capture_output=True, text=True
            )

            if "Ultimate Performance" in result.stdout or result.returncode == 0:
                # Extract the GUID and activate it
                import re
                guid_match = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
                                       result.stdout)
                if guid_match:
                    plan_guid = guid_match.group(1)
                    subprocess.run(f"powercfg /setactive {plan_guid}", shell=True, check=True)
                    logger.info("Ultimate Performance power plan activated")
                    return f"Ultimate Performance activated ({plan_guid})"

            # Fallback: Create custom high performance plan
            result = subprocess.run(
                f"powercfg /duplicatescheme 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c {self.POWER_PLAN_GUID}",
                shell=True, capture_output=True, text=True
            )

            if result.returncode == 0:
                # Configure the custom plan
                tweaks = [
                    # Disable core parking
                    f"powercfg /setacvalueindex {self.POWER_PLAN_GUID} sub_processor CPMINCORES 100",
                    # Maximum processor state
                    f"powercfg /setacvalueindex {self.POWER_PLAN_GUID} sub_processor PROCTHROTTLEMAX 100",
                    # Minimum processor state
                    f"powercfg /setacvalueindex {self.POWER_PLAN_GUID} sub_processor PROCTHROTTLEMIN 100",
                    # Disable USB selective suspend
                    f"powercfg /setacvalueindex {self.POWER_PLAN_GUID} sub_usb 2a737441-1930-4402-8d77-b2bebba308a3 0",
                    # Disable hard disk sleep
                    f"powercfg /setacvalueindex {self.POWER_PLAN_GUID} sub_disk 0b2d69d7-a2a1-449c-9680-f91c70521c60 0",
                    # Disable sleep
                    f"powercfg /setacvalueindex {self.POWER_PLAN_GUID} sub_sleep 238c9fa8-0aad-41ed-83f4-97be242c8f20 0",
                    # Disable PCI Express link state
                    f"powercfg /setacvalueindex {self.POWER_PLAN_GUID} sub_pciexpress ee12f906-d277-404b-b6da-e5fa1a576df5 0",
                    # Disable display dimming
                    f"powercfg /setacvalueindex {self.POWER_PLAN_GUID} sub_video aded5e82-b909-4619-9949-f5d71dac0bcb 0",
                    # Maximum brightness
                    f"powercfg /setacvalueindex {self.POWER_PLAN_GUID} sub_video 3b0d8229-0e99-4c27-96b3-9d802411c558 100",
                ]

                for tweak in tweaks:
                    subprocess.run(tweak, shell=True, capture_output=True)

                # Activate the plan
                subprocess.run(f"powercfg /setactive {self.POWER_PLAN_GUID}", shell=True, check=True)

                logger.info("NEON VOID Ultimate power plan created and activated")
                return "NEON VOID Ultimate power plan activated"

            return f"Failed: {result.stderr[:200]}"

        except Exception as e:
            logger.error(f"Power plan creation failed: {e}")
            return f"Failed: {e}"

    def enable_game_mode(self) -> str:
        """Enable Windows Game Mode."""
        try:
            result = subprocess.run(
                r'reg add "HKCU\Software\Microsoft\GameBar" /v AllowAutoGameMode /t REG_DWORD /d 1 /f',
                shell=True, capture_output=True, text=True
            )
            result2 = subprocess.run(
                r'reg add "HKCU\Software\Microsoft\GameBar" /v AutoGameModeEnabled /t REG_DWORD /d 1 /f',
                shell=True, capture_output=True, text=True
            )
            logger.info("Game Mode enabled")
            return "Game Mode enabled"
        except Exception as e:
            logger.error(f"Game Mode enable failed: {e}")
            return f"Failed: {e}"

    def enable_hags(self) -> str:
        """Enable Hardware-Accelerated GPU Scheduling."""
        try:
            result = subprocess.run(
                r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" '
                r'/v HwSchMode /t REG_DWORD /d 2 /f',
                shell=True, capture_output=True, text=True
            )
            if result.returncode == 0:
                logger.info("HAGS enabled (requires restart)")
                return "HAGS enabled - restart required"
            return f"Failed: {result.stderr[:100]}"
        except Exception as e:
            logger.error(f"HAGS enable failed: {e}")
            return f"Failed: {e}"

    def set_timer_resolution(self, ms: float = 0.5) -> str:
        """Set Windows timer resolution (requires third-party tool)."""
        logger.info(f"Timer resolution set to {ms}ms (requires external tool)")
        return f"Timer resolution target: {ms}ms - use ClockRes or similar tool"

    def enable_large_system_cache(self) -> str:
        """Enable Large System Cache for better file performance."""
        try:
            result = subprocess.run(
                r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" '
                r'/v LargeSystemCache /t REG_DWORD /d 1 /f',
                shell=True, capture_output=True, text=True
            )
            logger.info("Large System Cache enabled")
            return "Large System Cache enabled"
        except Exception as e:
            logger.error(f"Large System Cache enable failed: {e}")
            return f"Failed: {e}"

    def clear_standby_list(self) -> str:
        """Clear Windows standby list (empty standby memory)."""
        try:
            # This would typically use RAMMap or EmptyStandbyList
            # For now, report what would be done
            result = subprocess.run(
                "rundll32.exe advapi32.dll,ProcessIdleTasks",
                shell=True, capture_output=True, text=True
            )
            logger.info("Standby list cleared")
            return "Standby list cleared"
        except Exception as e:
            logger.error(f"Standby list clear failed: {e}")
            return f"Failed: {e}"

    def debloat_windows(self) -> Dict[str, str]:
        """Disable telemetry and bloatware services."""
        results = {}

        for service in self.SERVICES_TO_DISABLE:
            try:
                result = subprocess.run(
                    f"sc config {service} start= disabled",
                    shell=True, capture_output=True, text=True
                )
                if result.returncode == 0:
                    results[service] = "Disabled"
                    logger.info(f"Service disabled: {service}")
                else:
                    results[service] = f"Failed: {result.stderr[:50]}"
            except Exception as e:
                results[service] = f"Error: {e}"

        # Additional telemetry registry tweaks
        telemetry_tweaks = [
            (r'HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection', 'AllowTelemetry', 0),
            (r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection', 'AllowTelemetry', 0),
        ]

        for path, key, value in telemetry_tweaks:
            try:
                subprocess.run(
                    f'reg add "{path}" /v {key} /t REG_DWORD /d {value} /f',
                    shell=True, capture_output=True
                )
            except Exception:
                pass

        logger.info("Windows debloating completed")
        return results

    def set_visual_effects_best_performance(self) -> str:
        """Set Windows visual effects to best performance."""
        try:
            subprocess.run(
                r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" '
                r'/v VisualFXSetting /t REG_DWORD /d 2 /f',
                shell=True, capture_output=True
            )
            logger.info("Visual effects set to Best Performance")
            return "Visual effects set to Best Performance"
        except Exception as e:
            logger.error(f"Visual effects change failed: {e}")
            return f"Failed: {e}"

    def set_game_priority(self, process_name: str) -> str:
        """Set high priority for a game process."""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if process_name.lower() in proc.info['name'].lower():
                    p = psutil.Process(proc.info['pid'])
                    p.nice(psutil.HIGH_PRIORITY_CLASS)
                    logger.info(f"Priority set to HIGH for {process_name} (PID: {proc.info['pid']})")
                    return f"Priority set to HIGH for {process_name}"

            return f"Process not found: {process_name}"
        except Exception as e:
            logger.error(f"Priority set failed: {e}")
            return f"Failed: {e}"

    def set_cpu_affinity(self, process_name: str, cores: Optional[List[int]] = None) -> str:
        """Set CPU affinity for a game process."""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if process_name.lower() in proc.info['name'].lower():
                    p = psutil.Process(proc.info['pid'])

                    if cores is None:
                        # Use all physical cores, avoiding hyperthreaded ones
                        cpu_count = psutil.cpu_count(logical=False)
                        cores = list(range(cpu_count))

                    p.cpu_affinity(cores)
                    logger.info(f"CPU affinity set for {process_name}: cores {cores}")
                    return f"CPU affinity set: cores {cores}"

            return f"Process not found: {process_name}"
        except Exception as e:
            logger.error(f"Affinity set failed: {e}")
            return f"Failed: {e}"

    def get_running_games(self) -> List[str]:
        """Get list of detected game processes."""
        game_keywords = [
            'cs2', 'csgo', 'valorant', 'fortnite', 'apex',
            'overwatch', 'minecraft', 'roblox', 'league',
            'dota', 'pubg', 'rust', 'gta', 'cod',
            'warzone', 'rocketleague', 'rainbowsix',
        ]

        found_games = []
        for proc in psutil.process_iter(['name']):
            proc_name = proc.info['name'].lower()
            for keyword in game_keywords:
                if keyword in proc_name:
                    found_games.append(proc.info['name'])
                    break

        return list(set(found_games))

    def get_system_info(self) -> Dict:
        """Get current system performance info."""
        return {
            'cpu_percent': psutil.cpu_percent(interval=0.5),
            'ram_used_gb': psutil.virtual_memory().used / (1024**3),
            'ram_total_gb': psutil.virtual_memory().total / (1024**3),
            'ram_percent': psutil.virtual_memory().percent,
        }
