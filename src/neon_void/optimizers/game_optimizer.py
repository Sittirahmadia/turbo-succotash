"""
Game-Specific Optimizer for NEON VOID OPTIMIZER.
Auto-detection, per-game profiles, specialized optimization for popular titles.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional

import psutil

from ..core.config import config
from ..core.logger import logger


class GameOptimizer:
    """
    Per-game optimization with auto-detection.
    Supports 20+ popular titles with tailored profiles.
    """

    # Game executable names to detect
    SUPPORTED_GAMES = {
        "Valorant": ["VALORANT-Win64-Shipping.exe", "VALORANT.exe"],
        "CS2": ["cs2.exe"],
        "CSGO": ["csgo.exe"],
        "Fortnite": ["FortniteClient-Win64-Shipping.exe", "FortniteGame.exe"],
        "Apex Legends": ["r5apex.exe", "r5apex_dx12.exe"],
        "Overwatch": ["Overwatch.exe"],
        "Minecraft": ["javaw.exe", "Minecraft.Windows.exe"],
        "Roblox": ["RobloxPlayerBeta.exe"],
        "League of Legends": ["League of Legends.exe"],
        "Dota 2": ["dota2.exe"],
        "Genshin Impact": ["GenshinImpact.exe", "YuanShen.exe"],
        "Rust": ["RustClient.exe"],
        "GTA V": ["GTA5.exe", "GTAV.exe"],
        "PUBG": ["TslGame.exe"],
        "The Finals": ["Discovery.exe"],
        "Call of Duty": ["cod.exe", "ModernWarfare.exe", "MW2.exe"],
        "Rocket League": ["RocketLeague.exe"],
        "Rainbow Six": ["RainbowSix.exe", "RainbowSix_Vulkan.exe"],
        "Elden Ring": ["eldenring.exe"],
        "Cyberpunk 2077": ["Cyberpunk2077.exe"],
    }

    # Minecraft launcher executables
    MINECRAFT_LAUNCHERS = {
        "Official": "MinecraftLauncher.exe",
        "Prism": "prismlauncher.exe",
        "Modrinth": "ModrinthApp.exe",
        "CurseForge": "CurseForge.exe",
        "Lunar": "Lunar Client.exe",
        "Badlion": "BadlionClient.exe",
        "TLauncher": "TLauncher.exe",
        "MultiMC": "MultiMC.exe",
        "HMCL": "HMCL.exe",
    }

    # Optimization profiles per game
    DEFAULT_PROFILES = {
        "Valorant": {
            "fps_target": 240,
            "priority": "High",
            "cpu_affinity": "All",
            "network_optimization": True,
            "disable_fullscreen_optimizations": True,
        },
        "CS2": {
            "fps_target": 300,
            "priority": "High",
            "cpu_affinity": "All",
            "network_optimization": True,
            "disable_fullscreen_optimizations": True,
        },
        "Minecraft": {
            "fps_target": 144,
            "priority": "Above Normal",
            "jvm_flags": [
                "-XX:+UseG1GC",
                "-XX:+UnlockExperimentalVMOptions",
                "-XX:MaxGCPauseMillis=100",
                "-XX:+AlwaysPreTouch",
                "-XX:+DisableExplicitGC",
            ],
            "ram_allocation": 4,
            "network_optimization": False,
        },
        "Fortnite": {
            "fps_target": 144,
            "priority": "High",
            "disable_fullscreen_optimizations": True,
        },
        "Apex Legends": {
            "fps_target": 144,
            "priority": "High",
        },
    }

    def __init__(self) -> None:
        self._detected_games: Dict[str, int] = {}  # game_name -> pid
        self._current_game: Optional[str] = None

    def scan_for_games(self) -> Dict[str, int]:
        """Scan running processes for supported games."""
        detected = {}

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name']
                if not proc_name:
                    continue

                for game_name, executables in self.SUPPORTED_GAMES.items():
                    if any(exe.lower() == proc_name.lower() for exe in executables):
                        detected[game_name] = proc.info['pid']
                        logger.info(f"Game detected: {game_name} (PID: {proc.info['pid']})")

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self._detected_games = detected
        if detected:
            self._current_game = list(detected.keys())[0]

        return detected

    def get_detected_games(self) -> Dict[str, int]:
        """Get currently detected games."""
        return self._detected_games

    def get_current_game(self) -> Optional[str]:
        """Get the currently focused game."""
        return self._current_game

    def get_profile(self, game_name: str) -> Dict:
        """Get optimization profile for a game."""
        # Check for saved custom profile
        custom = config.get_profile(game_name)
        if custom:
            return custom

        # Return default profile
        return self.DEFAULT_PROFILES.get(game_name, self._get_generic_profile())

    def _get_generic_profile(self) -> Dict:
        """Get a generic gaming profile."""
        return {
            "fps_target": 144,
            "priority": "Above Normal",
            "cpu_affinity": "All",
            "network_optimization": True,
        }

    def save_profile(self, game_name: str, profile: Dict) -> None:
        """Save a custom profile for a game."""
        config.save_profile(game_name, profile)
        logger.info(f"Profile saved for {game_name}")

    def apply_profile(self, game_name: str) -> Dict[str, str]:
        """Apply optimization profile for a game."""
        profile = self.get_profile(game_name)
        results = {}

        try:
            # Set process priority if game is running
            if game_name in self._detected_games:
                pid = self._detected_games[game_name]
                proc = psutil.Process(pid)

                priority_str = profile.get("priority", "Normal")
                priority_map = {
                    "Realtime": psutil.REALTIME_PRIORITY_CLASS,
                    "High": psutil.HIGH_PRIORITY_CLASS,
                    "Above Normal": psutil.ABOVE_NORMAL_PRIORITY_CLASS,
                    "Normal": psutil.NORMAL_PRIORITY_CLASS,
                }
                proc.nice(priority_map.get(priority_str, psutil.NORMAL_PRIORITY_CLASS))
                results['priority'] = f"Set to {priority_str}"

            results['status'] = f"Profile applied for {game_name}"
            logger.info(f"Profile applied for {game_name}")

        except Exception as e:
            results['error'] = str(e)
            logger.error(f"Profile apply failed: {e}")

        return results

    # ===== MINECRAFT SPECIFIC =====

    def detect_minecraft_launcher(self) -> Optional[str]:
        """Detect which Minecraft launcher is installed."""
        for launcher_name, executable in self.MINECRAFT_LAUNCHERS.items():
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and proc.info['name'].lower() == executable.lower():
                    return launcher_name

        # Check for common install paths
        paths = [
            Path.home() / "AppData" / "Roaming" / ".minecraft",
            Path.home() / "AppData" / "Roaming" / ".PrismLauncher",
            Path.home() / "AppData" / "Roaming" / "ModrinthApp",
        ]
        for path in paths:
            if path.exists():
                if ".minecraft" in str(path):
                    return "Official (detected by folder)"
                elif "Prism" in str(path):
                    return "Prism (detected by folder)"
                elif "Modrinth" in str(path):
                    return "Modrinth (detected by folder)"

        return None

    def get_minecraft_jvm_flags(self, launcher: str) -> List[str]:
        """Get recommended JVM flags for Minecraft."""
        flags = [
            "-XX:+UseG1GC",
            "-XX:+ParallelRefProcEnabled",
            "-XX:MaxGCPauseMillis=200",
            "-XX:+UnlockExperimentalVMOptions",
            "-XX:+DisableExplicitGC",
            "-XX:+AlwaysPreTouch",
            "-XX:G1NewSizePercent=30",
            "-XX:G1MaxNewSizePercent=40",
            "-XX:G1HeapRegionSize=8M",
            "-XX:G1ReservePercent=20",
            "-XX:G1HeapWastePercent=5",
        ]

        if launcher in ["Lunar", "Badlion"]:
            # These launchers optimize automatically
            flags = ["-XX:+UseG1GC"]  # Minimal flags

        return flags

    def get_minecraft_optimization_tips(self) -> List[str]:
        """Get Minecraft-specific optimization tips."""
        return [
            "Use Fabric + Sodium for best performance",
            "Install Lithium, Starlight, and FerriteCore mods",
            "Reduce render distance to 8-12 chunks",
            "Use F3+B to show hitboxes (competitive)",
            "Allocate 4-6GB RAM for modded, 2-4GB for vanilla",
            "Use a lightweight resource pack",
            "Disable VSync and cap FPS at monitor refresh + 10",
            "Use performance shaders (Complementary/Shrimple)",
            "Enable Multithreaded Chunk Rendering if available",
        ]

    def get_game_specific_tips(self, game_name: str) -> List[str]:
        """Get optimization tips for any supported game."""
        tips = {
            "Valorant": [
                "Use Multithreaded Rendering",
                "Limit FPS to 1.5x your monitor refresh rate",
                "Enable NVIDIA Reflex Low Latency if available",
                "Use fullscreen exclusive mode",
            ],
            "CS2": [
                "Use -high -novid launch options",
                "Set fps_max to 0 or 400+",
                "Use 4:3 stretched for higher FPS (preference)",
                "Disable Steam overlay for more FPS",
            ],
            "Fortnite": [
                "Use Performance Mode (lowest latency)",
                "Set 3D Resolution to 100%",
                "Disable Motion Blur and Shadows",
                "Use DirectX 12 for better CPU usage",
            ],
            "Apex Legends": [
                "Use -high launch option",
                "Set fps_max to your monitor refresh",
                "Disable Volumetric Lighting",
                "Use TSAA anti-aliasing",
            ],
        }

        return tips.get(game_name, [
            "Close background applications",
            "Use fullscreen exclusive mode",
            "Update GPU drivers",
            "Disable Windows Game Bar overlay",
        ])
