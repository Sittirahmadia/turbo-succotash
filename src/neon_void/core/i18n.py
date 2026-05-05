"""
Internationalization module for NEON VOID OPTIMIZER.
Supports English and Bahasa Indonesia with easy extensibility.
"""

from enum import Enum
from typing import Dict, Any, Optional


class Language(Enum):
    ENGLISH = "en"
    INDONESIA = "id"


# Complete translation dictionary
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # ===== GENERAL =====
    "app_title": {
        "en": "NEON VOID OPTIMIZER",
        "id": "NEON VOID OPTIMIZER"
    },
    "app_subtitle": {
        "en": "ULTIMATE GAMING OPTIMIZATION SUITE",
        "id": "SUIT OPTIMASI GAMING ULTIMATE"
    },
    "version": {
        "en": "Version",
        "id": "Versi"
    },
    "loading": {
        "en": "INITIALIZING NEURAL INTERFACE...",
        "id": "MENGINISIALISASI ANTARMUKA NEURAL..."
    },
    "ready": {
        "en": "SYSTEM READY",
        "id": "SISTEM SIAP"
    },
    "apply": {
        "en": "APPLY",
        "id": "TERAPKAN"
    },
    "undo": {
        "en": "UNDO",
        "id": "BATALKAN"
    },
    "restore": {
        "en": "RESTORE DEFAULT",
        "id": "PULIHKAN DEFAULT"
    },
    "backup": {
        "en": "BACKUP",
        "id": "CADANGKAN"
    },
    "save": {
        "en": "SAVE",
        "id": "SIMPAN"
    },
    "cancel": {
        "en": "CANCEL",
        "id": "BATAL"
    },
    "close": {
        "en": "CLOSE",
        "id": "TUTUP"
    },
    "confirm": {
        "en": "CONFIRM",
        "id": "KONFIRMASI"
    },
    "warning": {
        "en": "WARNING",
        "id": "PERINGATAN"
    },
    "error": {
        "en": "ERROR",
        "id": "KESALAHAN"
    },
    "success": {
        "en": "SUCCESS",
        "id": "BERHASIL"
    },
    "info": {
        "en": "INFO",
        "id": "INFO"
    },
    "on": {
        "en": "ON",
        "id": "AKTIF"
    },
    "off": {
        "en": "OFF",
        "id": "NONAKTIF"
    },
    "enabled": {
        "en": "ENABLED",
        "id": "DIAKTIFKAN"
    },
    "disabled": {
        "en": "DISABLED",
        "id": "DINONAKTIFKAN"
    },
    "low": {
        "en": "LOW",
        "id": "RENDAH"
    },
    "medium": {
        "en": "MEDIUM",
        "id": "SEDANG"
    },
    "high": {
        "en": "HIGH",
        "id": "TINGGI"
    },
    "extreme": {
        "en": "EXTREME",
        "id": "EKSTREM"
    },
    "safe": {
        "en": "SAFE",
        "id": "AMAN"
    },
    "moderate": {
        "en": "MODERATE RISK",
        "id": "RISIKO SEDANG"
    },
    "dangerous": {
        "en": "DANGEROUS",
        "id": "BERBAHAYA"
    },

    # ===== TABS =====
    "tab_dashboard": {
        "en": "DASHBOARD",
        "id": "DASHBOARD"
    },
    "tab_network": {
        "en": "NETWORK",
        "id": "JARINGAN"
    },
    "tab_fps": {
        "en": "FPS BOOST",
        "id": "FPS BOOST"
    },
    "tab_input": {
        "en": "INPUT",
        "id": "INPUT"
    },
    "tab_graphics": {
        "en": "GRAPHICS",
        "id": "GRAFIS"
    },
    "tab_vram": {
        "en": "VRAM",
        "id": "VRAM"
    },
    "tab_cpu_oc": {
        "en": "CPU OC",
        "id": "CPU OC"
    },
    "tab_gpu_oc": {
        "en": "GPU OC",
        "id": "GPU OC"
    },
    "tab_audio": {
        "en": "AUDIO",
        "id": "AUDIO"
    },
    "tab_games": {
        "en": "GAMES",
        "id": "PERMAINAN"
    },
    "tab_ai": {
        "en": "AI PREDICT",
        "id": "AI PREDIKSI"
    },
    "tab_advanced": {
        "en": "ADVANCED",
        "id": "LANJUTAN"
    },
    "tab_settings": {
        "en": "SETTINGS",
        "id": "PENGATURAN"
    },

    # ===== DASHBOARD =====
    "dash_system_health": {
        "en": "SYSTEM HEALTH",
        "id": "KESEHATAN SISTEM"
    },
    "dash_current_ping": {
        "en": "CURRENT PING",
        "id": "PING SAAT INI"
    },
    "dash_jitter": {
        "en": "JITTER",
        "id": "JITTER"
    },
    "dash_packet_loss": {
        "en": "PACKET LOSS",
        "id": "PACKET LOSS"
    },
    "dash_fps": {
        "en": "FPS",
        "id": "FPS"
    },
    "dash_ai_predicted": {
        "en": "AI PREDICTED LATENCY",
        "id": "LATENSI PREDIKSI AI"
    },
    "dash_cpu_temp": {
        "en": "CPU TEMP",
        "id": "SUHU CPU"
    },
    "dash_gpu_temp": {
        "en": "GPU TEMP",
        "id": "SUHU GPU"
    },
    "dash_cpu_usage": {
        "en": "CPU USAGE",
        "id": "PENGGUNAAN CPU"
    },
    "dash_gpu_usage": {
        "en": "GPU USAGE",
        "id": "PENGGUNAAN GPU"
    },
    "dash_vram_usage": {
        "en": "VRAM USAGE",
        "id": "PENGGUNAAN VRAM"
    },
    "dash_ram_usage": {
        "en": "RAM USAGE",
        "id": "PENGGUNAAN RAM"
    },
    "dash_net_speed": {
        "en": "NETWORK SPEED",
        "id": "KECEPATAN JARINGAN"
    },
    "dash_audio_latency": {
        "en": "AUDIO LATENCY",
        "id": "LATENSI AUDIO"
    },
    "dash_full_void_boost": {
        "en": "FULL VOID BOOST",
        "id": "FULL VOID BOOST"
    },
    "dash_presets": {
        "en": "QUICK PRESETS",
        "id": "PRESET CEPAT"
    },
    "dash_preset_competitive": {
        "en": "COMPETITIVE",
        "id": "KOMPETITIF"
    },
    "dash_preset_balanced": {
        "en": "BALANCED",
        "id": "SEIMBANG"
    },
    "dash_preset_extreme": {
        "en": "EXTREME",
        "id": "EKSTREM"
    },
    "dash_preset_powersave": {
        "en": "POWER SAVE",
        "id": "HEMAT DAYA"
    },
    "dash_active_game": {
        "en": "ACTIVE GAME",
        "id": "PERMAINAN AKTIF"
    },
    "dash_no_game": {
        "en": "NO GAME DETECTED",
        "id": "TIDAK ADA PERMAINAN TERDETEKSI"
    },
    "dash_game_detected": {
        "en": "Game detected: {game}",
        "id": "Permainan terdeteksi: {game}"
    },

    # ===== NETWORK =====
    "net_adapter": {
        "en": "NETWORK ADAPTER",
        "id": "ADAPTER JARINGAN"
    },
    "net_gaming_profile": {
        "en": "GAMING OPTIMIZED PROFILE",
        "id": "PROFIL GAMING TEROPTIMASI"
    },
    "net_tcp_ip": {
        "en": "TCP/IP OPTIMIZATION",
        "id": "OPTIMASI TCP/IP"
    },
    "net_nagle": {
        "en": "Disable Nagle's Algorithm",
        "id": "Nonaktifkan Algoritma Nagle"
    },
    "net_tcp_no_delay": {
        "en": "TCP NoDelay",
        "id": "TCP NoDelay"
    },
    "net_tcp_ack": {
        "en": "TCP Ack Frequency",
        "id": "Frekuensi TCP Ack"
    },
    "net_autotuning": {
        "en": "TCP AutoTuning Level",
        "id": "Level AutoTuning TCP"
    },
    "net_congestion": {
        "en": "Congestion Provider",
        "id": "Penyedia Congestion"
    },
    "net_ecn": {
        "en": "ECN Capability",
        "id": "Kemampuan ECN"
    },
    "net_timestamps": {
        "en": "TCP Timestamps",
        "id": "Timestamp TCP"
    },
    "net_mtu": {
        "en": "MTU OPTIMIZATION",
        "id": "OPTIMASI MTU"
    },
    "net_mtu_size": {
        "en": "MTU Size",
        "id": "Ukuran MTU"
    },
    "net_pmtud": {
        "en": "Enable PMTUD",
        "id": "Aktifkan PMTUD"
    },
    "net_dns": {
        "en": "DNS OPTIMIZATION",
        "id": "OPTIMASI DNS"
    },
    "net_dns_benchmark": {
        "en": "DNS Benchmark",
        "id": "Benchmark DNS"
    },
    "net_dns_auto": {
        "en": "Auto-switch to fastest DNS",
        "id": "Otomatis pilih DNS tercepat"
    },
    "net_qos": {
        "en": "QoS TAGGING",
        "id": "TAGGING QoS"
    },
    "net_qos_game": {
        "en": "QoS Priority for Game",
        "id": "Prioritas QoS untuk Game"
    },
    "net_latency_test": {
        "en": "LATENCY TESTER",
        "id": "PENGUJI LATENSI"
    },
    "net_latency_run": {
        "en": "RUN TEST",
        "id": "JALANKAN TES"
    },
    "net_latency_history": {
        "en": "HISTORY",
        "id": "RIWAYAT"
    },

    # ===== FPS BOOST =====
    "fps_power_plan": {
        "en": "POWER PLAN",
        "id": "RENCANA DAYA"
    },
    "fps_neon_void_plan": {
        "en": "Activate NEON VOID Ultimate Plan",
        "id": "Aktifkan Rencana Ultimate NEON VOID"
    },
    "fps_game_mode": {
        "en": "WINDOWS GAME MODE",
        "id": "MODE PERMAINAN WINDOWS"
    },
    "fps_game_mode_toggle": {
        "en": "Enable Game Mode",
        "id": "Aktifkan Mode Permainan"
    },
    "fps_hags": {
        "en": "HARDWARE-ACCELERATED GPU SCHEDULING",
        "id": "PENJADWALAN GPU TERAKSELERASI HARDWARE"
    },
    "fps_hags_toggle": {
        "en": "Enable HAGS",
        "id": "Aktifkan HAGS"
    },
    "fps_timer": {
        "en": "TIMER RESOLUTION",
        "id": "RESOLUSI TIMER"
    },
    "fps_timer_resolution": {
        "en": "Timer Resolution (ms)",
        "id": "Resolusi Timer (ms)"
    },
    "fps_memory": {
        "en": "MEMORY MANAGEMENT",
        "id": "MANAJEMEN MEMORI"
    },
    "fps_large_cache": {
        "en": "Large System Cache",
        "id": "Cache Sistem Besar"
    },
    "fps_clear_standby": {
        "en": "Clear Standby List",
        "id": "Bersihkan Daftar Siaga"
    },
    "fps_debloat": {
        "en": "WINDOWS DEBLOAT",
        "id": "DEBLOAT WINDOWS"
    },
    "fps_debloat_run": {
        "en": "DISABLE TELEMETRY & BLOAT",
        "id": "NONAKTIFKAN TELEMETRI & BLOAT"
    },
    "fps_visual": {
        "en": "VISUAL EFFECTS",
        "id": "EFEK VISUAL"
    },
    "fps_visual_best": {
        "en": "Best Performance",
        "id": "Performa Terbaik"
    },
    "fps_process_manager": {
        "en": "PROCESS MANAGER",
        "id": "MANAJER PROSES"
    },
    "fps_set_priority": {
        "en": "Set Game Priority",
        "id": "Atur Prioritas Game"
    },
    "fps_set_affinity": {
        "en": "Set CPU Affinity",
        "id": "Atur CPU Affinity"
    },

    # ===== INPUT =====
    "input_mouse": {
        "en": "MOUSE OPTIMIZATION",
        "id": "OPTIMASI MOUSE"
    },
    "input_markc": {
        "en": "Apply MarkC Mouse Fix",
        "id": "Terapkan MarkC Mouse Fix"
    },
    "input_raw_accel": {
        "en": "RAW ACCELERATION",
        "id": "AKSELERASI RAW"
    },
    "input_raw_accel_preset": {
        "en": "Acceleration Preset",
        "id": "Preset Akselerasi"
    },
    "input_raw_input": {
        "en": "ENABLE RAW INPUT",
        "id": "AKTIFKAN RAW INPUT"
    },
    "input_raw_input_toggle": {
        "en": "Raw Input Buffer",
        "id": "Buffer Raw Input"
    },
    "input_keyboard": {
        "en": "KEYBOARD OPTIMIZATION",
        "id": "OPTIMASI KEYBOARD"
    },
    "input_repeat_rate": {
        "en": "Repeat Rate",
        "id": "Kecepatan Ulang"
    },
    "input_repeat_delay": {
        "en": "Repeat Delay",
        "id": "Jeda Ulang"
    },
    "input_usb": {
        "en": "USB POLLING & LATENCY",
        "id": "POLLING & LATENSI USB"
    },
    "input_polling_rate": {
        "en": "Polling Rate (Hz)",
        "id": "Kecepatan Polling (Hz)"
    },
    "input_usb_tweaks": {
        "en": "Apply USB Latency Tweaks",
        "id": "Terapkan Tweak Latensi USB"
    },

    # ===== GRAPHICS =====
    "gfx_gpu_vendor": {
        "en": "GPU VENDOR",
        "id": "VENDOR GPU"
    },
    "gfx_low_latency": {
        "en": "Low Latency Mode",
        "id": "Mode Latensi Rendah"
    },
    "gfx_max_perf": {
        "en": "Maximum Performance",
        "id": "Performa Maksimum"
    },
    "gfx_shader_cache": {
        "en": "Clear Shader Cache",
        "id": "Bersihkan Cache Shader"
    },
    "gfx_driver": {
        "en": "DRIVER",
        "id": "DRIVER"
    },
    "gfx_check_updates": {
        "en": "Check for Updates",
        "id": "Periksa Pembaruan"
    },

    # ===== VRAM =====
    "vram_monitor": {
        "en": "VRAM MONITOR",
        "id": "MONITOR VRAM"
    },
    "vram_current": {
        "en": "Current Usage",
        "id": "Penggunaan Saat Ini"
    },
    "vram_total": {
        "en": "Total VRAM",
        "id": "VRAM Total"
    },
    "vram_defrag": {
        "en": "VRAM DEFRAGMENT",
        "id": "DEFRAGMENT VRAM"
    },
    "vram_defrag_run": {
        "en": "DEFRAGMENT VRAM",
        "id": "DEFRAGMENT VRAM"
    },
    "vram_cache": {
        "en": "CACHE CLEANING",
        "id": "PENBERSIHAN CACHE"
    },
    "vram_dx_cache": {
        "en": "Clear DirectX Shader Cache",
        "id": "Bersihkan Cache Shader DirectX"
    },
    "vram_vulkan_cache": {
        "en": "Clear Vulkan Cache",
        "id": "Bersihkan Cache Vulkan"
    },
    "vram_profiles": {
        "en": "PER-GAME PROFILES",
        "id": "PROFIL PER-GAME"
    },
    "vram_limit": {
        "en": "VRAM Limit (MB)",
        "id": "Batas VRAM (MB)"
    },

    # ===== CPU OC =====
    "cpu_monitor": {
        "en": "CPU MONITOR",
        "id": "MONITOR CPU"
    },
    "cpu_clock": {
        "en": "Clock Speed",
        "id": "Kecepatan Clock"
    },
    "cpu_voltage": {
        "en": "Voltage",
        "id": "Voltase"
    },
    "cpu_presets": {
        "en": "OVERCLOCK PRESETS",
        "id": "PRESET OVERCLOCK"
    },
    "cpu_preset_gaming": {
        "en": "GAMING",
        "id": "GAMING"
    },
    "cpu_preset_highperf": {
        "en": "HIGH PERFORMANCE",
        "id": "PERFORMA TINGGI"
    },
    "cpu_preset_extreme": {
        "en": "EXTREME",
        "id": "EKSTREM"
    },
    "cpu_manual": {
        "en": "MANUAL OVERCLOCK",
        "id": "OVERCLOCK MANUAL"
    },
    "cpu_multiplier": {
        "en": "Multiplier",
        "id": "Pengganda"
    },
    "cpu_voltage_offset": {
        "en": "Voltage Offset (mV)",
        "id": "Offset Voltase (mV)"
    },
    "cpu_power_limit": {
        "en": "Power Limit (W)",
        "id": "Batas Daya (W)"
    },
    "cpu_temp_limit": {
        "en": "Temperature Limit (C)",
        "id": "Batas Suhu (C)"
    },
    "cpu_safety": {
        "en": "SAFETY PROTECTION",
        "id": "PROTEKSI KEAMANAN"
    },
    "cpu_safety_toggle": {
        "en": "Enable Temperature Protection",
        "id": "Aktifkan Proteksi Suhu"
    },
    "cpu_stress_test": {
        "en": "STRESS TEST",
        "id": "TES STRES"
    },
    "cpu_stress_run": {
        "en": "RUN STRESS TEST",
        "id": "JALANKAN TES STRES"
    },

    # ===== GPU OC =====
    "gpu_monitor": {
        "en": "GPU MONITOR",
        "id": "MONITOR GPU"
    },
    "gpu_core_clock": {
        "en": "Core Clock",
        "id": "Clock Core"
    },
    "gpu_mem_clock": {
        "en": "Memory Clock",
        "id": "Clock Memori"
    },
    "gpu_power_draw": {
        "en": "Power Draw",
        "id": "Penggunaan Daya"
    },
    "gpu_fan_speed": {
        "en": "Fan Speed",
        "id": "Kecepatan Kipas"
    },
    "gpu_core_offset": {
        "en": "Core Offset (MHz)",
        "id": "Offset Core (MHz)"
    },
    "gpu_mem_offset": {
        "en": "Memory Offset (MHz)",
        "id": "Offset Memori (MHz)"
    },
    "gpu_volt_offset": {
        "en": "Voltage Offset (mV)",
        "id": "Offset Voltase (mV)"
    },
    "gpu_power_limit_oc": {
        "en": "Power Limit (%)",
        "id": "Batas Daya (%)"
    },
    "gpu_fan_curve": {
        "en": "CUSTOM FAN CURVE",
        "id": "KURVA KIPAS KUSTOM"
    },
    "gpu_stability": {
        "en": "STABILITY MONITOR",
        "id": "MONITOR STABILITAS"
    },

    # ===== AUDIO =====
    "audio_latency_monitor": {
        "en": "AUDIO LATENCY MONITOR",
        "id": "MONITOR LATENSI AUDIO"
    },
    "audio_competitive_mode": {
        "en": "COMPETITIVE LOW LATENCY MODE",
        "id": "MODE LATENSI RENDAH KOMPETITIF"
    },
    "audio_wasapi": {
        "en": "FORCE WASAPI EXCLUSIVE",
        "id": "PAKSA WASAPI EKSKLUSIF"
    },
    "audio_buffer": {
        "en": "BUFFER SIZE",
        "id": "UKURAN BUFFER"
    },
    "audio_buffer_size": {
        "en": "Buffer Size (samples)",
        "id": "Ukuran Buffer (sampel)"
    },
    "audio_sample_rate": {
        "en": "SAMPLE RATE",
        "id": "SAMPLE RATE"
    },
    "audio_disable_enhancements": {
        "en": "DISABLE AUDIO ENHANCEMENTS",
        "id": "NONAKTIFKAN PENINGKAT AUDIO"
    },
    "audio_enhancements_toggle": {
        "en": "Disable All Enhancements",
        "id": "Nonaktifkan Semua Peningkat"
    },
    "audio_mic": {
        "en": "MICROPHONE OPTIMIZATION",
        "id": "OPTIMASI MIKROFON"
    },
    "audio_mic_boost": {
        "en": "Mic Boost",
        "id": "Penguat Mic"
    },
    "audio_noise_suppression": {
        "en": "Noise Suppression",
        "id": "Penekan Kebisingan"
    },
    "audio_profiles": {
        "en": "AUDIO PROFILES",
        "id": "PROFIL AUDIO"
    },
    "audio_profile_competitive": {
        "en": "COMPETITIVE",
        "id": "KOMPETITIF"
    },
    "audio_profile_entertainment": {
        "en": "ENTERTAINMENT",
        "id": "HIBURAN"
    },

    # ===== GAMES =====
    "games_detected": {
        "en": "DETECTED GAMES",
        "id": "PERMAINAN TERDETEKSI"
    },
    "games_scan": {
        "en": "SCAN FOR GAMES",
        "id": "PINDAI PERMAINAN"
    },
    "games_profile_for": {
        "en": "PROFILE: {game}",
        "id": "PROFIL: {game}"
    },
    "games_minecraft": {
        "en": "MINECRAFT OPTIMIZER",
        "id": "OPTIMASI MINECRAFT"
    },
    "games_minecraft_launcher": {
        "en": "Launcher",
        "id": "Launcher"
    },
    "games_minecraft_jvm": {
        "en": "JVM Flags",
        "id": "Flag JVM"
    },
    "games_minecraft_ram": {
        "en": "RAM Allocation (GB)",
        "id": "Alokasi RAM (GB)"
    },
    "games_minecraft_mods": {
        "en": "Performance Mods",
        "id": "Mod Performa"
    },
    "games_minecraft_shaders": {
        "en": "Shader Optimization",
        "id": "Optimasi Shader"
    },
    "games_minecraft_backup": {
        "en": "Backup Worlds",
        "id": "Cadangkan Dunia"
    },
    "games_fps_target": {
        "en": "FPS Target",
        "id": "Target FPS"
    },
    "games_net_opt": {
        "en": "Network Optimization",
        "id": "Optimasi Jaringan"
    },
    " games_gfx_opt": {
        "en": "Graphics Optimization",
        "id": "Optimasi Grafis"
    },
    "games_apply_profile": {
        "en": "APPLY GAME PROFILE",
        "id": "TERAPKAN PROFIL GAME"
    },

    # ===== AI PREDICTION =====
    "ai_status": {
        "en": "AI STATUS",
        "id": "STATUS AI"
    },
    "ai_training": {
        "en": "Training...",
        "id": "Sedang Melatih..."
    },
    "ai_last_trained": {
        "en": "Last Trained",
        "id": "Terakhir Dilatih"
    },
    "ai_accuracy": {
        "en": "Model Accuracy (MAE)",
        "id": "Akurasi Model (MAE)"
    },
    "ai_predictions": {
        "en": "PREDICTIONS",
        "id": "PREDIKSI"
    },
    "ai_predict_5s": {
        "en": "5 seconds",
        "id": "5 detik"
    },
    "ai_predict_15s": {
        "en": "15 seconds",
        "id": "15 detik"
    },
    "ai_predict_30s": {
        "en": "30 seconds",
        "id": "30 detik"
    },
    "ai_predict_60s": {
        "en": "60 seconds",
        "id": "60 detik"
    },
    "ai_spike_probability": {
        "en": "SPIKE PROBABILITY",
        "id": "PROBABILITAS SPIKE"
    },
    "ai_void_mode": {
        "en": "AI VOID MODE",
        "id": "MODE AI VOID"
    },
    "ai_void_auto": {
        "en": "Auto-optimize on predicted spike",
        "id": "Otomatis optimasi saat spike diprediksi"
    },
    "ai_suggestions": {
        "en": "AI SUGGESTIONS",
        "id": "SARAN AI"
    },
    "ai_feature_importance": {
        "en": "FEATURE IMPORTANCE",
        "id": "PENTINGNYA FITUR"
    },
    "ai_retrain": {
        "en": "RETRAIN MODEL",
        "id": "LATIH ULANG MODEL"
    },
    "ai_reset": {
        "en": "RESET AI DATA",
        "id": "RESET DATA AI"
    },
    "ai_enable": {
        "en": "ENABLE AI PREDICTION",
        "id": "AKTIFKAN PREDIKSI AI"
    },
    "ai_data_local": {
        "en": "All AI data is stored locally. No cloud upload.",
        "id": "Semua data AI disimpan secara lokal. Tidak ada upload ke cloud."
    },

    # ===== ADVANCED =====
    "adv_registry": {
        "en": "REGISTRY TWEAKS",
        "id": "TWEAK REGISTRY"
    },
    "adv_services": {
        "en": "SERVICES OPTIMIZATION",
        "id": "OPTIMASI LAYANAN"
    },
    "adv_msi": {
        "en": "MSI MODE",
        "id": "MODE MSI"
    },
    "adv_msi_enable": {
        "en": "Enable MSI Mode for GPU",
        "id": "Aktifkan Mode MSI untuk GPU"
    },
    "adv_dpc": {
        "en": "DPC LATENCY",
        "id": "LATENSI DPC"
    },
    "adv_dpc_check": {
        "en": "CHECK DPC LATENCY",
        "id": "PERIKSA LATENSI DPC"
    },
    "adv_junk_cleaner": {
        "en": "JUNK CLEANER",
        "id": "PEBERSIH SAMPAH"
    },
    "adv_junk_run": {
        "en": "CLEAN JUNK FILES",
        "id": "BERSIHKAN FILE SAMPAH"
    },
    "adv_prefetch": {
        "en": "PREFETCH OPTIMIZER",
        "id": "OPTIMASI PREFETCH"
    },

    # ===== SETTINGS =====
    "set_language": {
        "en": "LANGUAGE",
        "id": "BAHASA"
    },
    "set_theme": {
        "en": "THEME",
        "id": "TEMA"
    },
    "set_3d_bg": {
        "en": "3D ANIMATED BACKGROUND",
        "id": "BACKGROUND 3D ANIMASI"
    },
    "set_crt_effect": {
        "en": "CRT SCANLINE EFFECT",
        "id": "EFEK SCANLINE CRT"
    },
    "set_glitch_effect": {
        "en": "GLITCH EFFECT",
        "id": "EFEK GLITCH"
    },
    "set_sound": {
        "en": "SOUND EFFECTS",
        "id": "EFEK SUARA"
    },
    "set_overlay": {
        "en": "IN-GAME OVERLAY",
        "id": "OVERLAY IN-GAME"
    },
    "set_startup": {
        "en": "START WITH WINDOWS",
        "id": "MULAI DENGAN WINDOWS"
    },
    "set_minimize": {
        "en": "MINIMIZE TO TRAY",
        "id": "MINIMIZE KE TRAY"
    },
    "set_update": {
        "en": "CHECK FOR UPDATES",
        "id": "PERIKSA PEMBARUAN"
    },
    "set_logs": {
        "en": "VIEW LOGS",
        "id": "LIHAT LOG"
    },
    "set_export_logs": {
        "en": "EXPORT LOGS",
        "id": "EKSPOR LOG"
    },
    "set_about": {
        "en": "ABOUT",
        "id": "TENTANG"
    },

    # ===== LOG MESSAGES =====
    "log_app_start": {
        "en": "Application started",
        "id": "Aplikasi dimulai"
    },
    "log_app_exit": {
        "en": "Application shutting down",
        "id": "Aplikasi dimatikan"
    },
    "log_admin_required": {
        "en": "Administrator privileges required for this operation",
        "id": "Hak administrator diperlukan untuk operasi ini"
    },
    "log_backup_created": {
        "en": "Backup created: {name}",
        "id": "Cadangan dibuat: {name}"
    },
    "log_backup_restored": {
        "en": "Backup restored: {name}",
        "id": "Cadangan dipulihkan: {name}"
    },
    "log_tweak_applied": {
        "en": "Tweak applied: {name}",
        "id": "Tweak diterapkan: {name}"
    },
    "log_tweet_reverted": {
        "en": "Tweak reverted: {name}",
        "id": "Tweak dibatalkan: {name}"
    },
    "log_ai_trained": {
        "en": "AI model trained. MAE: {mae:.2f}",
        "id": "Model AI dilatih. MAE: {mae:.2f}"
    },
    "log_game_detected": {
        "en": "Game detected: {game} (PID: {pid})",
        "id": "Permainan terdeteksi: {game} (PID: {pid})"
    },
    "log_error": {
        "en": "Error: {error}",
        "id": "Kesalahan: {error}"
    },
}


class I18n:
    """Internationalization manager with singleton pattern."""
    _instance: Optional['I18n'] = None

    def __new__(cls) -> 'I18n':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._current_lang = Language.ENGLISH
        return cls._instance

    @property
    def current_language(self) -> Language:
        return self._current_lang

    @current_language.setter
    def current_language(self, lang: Language) -> None:
        self._current_lang = lang

    def get(self, key: str, **kwargs: Any) -> str:
        """Get translated string by key with optional format arguments."""
        translation = TRANSLATIONS.get(key, {})
        text = translation.get(self._current_lang.value,
                               translation.get("en", key))
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        return text

    def toggle_language(self) -> None:
        """Toggle between English and Indonesia."""
        if self._current_lang == Language.ENGLISH:
            self._current_lang = Language.INDONESIA
        else:
            self._current_lang = Language.ENGLISH


# Global translator instance
translator = I18n()


def tr(key: str, **kwargs: Any) -> str:
    """Shorthand function for translation."""
    return translator.get(key, **kwargs)
