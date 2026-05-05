"""
Build script for NEON VOID OPTIMIZER.
Creates a PyInstaller one-file executable with embedded assets.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def create_spec_file() -> str:
    """Create PyInstaller spec file with proper configuration."""
    # Get absolute paths to project root and source
    # This script is in project_root/scripts/build.py
    root_dir = Path(__file__).parent.parent.absolute()
    src_dir = (root_dir / "src").absolute()
    
    # Define paths
    main_py = (src_dir / "neon_void" / "__main__.py").as_posix()
    src_path = src_dir.as_posix()
    assets_dir = (src_dir / "neon_void" / "assets").as_posix()
    config_dir = (root_dir / "config").as_posix()
    icon_path = (src_dir / "neon_void" / "assets" / "images" / "icon.ico").as_posix()

    # Ensure directories exist to avoid PyInstaller errors
    os.makedirs(assets_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(os.path.dirname(icon_path), exist_ok=True)

    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{main_py}'],
    pathex=['{src_path}'],
    binaries=[],
    datas=[
        ('{assets_dir}', 'neon_void/assets'),
        ('{config_dir}', 'config'),
    ],
    hiddenimports=[
        'sklearn',
        'sklearn.ensemble',
        'sklearn.metrics',
        'sklearn.model_selection',
        'sklearn.preprocessing',
        'sklearn.tree._utils',
        'sklearn.utils._typedefs',
        'sklearn.neighbors._partition_nodes',
        'GPUtil',
        'psutil',
        'requests',
        'dns.resolver',
        'cpuinfo',
        'wmi',
        'pycaw.pycaw',
        'comtypes',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NEON_VOID_OPTIMIZER',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{icon_path}' if os.path.exists('{icon_path}') else None,
    # Admin manifest
    uac_admin=True,
)
"""
    return spec_content


def build() -> bool:
    """Build the executable using PyInstaller."""
    print("=" * 60)
    print("NEON VOID OPTIMIZER - Build Script")
    print("=" * 60)

    # Check PyInstaller
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Create spec file
    spec_path = Path("build.spec")
    with open(spec_path, 'w') as f:
        f.write(create_spec_file())
    print(f"Spec file created: {spec_path}")

    # Run PyInstaller
    print("\nBuilding executable...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", str(spec_path), "--clean", "--noconfirm"],
            capture_output=False,
            text=True,
        )

        if result.returncode == 0:
            print("\n" + "=" * 60)
            print("BUILD SUCCESSFUL!")
            print("=" * 60)
            print(f"Executable: dist/NEON_VOID_OPTIMIZER.exe")
            return True
        else:
            print("\nBUILD FAILED!")
            return False

    except Exception as e:
        print(f"Build error: {e}")
        return False


def clean() -> None:
    """Clean build artifacts."""
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for d in dirs_to_remove:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"Removed: {d}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="NEON VOID OPTIMIZER Build Script")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts")
    parser.add_argument("--build", action="store_true", help="Build executable")
    args = parser.parse_args()

    if args.clean:
        clean()
    elif args.build or len(sys.argv) == 1:
        build()
