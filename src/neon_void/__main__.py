"""
NEON VOID OPTIMIZER (CYBERPULSE) - Main Entry Point
The ultimate all-in-one gaming optimization tool.
"""

import sys
import time
import threading

import dearpygui.dearpygui as dpg

from .core.i18n import translator, tr
from .core.logger import logger
from .core.config import config
from .core.system_monitor import system_monitor
from .core.backup_manager import backup_manager

from .ai.predictor import AIPredictor

from .optimizers.network_optimizer import NetworkOptimizer
from .optimizers.fps_booster import FPSBooster
from .optimizers.input_optimizer import InputOptimizer
from .optimizers.graphics_optimizer import GraphicsOptimizer
from .optimizers.vram_optimizer import VRAMOptimizer
from .optimizers.cpu_optimizer import CPUOverclocker
from .optimizers.gpu_optimizer import GPUOverclocker
from .optimizers.audio_optimizer import AudioOptimizer
from .optimizers.game_optimizer import GameOptimizer
from .optimizers.advanced_tweaks import AdvancedTweaks

from .ui.theme import initialize_themes, get_theme, COLORS


class NeonVoidApp:
    """
    Main application class for NEON VOID OPTIMIZER.
    Manages the UI, all optimizers, AI prediction, and system monitoring.
    """

    def __init__(self) -> None:
        self.ai = AIPredictor()
        self.network = NetworkOptimizer()
        self.fps = FPSBooster()
        self.input_opt = InputOptimizer()
        self.graphics = GraphicsOptimizer()
        self.vram = VRAMOptimizer()
        self.cpu_oc = CPUOverclocker()
        self.gpu_oc = GPUOverclocker()
        self.audio = AudioOptimizer()
        self.games = GameOptimizer()
        self.advanced = AdvancedTweaks()

        self._update_callbacks = []
        self._running = False

    def setup(self) -> None:
        """Initialize Dear PyGui and create the UI."""
        dpg.create_context()

        # Initialize themes
        initialize_themes()
        dpg.bind_theme(get_theme("global"))

        # Configure viewport
        dpg.create_viewport(
            title="NEON VOID OPTIMIZER v1.0",
            width=config.config.window_width,
            height=config.config.window_height,
            min_width=1200,
            min_height=700,
            resizable=True,
            vsync=False,  # Disable vsync for smoother UI
            small_icon="",
            large_icon=""
        )

        dpg.setup_dearpygui()

        # Create all UI windows
        self._create_main_window()

    def run(self) -> None:
        """Run the application main loop."""
        logger.info("=" * 60)
        logger.info("NEON VOID OPTIMIZER (CYBERPULSE) v1.0 Starting...")
        logger.info("=" * 60)

        # Start system monitoring
        system_monitor.start()
        self._running = True

        # Start update thread
        update_thread = threading.Thread(target=self._update_loop, daemon=True)
        update_thread.start()

        # Show viewport and start
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)

        logger.info("Application initialized successfully")
        logger.info(tr("ready"))

        try:
            dpg.start_dearpygui()
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()

    def shutdown(self) -> None:
        """Clean shutdown."""
        self._running = False
        system_monitor.stop()
        logger.info("Application shutting down...")
        dpg.destroy_context()

    def _create_main_window(self) -> None:
        """Create the main application window with all tabs."""
        with dpg.window(
            tag="main_window",
            label="NEON VOID OPTIMIZER",
            menubar=False,
            no_scrollbar=True,
            no_collapse=True,
            no_close=True,
        ):
            # Header bar
            self._create_header()

            # Tab bar
            with dpg.tab_bar(tag="main_tab_bar"):
                self._create_dashboard_tab()
                self._create_network_tab()
                self._create_fps_tab()
                self._create_input_tab()
                self._create_graphics_tab()
                self._create_vram_tab()
                self._create_cpu_oc_tab()
                self._create_gpu_oc_tab()
                self._create_audio_tab()
                self._create_games_tab()
                self._create_ai_tab()
                self._create_advanced_tab()
                self._create_settings_tab()

            # Status bar
            self._create_status_bar()

    def _create_header(self) -> None:
        """Create the application header."""
        with dpg.group(horizontal=True, height=50):
            # Title
            dpg.add_text("NEON VOID", color=COLORS["electric_cyan"], tag="header_title")
            dpg.bind_item_font("header_title", dpg.add_font("ProggyClean.ttf", 24))

            dpg.add_text("OPTIMIZER", color=COLORS["hot_magenta"], tag="header_subtitle")
            dpg.bind_item_font("header_subtitle", dpg.add_font("ProggyClean.ttf", 24))

            dpg.add_spacer(width=20)

            # Version
            dpg.add_text("v1.0", color=COLORS["gray"])

            dpg.add_spacer()

            # Health indicator
            dpg.add_text(tr("dash_system_health") + ":", color=COLORS["gray"])
            dpg.add_text("--", tag="header_health_value", color=COLORS["acid_green"])

    def _create_dashboard_tab(self) -> None:
        """Create the main dashboard tab."""
        with dpg.tab(label=tr("tab_dashboard"), tag="tab_dashboard"):
            with dpg.group(horizontal=True):
                # Left column - Metrics
                with dpg.child_window(width=900, height=-40):
                    # Real-time metrics grid
                    with dpg.group(horizontal=True):
                        self._create_metric_card("dash_ping", tr("dash_current_ping"), "0 ms", COLORS["electric_cyan"])
                        self._create_metric_card("dash_jitter", tr("dash_jitter"), "0 ms", COLORS["hot_magenta"])
                        self._create_metric_card("dash_pl", tr("dash_packet_loss"), "0%", COLORS["neon_purple"])
                        self._create_metric_card("dash_fps", tr("dash_fps"), "--", COLORS["acid_green"])

                    dpg.add_spacer(height=10)

                    with dpg.group(horizontal=True):
                        self._create_metric_card("dash_cpu", tr("dash_cpu_usage"), "0%", COLORS["electric_cyan"])
                        self._create_metric_card("dash_gpu", tr("dash_gpu_usage"), "0%", COLORS["hot_magenta"])
                        self._create_metric_card("dash_ram", tr("dash_ram_usage"), "0%", COLORS["neon_purple"])
                        self._create_metric_card("dash_vram", tr("dash_vram_usage"), "0%", COLORS["acid_green"])

                    dpg.add_spacer(height=10)

                    # Temperature row
                    with dpg.group(horizontal=True):
                        self._create_metric_card("dash_cputemp", tr("dash_cpu_temp"), "-- C", COLORS["electric_cyan"])
                        self._create_metric_card("dash_gputemp", tr("dash_gpu_temp"), "-- C", COLORS["hot_magenta"])
                        self._create_metric_card("dash_netspeed", tr("dash_net_speed"), "0/0 MB/s", COLORS["neon_purple"])
                        self._create_metric_card("dash_ai", tr("dash_ai_predicted"), "-- ms", COLORS["acid_green"])

                    # Health score and boost button
                    dpg.add_spacer(height=15)
                    with dpg.group(horizontal=True):
                        # Health score gauge
                        with dpg.child_window(width=300, height=120):
                            dpg.add_text(tr("dash_system_health"), color=COLORS["gray"])
                            dpg.add_text("0", tag="dash_health_score",
                                        color=COLORS["acid_green"], bullet=False)
                            dpg.bind_item_font("dash_health_score", dpg.add_font("ProggyClean.ttf", 48))

                        # Full Void Boost button
                        dpg.add_button(
                            label=tr("dash_full_void_boost"),
                            width=300, height=60,
                            callback=self._on_full_void_boost,
                            tag="btn_full_void_boost"
                        )
                        dpg.bind_item_theme("btn_full_void_boost", get_theme("glow_button_magenta"))

                        # Quick presets
                        with dpg.group():
                            dpg.add_text(tr("dash_presets"), color=COLORS["gray"])
                            with dpg.group(horizontal=True):
                                dpg.add_button(label=tr("dash_preset_competitive"),
                                             callback=lambda: self._apply_preset("competitive"), width=90)
                                dpg.add_button(label=tr("dash_preset_balanced"),
                                             callback=lambda: self._apply_preset("balanced"), width=90)
                                dpg.add_button(label=tr("dash_preset_extreme"),
                                             callback=lambda: self._apply_preset("extreme"), width=90)

                # Right column - Active game & logs
                with dpg.child_window(width=-1, height=-40):
                    dpg.add_text(tr("dash_active_game"), color=COLORS["electric_cyan"])
                    dpg.add_text(tr("dash_no_game"), tag="dash_active_game_value", color=COLORS["gray"])

                    dpg.add_spacer(height=10)

                    # Log window
                    dpg.add_text("LOGS", color=COLORS["gray"])
                    dpg.add_input_text(
                        multiline=True,
                        readonly=True,
                        width=-1,
                        height=-1,
                        tag="dash_log_window"
                    )

    def _create_metric_card(self, tag: str, label: str, value: str, color: tuple) -> None:
        """Create a metric display card."""
        with dpg.child_window(width=210, height=80):
            dpg.add_text(label, color=COLORS["gray"], tag=f"{tag}_label")
            dpg.add_text(value, color=color, tag=f"{tag}_value")

    def _create_network_tab(self) -> None:
        """Create Network & Latency Optimizer tab."""
        with dpg.tab(label=tr("tab_network"), tag="tab_network"):
            with dpg.group(horizontal=True):
                # Left column
                with dpg.child_window(width=500, height=-40):
                    dpg.add_text(tr("net_gaming_profile"), color=COLORS["electric_cyan"])
                    dpg.add_button(label="Apply Gaming TCP/IP Profile",
                                 callback=self._on_apply_network_profile, width=250)

                    dpg.add_spacer(height=10)
                    dpg.add_text(tr("net_tcp_ip"), color=COLORS["electric_cyan"])
                    dpg.add_checkbox(label=tr("net_nagle"), default_value=True, tag="net_nagle")
                    dpg.add_checkbox(label=tr("net_tcp_no_delay"), default_value=True, tag="net_tcp_nodelay")
                    dpg.add_checkbox(label=tr("net_tcp_ack"), default_value=True, tag="net_tcp_ack")
                    dpg.add_checkbox(label=tr("net_ecn"), default_value=True, tag="net_ecn")

                    dpg.add_spacer(height=10)
                    dpg.add_text(tr("net_mtu"), color=COLORS["electric_cyan"])
                    dpg.add_slider_int(label=tr("net_mtu_size"), default_value=1500,
                                     min_value=576, max_value=9000, tag="net_mtu_size")

                # Right column
                with dpg.child_window(width=-1, height=-40):
                    dpg.add_text(tr("net_dns"), color=COLORS["electric_cyan"])
                    dpg.add_button(label=tr("net_dns_benchmark"),
                                 callback=self._on_dns_benchmark, width=200)
                    dpg.add_text("Results:", tag="net_dns_results", color=COLORS["gray"])

                    dpg.add_spacer(height=10)
                    dpg.add_text(tr("net_latency_test"), color=COLORS["electric_cyan"])
                    dpg.add_button(label=tr("net_latency_run"),
                                 callback=self._on_latency_test, width=200)
                    dpg.add_text("Results:", tag="net_latency_results", color=COLORS["gray"])

    def _create_fps_tab(self) -> None:
        """Create FPS & System Booster tab."""
        with dpg.tab(label=tr("tab_fps"), tag="tab_fps"):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=450, height=-40):
                    dpg.add_text(tr("fps_power_plan"), color=COLORS["electric_cyan"])
                    dpg.add_button(label=tr("fps_neon_void_plan"),
                                 callback=self._on_power_plan, width=300)

                    dpg.add_spacer(height=10)
                    dpg.add_text(tr("fps_game_mode"), color=COLORS["electric_cyan"])
                    dpg.add_checkbox(label=tr("fps_game_mode_toggle"), tag="fps_game_mode")

                    dpg.add_spacer(height=10)
                    dpg.add_text(tr("fps_hags"), color=COLORS["electric_cyan"])
                    dpg.add_checkbox(label=tr("fps_hags_toggle"), tag="fps_hags")

                    dpg.add_spacer(height=10)
                    dpg.add_text(tr("fps_memory"), color=COLORS["electric_cyan"])
                    dpg.add_checkbox(label=tr("fps_large_cache"), tag="fps_large_cache")
                    dpg.add_button(label=tr("fps_clear_standby"),
                                 callback=self._on_clear_standby, width=200)

                with dpg.child_window(width=-1, height=-40):
                    dpg.add_text(tr("fps_debloat"), color=COLORS["electric_cyan"])
                    dpg.add_button(label=tr("fps_debloat_run"),
                                 callback=self._on_debloat, width=250)

                    dpg.add_spacer(height=10)
                    dpg.add_text(tr("fps_visual"), color=COLORS["electric_cyan"])
                    dpg.add_button(label=tr("fps_visual_best"),
                                 callback=self._on_visual_effects, width=250)

                    dpg.add_spacer(height=10)
                    dpg.add_text(tr("fps_process_manager"), color=COLORS["electric_cyan"])
                    dpg.add_input_text(label="Game Process Name", tag="fps_process_name", width=200)
                    dpg.add_button(label=tr("fps_set_priority"),
                                 callback=self._on_set_priority, width=200)

    def _create_input_tab(self) -> None:
        """Create Input & Mouse Optimizer tab."""
        with dpg.tab(label=tr("tab_input"), tag="tab_input"):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=450, height=-40):
                    dpg.add_text(tr("input_mouse"), color=COLORS["electric_cyan"])
                    dpg.add_button(label=tr("input_markc"),
                                 callback=self._on_markc_fix, width=250)

                    dpg.add_spacer(height=10)
                    dpg.add_text(tr("input_raw_accel"), color=COLORS["electric_cyan"])
                    dpg.add_combo(
                        items=list(self.input_opt.RAW_ACCEL_PRESETS.keys()),
                        label=tr("input_raw_accel_preset"),
                        tag="input_raw_preset", width=200
                    )
                    dpg.add_button(label="Apply Preset",
                                 callback=self._on_raw_accel_preset, width=200)

                    dpg.add_spacer(height=10)
                    dpg.add_text(tr("input_keyboard"), color=COLORS["electric_cyan"])
                    dpg.add_slider_int(label=tr("input_repeat_rate"),
                                     default_value=31, min_value=0, max_value=31, tag="input_repeat_rate")
                    dpg.add_slider_int(label=tr("input_repeat_delay"),
                                     default_value=0, min_value=0, max_value=3, tag="input_repeat_delay")

                with dpg.child_window(width=-1, height=-40):
                    dpg.add_text(tr("input_usb"), color=COLORS["electric_cyan"])
                    dpg.add_combo(
                        items=["125 Hz", "250 Hz", "500 Hz", "1000 Hz", "2000 Hz", "4000 Hz", "8000 Hz"],
                        label=tr("input_polling_rate"),
                        tag="input_polling_rate", default_value="1000 Hz"
                    )
                    dpg.add_button(label=tr("input_usb_tweaks"),
                                 callback=self._on_usb_tweaks, width=250)

    def _create_graphics_tab(self) -> None:
        """Create Graphics & Driver Optimizer tab."""
        with dpg.tab(label=tr("tab_graphics"), tag="tab_graphics"):
            dpg.add_text(f"GPU: {self.graphics.vendor}", tag="gfx_vendor_display", color=COLORS["electric_cyan"])

            with dpg.group(horizontal=True):
                with dpg.child_window(width=450, height=-40):
                    dpg.add_text(tr("gfx_driver"), color=COLORS["electric_cyan"])
                    dpg.add_button(label=tr("gfx_check_updates"),
                                 callback=self._on_check_driver, width=200)
                    dpg.add_text("Driver: ", tag="gfx_driver_info", color=COLORS["gray"])

                    dpg.add_spacer(height=10)
                    dpg.add_button(label=tr("gfx_shader_cache"),
                                 callback=self._on_clear_shader_cache, width=250)

                with dpg.child_window(width=-1, height=-40):
                    dpg.add_text("Settings for " + self.graphics.vendor, color=COLORS["electric_cyan"])
                    settings = self.graphics.get_settings()
                    for name, info in settings.items():
                        dpg.add_text(f"{name}: {info.get('description', '')}", color=COLORS["gray"])
                        dpg.add_text(f"Recommended: {info.get('recommended', 'N/A')}", color=COLORS["acid_green"])
                        dpg.add_separator()

    def _create_vram_tab(self) -> None:
        """Create VRAM Optimizer tab."""
        with dpg.tab(label=tr("tab_vram"), tag="tab_vram"):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=450, height=-40):
                    dpg.add_text(tr("vram_monitor"), color=COLORS["electric_cyan"])
                    dpg.add_text("Total: --", tag="vram_total", color=COLORS["gray"])
                    dpg.add_text("Used: --", tag="vram_used", color=COLORS["gray"])
                    dpg.add_text("Usage: --%", tag="vram_usage", color=COLORS["gray"])

                    dpg.add_spacer(height=10)
                    dpg.add_button(label=tr("vram_defrag_run"),
                                 callback=self._on_vram_defrag, width=200)

                with dpg.child_window(width=-1, height=-40):
                    dpg.add_text(tr("vram_cache"), color=COLORS["electric_cyan"])
                    dpg.add_button(label=tr("vram_dx_cache"),
                                 callback=lambda: self._on_clear_vram_cache("dx_shader"), width=250)
                    dpg.add_button(label=tr("vram_vulkan_cache"),
                                 callback=lambda: self._on_clear_vram_cache("vulkan"), width=250)

    def _create_cpu_oc_tab(self) -> None:
        """Create CPU Overclocking tab."""
        with dpg.tab(label=tr("tab_cpu_oc"), tag="tab_cpu_oc"):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=450, height=-40):
                    dpg.add_text(tr("cpu_monitor"), color=COLORS["electric_cyan"])
                    dpg.add_text("Clock: -- MHz", tag="cpu_clock", color=COLORS["gray"])
                    dpg.add_text("Temp: -- C", tag="cpu_temp", color=COLORS["gray"])
                    dpg.add_text("Usage: --%", tag="cpu_usage", color=COLORS["gray"])

                    dpg.add_spacer(height=10)
                    dpg.add_text(tr("cpu_presets"), color=COLORS["electric_cyan"])
                    for preset_name in self.cpu_oc.SAFETY_PRESETS.keys():
                        btn_tag = f"cpu_preset_{preset_name}"
                        dpg.add_button(label=preset_name,
                                     callback=lambda s, a, u=preset_name: self._on_cpu_preset(u),
                                     tag=btn_tag, width=200)

                with dpg.child_window(width=-1, height=-40):
                    dpg.add_text(tr("cpu_manual"), color=COLORS["electric_cyan"])
                    dpg.add_slider_float(label=tr("cpu_multiplier"), min_value=1.0,
                                        max_value=60.0, tag="cpu_manual_mult")
                    dpg.add_slider_int(label=tr("cpu_voltage_offset"), min_value=-200,
                                      max_value=200, tag="cpu_manual_volt")
                    dpg.add_button(label="Apply Manual OC",
                                 callback=self._on_cpu_manual_oc, width=200)

                    dpg.add_spacer(height=10)
                    dpg.add_text(tr("cpu_safety"), color=COLORS["hot_magenta"])
                    dpg.add_checkbox(label=tr("cpu_safety_toggle"), default_value=True, tag="cpu_safety_toggle")

    def _create_gpu_oc_tab(self) -> None:
        """Create GPU Overclocking tab."""
        with dpg.tab(label=tr("tab_gpu_oc"), tag="tab_gpu_oc"):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=450, height=-40):
                    dpg.add_text(tr("gpu_monitor"), color=COLORS["electric_cyan"])
                    dpg.add_text("Core: -- MHz", tag="gpu_core_clock", color=COLORS["gray"])
                    dpg.add_text("Mem: -- MHz", tag="gpu_mem_clock", color=COLORS["gray"])
                    dpg.add_text("Temp: -- C", tag="gpu_temp_oc", color=COLORS["gray"])

                    dpg.add_spacer(height=10)
                    for preset_name in self.gpu_oc.SAFETY_PRESETS.keys():
                        dpg.add_button(label=preset_name,
                                     callback=lambda s, a, u=preset_name: self._on_gpu_preset(u),
                                     width=200)

                with dpg.child_window(width=-1, height=-40):
                    dpg.add_text(tr("gpu_manual"), color=COLORS["electric_cyan"])
                    dpg.add_slider_int(label=tr("gpu_core_offset"), min_value=-200,
                                      max_value=500, tag="gpu_core_offset")
                    dpg.add_slider_int(label=tr("gpu_mem_offset"), min_value=-500,
                                      max_value=1500, tag="gpu_mem_offset")
                    dpg.add_slider_int(label=tr("gpu_power_limit_oc"), min_value=50,
                                      max_value=150, tag="gpu_power_limit")
                    dpg.add_button(label="Apply Manual OC",
                                 callback=self._on_gpu_manual_oc, width=200)

    def _create_audio_tab(self) -> None:
        """Create Audio Optimizer tab."""
        with dpg.tab(label=tr("tab_audio"), tag="tab_audio"):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=450, height=-40):
                    dpg.add_text(tr("audio_latency_monitor"), color=COLORS["electric_cyan"])
                    dpg.add_text("Latency: -- ms", tag="audio_latency_val", color=COLORS["gray"])

                    dpg.add_spacer(height=10)
                    dpg.add_button(label=tr("audio_competitive_mode"),
                                 callback=self._on_audio_competitive, width=250)
                    dpg.add_button(label=tr("audio_wasapi"),
                                 callback=self._on_wasapi_exclusive, width=250)

                with dpg.child_window(width=-1, height=-40):
                    dpg.add_text(tr("audio_buffer"), color=COLORS["electric_cyan"])
                    dpg.add_slider_int(label=tr("audio_buffer_size"), min_value=32,
                                      max_value=2048, default_value=128, tag="audio_buffer_size")
                    dpg.add_button(label="Apply Buffer Size",
                                 callback=self._on_set_buffer_size, width=200)

                    dpg.add_spacer(height=10)
                    dpg.add_checkbox(label=tr("audio_disable_enhancements"), tag="audio_disable_enh")

    def _create_games_tab(self) -> None:
        """Create Game-Specific Optimizer tab."""
        with dpg.tab(label=tr("tab_games"), tag="tab_games"):
            dpg.add_button(label=tr("games_scan"), callback=self._on_scan_games, width=200)
            dpg.add_text("Detected Games:", color=COLORS["electric_cyan"])
            dpg.add_text("None", tag="games_detected_list", color=COLORS["gray"])

            dpg.add_spacer(height=10)
            dpg.add_text(tr("games_minecraft"), color=COLORS["acid_green"])
            mc_launcher = self.games.detect_minecraft_launcher()
            dpg.add_text(f"Launcher: {mc_launcher or 'Not detected'}", tag="mc_launcher_info", color=COLORS["gray"])
            dpg.add_button(label="Get Minecraft Tips",
                         callback=self._on_minecraft_tips, width=200)

    def _create_ai_tab(self) -> None:
        """Create AI Prediction tab."""
        with dpg.tab(label=tr("tab_ai"), tag="tab_ai"):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=450, height=-40):
                    dpg.add_text(tr("ai_status"), color=COLORS["electric_cyan"])
                    dpg.add_text("Status: --", tag="ai_status_text", color=COLORS["gray"])
                    dpg.add_text("MAE: --", tag="ai_mae", color=COLORS["gray"])
                    dpg.add_text("Samples: --", tag="ai_samples", color=COLORS["gray"])

                    dpg.add_spacer(height=10)
                    dpg.add_button(label=tr("ai_retrain"),
                                 callback=self._on_ai_retrain, width=200)
                    dpg.add_button(label=tr("ai_reset"),
                                 callback=self._on_ai_reset, width=200)

                with dpg.child_window(width=-1, height=-40):
                    dpg.add_text(tr("ai_predictions"), color=COLORS["electric_cyan"])
                    dpg.add_text("5s: --", tag="ai_pred_5s", color=COLORS["gray"])
                    dpg.add_text("15s: --", tag="ai_pred_15s", color=COLORS["gray"])
                    dpg.add_text("30s: --", tag="ai_pred_30s", color=COLORS["gray"])
                    dpg.add_text("60s: --", tag="ai_pred_60s", color=COLORS["gray"])

                    dpg.add_spacer(height=10)
                    dpg.add_text(tr("ai_spike_probability"), color=COLORS["hot_magenta"])
                    dpg.add_text("--%", tag="ai_spike_prob", color=COLORS["gray"])

                    dpg.add_spacer(height=10)
                    dpg.add_checkbox(label=tr("ai_void_auto"), tag="ai_void_auto")

    def _create_advanced_tab(self) -> None:
        """Create Advanced Tweaks tab."""
        with dpg.tab(label=tr("tab_advanced"), tag="tab_advanced"):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=450, height=-40):
                    dpg.add_text(tr("adv_registry"), color=COLORS["electric_cyan"])
                    tweaks = self.advanced.get_registry_tweaks()
                    for tid, tinfo in list(tweaks.items())[:5]:  # Show first 5
                        with dpg.group(horizontal=True):
                            dpg.add_checkbox(label=tinfo["name"], tag=f"adv_tweak_{tid}")
                            dpg.add_text(f"[{tinfo['risk']}]", color=COLORS["yellow"] if tinfo['risk'] == 'medium' else COLORS["acid_green"])

                    dpg.add_button(label="Apply Selected Tweaks",
                                 callback=self._on_apply_tweaks, width=250)

                with dpg.child_window(width=-1, height=-40):
                    dpg.add_text(tr("adv_junk_cleaner"), color=COLORS["electric_cyan"])
                    dpg.add_button(label=tr("adv_junk_run"),
                                 callback=self._on_clean_junk, width=250)

                    dpg.add_spacer(height=10)
                    dpg.add_text(tr("adv_msi"), color=COLORS["electric_cyan"])
                    dpg.add_button(label=tr("adv_msi_enable"),
                                 callback=self._on_enable_msi, width=250)

    def _create_settings_tab(self) -> None:
        """Create Settings tab."""
        with dpg.tab(label=tr("tab_settings"), tag="tab_settings"):
            dpg.add_text(tr("set_language"), color=COLORS["electric_cyan"])
            dpg.add_radio_button(items=["English", "Bahasa Indonesia"],
                               callback=self._on_language_change, tag="set_language")

            dpg.add_spacer(height=10)
            dpg.add_checkbox(label=tr("set_3d_bg"), default_value=True, tag="set_3d_bg")
            dpg.add_checkbox(label=tr("set_crt_effect"), default_value=False, tag="set_crt")
            dpg.add_checkbox(label=tr("set_glitch_effect"), default_value=False, tag="set_glitch")
            dpg.add_checkbox(label=tr("set_sound"), default_value=False, tag="set_sound")
            dpg.add_checkbox(label=tr("set_overlay"), default_value=False, tag="set_overlay")
            dpg.add_checkbox(label=tr("set_startup"), default_value=False, tag="set_startup")

            dpg.add_spacer(height=10)
            dpg.add_button(label=tr("set_export_logs"),
                         callback=self._on_export_logs, width=200)

    def _create_status_bar(self) -> None:
        """Create the bottom status bar."""
        with dpg.group(horizontal=True, tag="status_bar"):
            dpg.add_text("Ready", tag="status_text", color=COLORS["gray"])
            dpg.add_spacer()
            dpg.add_text("NEON VOID v1.0", color=COLORS["dark_gray"])

    # ===== CALLBACK HANDLERS =====

    def _on_full_void_boost(self) -> None:
        """Apply all optimizations at once."""
        logger.info("FULL VOID BOOST activated!")
        dpg.set_value("status_text", "Applying Full Void Boost...")

        # Apply network profile
        self.network.apply_gaming_profile("")
        # Enable Game Mode
        self.fps.enable_game_mode()
        # Enable competitive audio
        self.audio.enable_competitive_mode()

        logger.info("Full Void Boost complete!")
        dpg.set_value("status_text", "Full Void Boost Applied!")

    def _apply_preset(self, preset: str) -> None:
        """Apply a quick preset."""
        logger.info(f"Applying {preset} preset")

    def _on_apply_network_profile(self) -> None:
        results = self.network.apply_gaming_profile("")
        logger.info(f"Network profile applied: {results}")

    def _on_dns_benchmark(self) -> None:
        dpg.set_value("net_dns_results", "Running benchmark...")
        results = self.network.benchmark_dns()
        text = "\\n".join([f"{k}: {v:.1f}ms" if isinstance(v, float) else f"{k}: {v}"
                          for k, v in results.items()])
        dpg.set_value("net_dns_results", text)

    def _on_latency_test(self) -> None:
        dpg.set_value("net_latency_results", "Testing...")
        result = self.network.test_latency()
        text = f"Avg: {result.avg_ms:.1f}ms | Jitter: {result.jitter_ms:.1f}ms | Loss: {result.packet_loss:.1f}%"
        dpg.set_value("net_latency_results", text)

    def _on_power_plan(self) -> None:
        result = self.fps.create_neon_void_power_plan()
        logger.info(result)

    def _on_clear_standby(self) -> None:
        result = self.fps.clear_standby_list()
        logger.info(result)

    def _on_debloat(self) -> None:
        results = self.fps.debloat_windows()
        logger.info(f"Debloat: {results}")

    def _on_visual_effects(self) -> None:
        result = self.fps.set_visual_effects_best_performance()
        logger.info(result)

    def _on_set_priority(self) -> None:
        process = dpg.get_value("fps_process_name")
        result = self.fps.set_game_priority(process)
        logger.info(result)

    def _on_markc_fix(self) -> None:
        result = self.input_opt.apply_markc_fix()
        logger.info(result)

    def _on_raw_accel_preset(self) -> None:
        preset = dpg.get_value("input_raw_preset")
        result = self.input_opt.set_raw_accel_preset(preset)
        logger.info(f"Raw Accel: {result}")

    def _on_usb_tweaks(self) -> None:
        result = self.input_opt.apply_usb_tweaks()
        logger.info(result)

    def _on_check_driver(self) -> None:
        info = self.graphics.get_driver_info()
        dpg.set_value("gfx_driver_info", f"Driver: {info.get('driver_version', 'Unknown')}")

    def _on_clear_shader_cache(self) -> None:
        result = self.graphics.clear_shader_cache()
        logger.info(result)

    def _on_vram_defrag(self) -> None:
        result = self.vram.defragment_vram()
        logger.info(result)

    def _on_clear_vram_cache(self, cache_type: str) -> None:
        results = self.vram.clear_cache(cache_type)
        logger.info(f"VRAM cache cleared: {results}")

    def _on_cpu_preset(self, preset: str) -> None:
        result = self.cpu_oc.apply_preset(preset)
        logger.info(f"CPU OC: {result}")

    def _on_cpu_manual_oc(self) -> None:
        mult = dpg.get_value("cpu_manual_mult")
        volt = dpg.get_value("cpu_manual_volt")
        result = self.cpu_oc.set_manual_oc(multiplier=mult, voltage_offset_mv=volt)
        logger.info(f"CPU Manual OC: {result}")

    def _on_gpu_preset(self, preset: str) -> None:
        result = self.gpu_oc.apply_preset(preset)
        logger.info(f"GPU OC: {result}")

    def _on_gpu_manual_oc(self) -> None:
        core = dpg.get_value("gpu_core_offset")
        mem = dpg.get_value("gpu_mem_offset")
        power = dpg.get_value("gpu_power_limit")
        result = self.gpu_oc.set_manual_oc(core, mem, None, power)
        logger.info(f"GPU Manual OC: {result}")

    def _on_audio_competitive(self) -> None:
        result = self.audio.enable_competitive_mode()
        logger.info(f"Audio: {result}")

    def _on_wasapi_exclusive(self) -> None:
        result = self.audio.force_wasapi_exclusive()
        logger.info(result)

    def _on_set_buffer_size(self) -> None:
        size = dpg.get_value("audio_buffer_size")
        result = self.audio.set_buffer_size(size)
        logger.info(result)

    def _on_scan_games(self) -> None:
        detected = self.games.scan_for_games()
        if detected:
            text = "\\n".join([f"{name} (PID: {pid})" for name, pid in detected.items()])
        else:
            text = "No games detected"
        dpg.set_value("games_detected_list", text)

    def _on_minecraft_tips(self) -> None:
        tips = self.games.get_minecraft_optimization_tips()
        logger.info("Minecraft tips:\\n" + "\\n".join(tips))

    def _on_ai_retrain(self) -> None:
        logger.info("AI retraining started...")
        self.ai.train(background=True)

    def _on_ai_reset(self) -> None:
        self.ai.reset_data()
        logger.info("AI data reset")

    def _on_apply_tweaks(self) -> None:
        tweaks = self.advanced.get_registry_tweaks()
        for tid in tweaks:
            if dpg.get_value(f"adv_tweak_{tid}"):
                result = self.advanced.apply_registry_tweak(tid)
                logger.info(f"Tweak {tid}: {result}")

    def _on_clean_junk(self) -> None:
        results = self.advanced.clean_junk_files()
        logger.info(f"Junk cleaned: {results}")

    def _on_enable_msi(self) -> None:
        result = self.advanced.enable_msi_mode()
        logger.info(result)

    def _on_language_change(self, sender, value) -> None:
        lang = "id" if value == "Bahasa Indonesia" else "en"
        from .core.i18n import Language
        translator.current_language = Language.INDONESIA if lang == "id" else Language.ENGLISH
        logger.info(f"Language changed to {value}")

    def _on_export_logs(self) -> None:
        import datetime
        filename = f"neon_void_logs_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        if backup_manager.export_logs(filename):
            logger.info(f"Logs exported to {filename}")
        else:
            logger.error("Failed to export logs")

    # ===== UPDATE LOOP =====

    def _update_loop(self) -> None:
        """Background update loop for real-time data."""
        while self._running:
            try:
                time.sleep(1.0)

                # Get current system snapshot
                snapshot = system_monitor.current

                # Collect AI data
                self.ai.collect_data_point({
                    'ping': snapshot.ping_ms,
                    'jitter': snapshot.jitter_ms,
                    'packet_loss': snapshot.packet_loss,
                    'bandwidth_down': snapshot.net_download_mbps,
                    'bandwidth_up': snapshot.net_upload_mbps,
                    'cpu_usage': snapshot.cpu_percent,
                    'ram_usage': snapshot.ram_percent,
                    'gpu_usage': snapshot.gpu_usage,
                    'vram_usage': snapshot.vram_percent,
                })

                # Update dashboard metrics
                try:
                    dpg.set_value("dash_ping_value", f"{snapshot.ping_ms:.0f} ms")
                    dpg.set_value("dash_jitter_value", f"{snapshot.jitter_ms:.1f} ms")
                    dpg.set_value("dash_pl_value", f"{snapshot.packet_loss:.1f}%")
                    dpg.set_value("dash_cpu_value", f"{snapshot.cpu_percent:.0f}%")
                    dpg.set_value("dash_gpu_value", f"{snapshot.gpu_usage:.0f}%")
                    dpg.set_value("dash_ram_value", f"{snapshot.ram_percent:.0f}%")
                    dpg.set_value("dash_vram_value", f"{snapshot.vram_percent:.0f}%")
                    dpg.set_value("dash_cputemp_value", f"{snapshot.cpu_temp or '--'} C")
                    dpg.set_value("dash_gputemp_value", f"{snapshot.gpu_temp or '--'} C")
                    dpg.set_value("dash_netspeed_value", f"{snapshot.net_download_mbps:.1f}/{snapshot.net_upload_mbps:.1f} MB/s")

                    # Health score
                    health = system_monitor.get_health_score()
                    dpg.set_value("dash_health_score", str(health))
                    dpg.configure_item("header_health_value", default_value=str(health))

                    # AI prediction
                    prediction = self.ai.predict({
                        'ping': snapshot.ping_ms,
                        'jitter': snapshot.jitter_ms,
                        'packet_loss': snapshot.packet_loss,
                        'bandwidth_down': snapshot.net_download_mbps,
                        'cpu_usage': snapshot.cpu_percent,
                        'ram_usage': snapshot.ram_percent,
                        'gpu_usage': snapshot.gpu_usage,
                        'vram_usage': snapshot.vram_percent,
                    })

                    if prediction:
                        dpg.set_value("dash_ai_value",
                                    f"{prediction.predictions.get(15, 0):.0f} ms")
                        dpg.set_value("ai_pred_5s",
                                    f"5s: {prediction.predictions.get(5, 0):.1f}ms")
                        dpg.set_value("ai_pred_15s",
                                    f"15s: {prediction.predictions.get(15, 0):.1f}ms")
                        dpg.set_value("ai_pred_30s",
                                    f"30s: {prediction.predictions.get(30, 0):.1f}ms")
                        dpg.set_value("ai_pred_60s",
                                    f"60s: {prediction.predictions.get(60, 0):.1f}ms")
                        dpg.set_value("ai_spike_prob",
                                    f"{prediction.spike_probability * 100:.0f}%")

                    # CPU OC tab
                    cpu_metrics = self.cpu_oc.get_metrics()
                    dpg.set_value("cpu_clock", f"Clock: {cpu_metrics.clock_speed_mhz:.0f} MHz")
                    dpg.set_value("cpu_temp", f"Temp: {cpu_metrics.temperature_c or '--'} C")
                    dpg.set_value("cpu_usage", f"Usage: {cpu_metrics.usage_percent:.0f}%")

                    # GPU OC tab
                    gpu_metrics = self.gpu_oc.get_metrics()
                    dpg.set_value("gpu_core_clock", f"Core: {gpu_metrics.core_clock_mhz:.0f} MHz")
                    dpg.set_value("gpu_mem_clock", f"Mem: {gpu_metrics.memory_clock_mhz:.0f} MHz")
                    dpg.set_value("gpu_temp_oc", f"Temp: {gpu_metrics.temperature_c or '--'} C")

                    # VRAM tab
                    vram_info = self.vram.get_vram_info()
                    dpg.set_value("vram_total", f"Total: {vram_info['total_mb']:.0f} MB")
                    dpg.set_value("vram_used", f"Used: {vram_info['used_mb']:.0f} MB")
                    dpg.set_value("vram_usage", f"Usage: {vram_info['usage_percent']:.1f}%")

                    # AI status
                    ai_status = self.ai.get_status()
                    status_text = "Training..." if ai_status.is_training else ai_status.status_message
                    dpg.set_value("ai_status_text", f"Status: {status_text}")
                    dpg.set_value("ai_mae", f"MAE: {ai_status.mae:.2f}ms")
                    dpg.set_value("ai_samples", f"Samples: {ai_status.samples_count}")

                except Exception as e:
                    pass  # DPG item might not exist yet

            except Exception as e:
                logger.debug(f"Update loop error: {e}")


def main() -> None:
    """Application entry point."""
    try:
        app = NeonVoidApp()
        app.setup()
        app.run()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
