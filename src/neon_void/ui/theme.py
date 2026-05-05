"""
Cyberpunk Theme Engine for NEON VOID OPTIMIZER.
Creates the immersive glassmorphism UI with neon accents using Dear PyGui.
"""

import dearpygui.dearpygui as dpg

# Color palette - Cyberpunk theme
COLORS = {
    "void_black": (10, 10, 15, 255),
    "deep_black": (15, 15, 25, 255),
    "panel_bg": (20, 20, 35, 220),
    "panel_bg_hover": (30, 30, 50, 230),
    "electric_cyan": (0, 240, 255),
    "electric_cyan_dim": (0, 180, 200, 180),
    "hot_magenta": (255, 0, 170),
    "hot_magenta_dim": (200, 0, 140, 180),
    "neon_purple": (170, 0, 255),
    "acid_green": (57, 255, 20),
    "acid_green_dim": (40, 200, 15, 180),
    "neon_orange": (255, 140, 0),
    "white": (240, 240, 255, 255),
    "gray": (150, 150, 170, 255),
    "dark_gray": (80, 80, 100, 255),
    "red": (255, 50, 50, 255),
    "yellow": (255, 220, 0, 255),
    "transparent": (0, 0, 0, 0),
    "glass_bg": (25, 25, 40, 200),
    "glass_border": (0, 240, 255, 80),
    "glass_border_hover": (0, 240, 255, 160),
    "glow_cyan": (0, 240, 255, 40),
    "glow_magenta": (255, 0, 170, 40),
}

# Gradients
GRADIENTS = {
    "cyber_pulse": [COLORS["electric_cyan"], COLORS["neon_purple"], COLORS["hot_magenta"]],
    "health_good": [COLORS["acid_green"], (0, 200, 100)],
    "health_warn": [COLORS["yellow"], COLORS["neon_orange"]],
    "health_danger": [COLORS["red"], COLORS["hot_magenta"]],
}


def create_global_theme() -> int:
    """Create and configure the global Dear PyGui cyberpunk theme."""

    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            # Window styling
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, COLORS["void_black"])
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, COLORS["deep_black"])
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, COLORS["deep_black"])
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, COLORS["void_black"])
            dpg.add_theme_color(dpg.mvThemeCol_Border, COLORS["electric_cyan_dim"])
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, COLORS["glow_cyan"])
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, COLORS["deep_black"])

            # Button styling
            dpg.add_theme_color(dpg.mvThemeCol_Button, COLORS["deep_black"])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, COLORS["panel_bg_hover"])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, COLORS["electric_cyan_dim"])

            # Frame/input styling
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, COLORS["deep_black"])
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, COLORS["panel_bg_hover"])
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, COLORS["electric_cyan_dim"])
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, COLORS["glass_bg"])

            # Text styling
            dpg.add_theme_color(dpg.mvThemeCol_Text, COLORS["white"])
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, COLORS["dark_gray"])
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, COLORS["electric_cyan_dim"])

            # Slider/checkbox
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, COLORS["electric_cyan"])
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, COLORS["electric_cyan"])
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, COLORS["hot_magenta"])

            # Header
            dpg.add_theme_color(dpg.mvThemeCol_Header, COLORS["panel_bg"])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, COLORS["panel_bg_hover"])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, COLORS["electric_cyan_dim"])

            # Tab styling
            dpg.add_theme_color(dpg.mvThemeCol_Tab, COLORS["deep_black"])
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, COLORS["panel_bg_hover"])
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, COLORS["electric_cyan_dim"])
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused, COLORS["deep_black"])
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, COLORS["panel_bg"])

            # Resize grip
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip, COLORS["electric_cyan_dim"])
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered, COLORS["electric_cyan"])
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive, COLORS["hot_magenta"])

            # Scrollbar
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, COLORS["void_black"])
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, COLORS["dark_gray"])
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, COLORS["gray"])
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, COLORS["electric_cyan"])

            # Style variables
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 3)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 3)
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 1)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 6)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 12, 12)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 4)

    return global_theme


def create_neon_button_theme(color_key: str = "electric_cyan") -> int:
    """Create a neon-styled button theme."""
    color = COLORS.get(color_key, COLORS["electric_cyan"])
    dim_color = (*color[:3], 180)

    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (*color[:3], 40))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (*color[:3], 100))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, dim_color)
            dpg.add_theme_color(dpg.mvThemeCol_Border, color)
            dpg.add_theme_color(dpg.mvThemeCol_Text, color)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)

    return theme


def create_glow_button_theme(color_key: str = "electric_cyan") -> int:
    """Create a glowing button theme for primary actions."""
    color = COLORS.get(color_key, COLORS["electric_cyan"])

    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (*color[:3], 180))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (*color[:3], 230))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, color)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 16, 8)

    return theme


def create_glass_panel_theme() -> int:
    """Create a glassmorphism panel theme."""
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvChildWindow):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, COLORS["glass_bg"])
            dpg.add_theme_color(dpg.mvThemeCol_Border, COLORS["glass_border"])
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 1)

    return theme


def create_danger_button_theme() -> int:
    """Create a danger/red button theme."""
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 50, 50, 80))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 50, 50, 150))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, COLORS["hot_magenta"])
            dpg.add_theme_color(dpg.mvThemeCol_Text, COLORS["red"])
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1)

    return theme


def get_health_color(score: int):
    """Get color based on health score (0-100)."""
    if score >= 80:
        return COLORS["acid_green"]
    elif score >= 60:
        return COLORS["yellow"]
    elif score >= 40:
        return COLORS["neon_orange"]
    elif score >= 20:
        return COLORS["red"]
    else:
        return COLORS["hot_magenta"]


def setup_fonts() -> None:
    """Configure fonts for the application."""
    # Dear PyGui uses default fonts; for a premium look we'd need custom font files.
    # Here we configure the default font with appropriate sizes.
    with dpg.font_registry():
        # Default font - larger and more readable
        default_font = dpg.add_font("ProggyClean.ttf", 15)
        dpg.bind_font(default_font)

        # Heading font (larger)
        heading_font = dpg.add_font("ProggyClean.ttf", 22)

        # Monospace font for logs/metrics
        mono_font = dpg.add_font("ProggyClean.ttf", 13)

    return default_font, heading_font, mono_font


THEMES = {}

def initialize_themes() -> dict:
    """Initialize and cache all themes."""
    global THEMES
    THEMES = {
        "global": create_global_theme(),
        "neon_button_cyan": create_neon_button_theme("electric_cyan"),
        "neon_button_magenta": create_neon_button_theme("hot_magenta"),
        "neon_button_green": create_neon_button_theme("acid_green"),
        "neon_button_purple": create_neon_button_theme("neon_purple"),
        "glow_button_cyan": create_glow_button_theme("electric_cyan"),
        "glow_button_magenta": create_glow_button_theme("hot_magenta"),
        "glass_panel": create_glass_panel_theme(),
        "danger_button": create_danger_button_theme(),
    }
    return THEMES


def get_theme(name: str) -> int:
    """Get a cached theme by name."""
    return THEMES.get(name, THEMES.get("global"))
