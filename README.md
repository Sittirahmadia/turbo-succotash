# NEON VOID OPTIMIZER (CYBERPULSE)

**The ultimate all-in-one gaming optimization tool for competitive gamers.**

A premium Windows desktop application combining network latency optimization, FPS boosting, input lag reduction, VRAM optimization, CPU/GPU overclocking, advanced audio optimization, AI-powered latency prediction, and deep game-specific optimization — wrapped in an immersive cyberpunk interface with real-time 3D rendered backgrounds.

## Features

- **Real-time 3D Cyberpunk Interface** — ModernGL-powered animated scene with infinite wireframe grid, floating particles, and holographic effects
- **AI Latency Prediction** — Ensemble ML models predicting network spikes 5-60 seconds ahead with confidence intervals
- **Network & Latency Optimizer** — Complete TCP/IP stack control, DNS benchmarking, QoS tagging, route optimization
- **FPS & System Booster** — Ultimate Power Plan, Game Mode, HAGS, memory management, process priority
- **Input & Mouse Optimizer** — MarkC fix, Raw Accel integration, USB polling rate, registry tweaks
- **Graphics & Driver Optimizer** — NVIDIA/AMD/Intel 3D settings, shader cache, driver management
- **VRAM Optimizer** — Real-time monitoring, defragmentation, cache cleaning, per-game profiles
- **CPU/GPU Overclocking** — Safe presets, manual controls, temperature-based protection, per-game profiles
- **Audio Optimizer** — WASAPI exclusive mode, buffer optimization, latency reduction
- **Game-Specific Profiles** — Auto-detection and tailored optimization for 20+ popular titles
- **Advanced Tweaks** — 30+ registry tweaks, MSI Mode, DPC latency reduction, junk cleaner
- **Full Safety System** — Automatic backups, undo stack, anti-cheat awareness, risk warnings

## Requirements

- Windows 10 22H2 or Windows 11 (x64)
- Python 3.11+
- Administrator privileges (for system-level optimizations)
- GPU with OpenGL 3.3+ support (for 3D renderer)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/neon-void-optimizer.git
cd neon-void-optimizer

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m neon_void
```

## Building Executable

```bash
# Build with PyInstaller
python scripts/build.py

# Or manually:
pyinstaller build.spec
```

The compiled executable will be in `dist/NEON_VOID_OPTIMIZER.exe`.

## Architecture

```
neon_void/
  core/           # System monitoring, config, logging, i18n, backup
  ui/             # Dear PyGui theme, custom widgets, animations, layout
  renderer/       # ModernGL 3D cyberpunk scene renderer
  optimizers/     # All optimization modules (network, fps, input, etc.)
  ai/             # AI latency prediction engine
  utils/          # Helper utilities and system wrappers
  assets/         # Shaders, fonts, sounds, images
```

## License

Proprietary — All rights reserved.
