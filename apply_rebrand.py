#!/usr/bin/env python3
"""
apply_rebrand.py - Autonomous Rebranding & Media Asset Generation Engine
Transforms NuvioMobile into AuraMobile across KMP, Compose, Android, and iOS layers.
Requires zero external dependencies (uses standard Python 3 libraries).
"""

import os
import sys
import re
import math
import struct
import zlib
import shutil
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent

# ==============================================================================
# PHASE 2: PURE PYTHON PNG RASTERIZER & ASSET GENERATION ENGINE
# ==============================================================================

def create_png_rgba(width, height, pixel_func):
    """
    Renders an RGBA image of size (width, height) using pixel_func(x, y) -> (r, g, b, a)
    and encodes it into standard PNG format using pure Python (zlib + struct).
    """
    raw_rows = []
    for y in range(height):
        row = bytearray([0])  # Filter type 0 (None)
        for x in range(width):
            r, g, b, a = pixel_func(x, y, width, height)
            r = max(0, min(255, int(r)))
            g = max(0, min(255, int(g)))
            b = max(0, min(255, int(b)))
            a = max(0, min(255, int(a)))
            row.extend((r, g, b, a))
        raw_rows.append(bytes(row))

    raw_data = b"".join(raw_rows)
    compressed = zlib.compress(raw_data, level=9)

    png = bytearray(b"\x89PNG\r\n\x1a\n")

    # IHDR chunk
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    ihdr_crc = zlib.crc32(b"IHDR" + ihdr_data)
    png.extend(struct.pack(">I", len(ihdr_data)) + b"IHDR" + ihdr_data + struct.pack(">I", ihdr_crc))

    # IDAT chunk
    idat_crc = zlib.crc32(b"IDAT" + compressed)
    png.extend(struct.pack(">I", len(compressed)) + b"IDAT" + compressed + struct.pack(">I", idat_crc))

    # IEND chunk
    iend_crc = zlib.crc32(b"IEND")
    png.extend(struct.pack(">I", 0) + b"IEND" + struct.pack(">I", iend_crc))

    return bytes(png)


def aura_logo_pixel(x, y, w, h, bg_color=(13, 13, 18, 255), halo_color=(0, 255, 255), play_color=(180, 100, 255)):
    """
    Mathematical SDF shader for Aura Media Player Logo:
    - Glowing neon halo ring (Cyan #00FFFF -> Violet #8A2BE2)
    - Stylized Play Glyph at center
    """
    nx = (x - w / 2.0) / (w / 2.0)
    ny = (y - h / 2.0) / (h / 2.0)
    dist = math.hypot(nx, ny)

    r_out, g_out, b_out, a_out = bg_color

    # 1. Halo Ring: radius ~ 0.70
    ring_radius = 0.70
    ring_dist = abs(dist - ring_radius)
    halo_intensity = math.exp(-pow(ring_dist / 0.09, 2))

    angle = math.atan2(ny, nx)
    t = (math.sin(angle * 2) + 1.0) / 2.0
    hr = (1.0 - t) * 0 + t * 138
    hg = (1.0 - t) * 255 + t * 43
    hb = (1.0 - t) * 255 + t * 226

    if halo_intensity > 0.01:
        alpha = halo_intensity * 0.95
        r_out = r_out * (1.0 - alpha) + hr * alpha
        g_out = g_out * (1.0 - alpha) + hg * alpha
        b_out = b_out * (1.0 - alpha) + hb * alpha

    # 2. Stylized Play Triangle SDF
    tx = nx + 0.06
    ty = ny
    if -0.22 <= tx <= 0.30:
        max_y = (0.30 - tx) * 0.577
        if -max_y <= ty <= max_y:
            edge_dist = min(tx - (-0.22), max_y - abs(ty))
            tri_alpha = min(1.0, edge_dist * 20.0)
            
            pt = (tx + 0.22) / 0.52
            pr = (1.0 - pt) * 160 + pt * 255
            pg = (1.0 - pt) * 230 + pt * 255
            pb = 255
            
            r_out = r_out * (1.0 - tri_alpha) + pr * tri_alpha
            g_out = g_out * (1.0 - tri_alpha) + pg * tri_alpha
            b_out = b_out * (1.0 - tri_alpha) + pb * tri_alpha

    return (r_out, g_out, b_out, a_out)


def aura_foreground_pixel(x, y, w, h):
    return aura_logo_pixel(x, y, w, h, bg_color=(0, 0, 0, 0))


COLORWAYS = {
    "original": {
        "halo_start": "#00FFFF", "halo_mid": "#8A2BE2", "halo_end": "#00E5FF",
        "bg_rgb": (13, 13, 18, 255), "halo_rgb_start": (0, 255, 255), "halo_rgb_end": (138, 43, 226),
        "play_rgb": (255, 255, 255), "ios_folder": "AppIcon"
    },
    "arctic_blue": {
        "halo_start": "#00E5FF", "halo_mid": "#00B0FF", "halo_end": "#80D8FF",
        "bg_rgb": (8, 18, 28, 255), "halo_rgb_start": (0, 229, 255), "halo_rgb_end": (0, 176, 255),
        "play_rgb": (224, 247, 250), "ios_folder": "AppIconArcticBlue"
    },
    "emerald": {
        "halo_start": "#00E676", "halo_mid": "#00C853", "halo_end": "#69F0AE",
        "bg_rgb": (6, 24, 14, 255), "halo_rgb_start": (0, 230, 118), "halo_rgb_end": (0, 200, 83),
        "play_rgb": (232, 245, 233), "ios_folder": "AppIconEmerald"
    },
    "rose_gold": {
        "halo_start": "#FF4081", "halo_mid": "#F50057", "halo_end": "#FF80AB",
        "bg_rgb": (28, 10, 18, 255), "halo_rgb_start": (255, 64, 129), "halo_rgb_end": (245, 0, 87),
        "play_rgb": (252, 228, 236), "ios_folder": "AppIconRoseGold"
    },
    "copper": {
        "halo_start": "#FF6D00", "halo_mid": "#FF9100", "halo_end": "#FFD180",
        "bg_rgb": (28, 16, 8, 255), "halo_rgb_start": (255, 109, 0), "halo_rgb_end": (255, 145, 0),
        "play_rgb": (255, 243, 224), "ios_folder": "AppIconCopper"
    },
    "graphite": {
        "halo_start": "#CFD8DC", "halo_mid": "#90A4AE", "halo_end": "#ECEFF1",
        "bg_rgb": (18, 20, 22, 255), "halo_rgb_start": (207, 216, 220), "halo_rgb_end": (144, 164, 174),
        "play_rgb": (236, 239, 241), "ios_folder": "AppIconGraphite"
    },
    "gold": {
        "halo_start": "#FFD700", "halo_mid": "#FFA000", "halo_end": "#FFE082",
        "bg_rgb": (26, 20, 6, 255), "halo_rgb_start": (255, 215, 0), "halo_rgb_end": (255, 160, 0),
        "play_rgb": (255, 248, 225), "ios_folder": "AppIconGold"
    }
}


def make_colorway_pixel_func(cw_config, transparent_bg=False):
    bg_color = (0, 0, 0, 0) if transparent_bg else cw_config["bg_rgb"]
    h_start = cw_config["halo_rgb_start"]
    h_end = cw_config["halo_rgb_end"]
    p_color = cw_config["play_rgb"]

    def pixel_func(x, y, w, h):
        nx = (x - w / 2.0) / (w / 2.0)
        ny = (y - h / 2.0) / (h / 2.0)
        dist = math.hypot(nx, ny)

        r_out, g_out, b_out, a_out = bg_color

        # Halo Ring
        ring_radius = 0.70
        ring_dist = abs(dist - ring_radius)
        halo_intensity = math.exp(-pow(ring_dist / 0.09, 2))

        angle = math.atan2(ny, nx)
        t = (math.sin(angle * 2) + 1.0) / 2.0
        hr = (1.0 - t) * h_start[0] + t * h_end[0]
        hg = (1.0 - t) * h_start[1] + t * h_end[1]
        hb = (1.0 - t) * h_start[2] + t * h_end[2]

        if halo_intensity > 0.01:
            alpha = halo_intensity * 0.95
            r_out = r_out * (1.0 - alpha) + hr * alpha
            g_out = g_out * (1.0 - alpha) + hg * alpha
            b_out = b_out * (1.0 - alpha) + hb * alpha
            if transparent_bg:
                a_out = max(a_out, int(alpha * 255))

        # Play Triangle SDF
        tx = nx + 0.06
        ty = ny
        if -0.22 <= tx <= 0.30:
            max_y = (0.30 - tx) * 0.577
            if -max_y <= ty <= max_y:
                edge_dist = min(tx - (-0.22), max_y - abs(ty))
                tri_alpha = min(1.0, edge_dist * 20.0)

                r_out = r_out * (1.0 - tri_alpha) + p_color[0] * tri_alpha
                g_out = g_out * (1.0 - tri_alpha) + p_color[1] * tri_alpha
                b_out = b_out * (1.0 - tri_alpha) + p_color[2] * tri_alpha
                if transparent_bg:
                    a_out = max(a_out, int(tri_alpha * 255))

        return (r_out, g_out, b_out, a_out)

    return pixel_func


def generate_colorway_splash_xml(cw_key, cw_config):
    return f"""<vector xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:aapt="http://schemas.android.com/aapt"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:pathData="M54,12 A42,42 0 1,0 54,96 A42,42 0 1,0 54,12 Z"
        android:strokeWidth="6"
        android:strokeLineCap="round">
        <aapt:attr name="android:strokeColor">
            <gradient
                android:startX="12"
                android:startY="12"
                android:endX="96"
                android:endY="96"
                android:type="linear">
                <item android:offset="0.0" android:color="{cw_config['halo_start']}" />
                <item android:offset="0.5" android:color="{cw_config['halo_mid']}" />
                <item android:offset="1.0" android:color="{cw_config['halo_end']}" />
            </gradient>
        </aapt:attr>
    </path>
    <path
        android:pathData="M44,36 L72,54 L44,72 Z">
        <aapt:attr name="android:fillColor">
            <gradient
                android:startX="44"
                android:startY="36"
                android:endX="72"
                android:endY="72"
                android:type="linear">
                <item android:offset="0.0" android:color="{cw_config['halo_start']}" />
                <item android:offset="1.0" android:color="#FFFFFFFF" />
            </gradient>
        </aapt:attr>
    </path>
</vector>
"""


def generate_all_assets():
    rebrand_dir = WORKSPACE / "rebrand_assets"
    
    dirs = [
        rebrand_dir / "composeApp/src/commonMain/composeResources/drawable",
        rebrand_dir / "androidApp/src/main/res/mipmap-mdpi",
        rebrand_dir / "androidApp/src/main/res/mipmap-hdpi",
        rebrand_dir / "androidApp/src/main/res/mipmap-xhdpi",
        rebrand_dir / "androidApp/src/main/res/mipmap-xxhdpi",
        rebrand_dir / "androidApp/src/main/res/mipmap-xxxhdpi",
        rebrand_dir / "composeApp/src/androidMain/res/mipmap-mdpi",
        rebrand_dir / "composeApp/src/androidMain/res/mipmap-hdpi",
        rebrand_dir / "composeApp/src/androidMain/res/mipmap-xhdpi",
        rebrand_dir / "composeApp/src/androidMain/res/mipmap-xxhdpi",
        rebrand_dir / "composeApp/src/androidMain/res/mipmap-xxxhdpi",
        rebrand_dir / "composeApp/src/androidMain/res/drawable",
        rebrand_dir / "iosApp/iosApp/Assets.xcassets/AppIcon.appiconset",
        rebrand_dir / "iosApp/iosApp/Assets.xcassets/LaunchImage.imageset",
    ]
    for cw_key, cw in COLORWAYS.items():
        if cw["ios_folder"] != "AppIcon":
            dirs.append(rebrand_dir / f"iosApp/iosApp/Assets.xcassets/{cw['ios_folder']}.appiconset")

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    print(f"[ASSETS] Created directory architecture in {rebrand_dir}")

    # Vector Drawables (XML) for all colorways
    android_drawable_dir = rebrand_dir / "composeApp/src/androidMain/res/drawable"
    compose_drawable_dir = rebrand_dir / "composeApp/src/commonMain/composeResources/drawable"

    for cw_key, cw in COLORWAYS.items():
        splash_xml = generate_colorway_splash_xml(cw_key, cw)
        if cw_key == "original":
            (android_drawable_dir / "ic_splash_logo.xml").write_text(splash_xml, encoding="utf-8")
            (android_drawable_dir / "splash_logo.xml").write_text(splash_xml, encoding="utf-8")
            (android_drawable_dir / "logo.xml").write_text(splash_xml, encoding="utf-8")
            (compose_drawable_dir / "logo.xml").write_text(splash_xml, encoding="utf-8")
            (compose_drawable_dir / "splash_logo.xml").write_text(splash_xml, encoding="utf-8")
        else:
            (android_drawable_dir / f"ic_splash_logo_{cw_key}.xml").write_text(splash_xml, encoding="utf-8")

    # Master and adaptive vector icons
    ic_launcher_xml = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/aura_background"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
    <monochrome android:drawable="@drawable/ic_launcher_monochrome"/>
</adaptive-icon>
"""
    ic_launcher_round_xml = ic_launcher_xml
    (android_drawable_dir / "ic_launcher.xml").write_text(ic_launcher_xml, encoding="utf-8")
    (android_drawable_dir / "ic_launcher_round.xml").write_text(ic_launcher_round_xml, encoding="utf-8")
    (compose_drawable_dir / "ic_launcher.xml").write_text(ic_launcher_xml, encoding="utf-8")
    (compose_drawable_dir / "ic_launcher_round.xml").write_text(ic_launcher_round_xml, encoding="utf-8")

    # Generate Colorway PNG slices for Android Mipmaps
    mipmap_sizes = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }

    for folder_name, size in mipmap_sizes.items():
        print(f"[ASSETS] Generating {folder_name} ({size}x{size}) across all colorways...")
        for cw_key, cw in COLORWAYS.items():
            icon_func = make_colorway_pixel_func(cw, transparent_bg=False)
            fg_func = make_colorway_pixel_func(cw, transparent_bg=True)

            icon_png = create_png_rgba(size, size, icon_func)
            fg_png = create_png_rgba(size, size, fg_func)

            for base_dest in [rebrand_dir / "androidApp/src/main/res", rebrand_dir / "composeApp/src/androidMain/res"]:
                dest_dir = base_dest / folder_name
                if cw_key == "original":
                    (dest_dir / "ic_launcher.png").write_bytes(icon_png)
                    (dest_dir / "ic_launcher_round.png").write_bytes(icon_png)
                    (dest_dir / "ic_launcher_foreground.png").write_bytes(fg_png)
                else:
                    (dest_dir / f"ic_launcher_{cw_key}.png").write_bytes(icon_png)
                    (dest_dir / f"ic_launcher_{cw_key}_foreground.png").write_bytes(fg_png)

    # Generate App Icons & Wordmarks for Compose Resources
    for cw_key, cw in COLORWAYS.items():
        icon_func = make_colorway_pixel_func(cw, transparent_bg=False)
        icon_512 = create_png_rgba(512, 512, icon_func)
        (compose_drawable_dir / f"app_icon_{cw_key}.png").write_bytes(icon_512)
        (compose_drawable_dir / f"app_logo_wordmark_{cw_key}.png").write_bytes(icon_512)
        if cw_key == "original":
            (compose_drawable_dir / "app_logo_wordmark.png").write_bytes(icon_512)

    # iOS Asset Catalogs across all colorways
    ios_contents_json = """{
  "images" : [
    {
      "filename" : "app-icon-1024.png",
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
"""
    for cw_key, cw in COLORWAYS.items():
        if "ios_folder" in cw:
            ios_icon_dir = rebrand_dir / f"iosApp/iosApp/Assets.xcassets/{cw['ios_folder']}.appiconset"
            ios_icon_dir.mkdir(parents=True, exist_ok=True)
            icon_func = make_colorway_pixel_func(cw, transparent_bg=False)
            ios_1024 = create_png_rgba(1024, 1024, icon_func)
            (ios_icon_dir / "app-icon-1024.png").write_bytes(ios_1024)
            (ios_icon_dir / "Contents.json").write_text(ios_contents_json, encoding="utf-8")

    # Clean up any legacy .webp icon files to prevent duplicate resource conflicts
    for base_dest in [WORKSPACE / "androidApp/src/main/res", WORKSPACE / "composeApp/src/androidMain/res"]:
        if base_dest.exists():
            for webp_file in base_dest.glob("**/*.webp"):
                if "ic_launcher" in webp_file.name or "ic_splash" in webp_file.name:
                    webp_file.unlink()

    print("[ASSETS] Completed all colorway assets and icon matrices successfully.")


# ==============================================================================
# PHASE 3: COMPREHENSIVE REBRANDING ENGINE
# ==============================================================================

EXCLUDE_DIRS = {
    ".git", ".gradle", ".idea", "build", "androidApp/build",
    "composeApp/build", "iosApp/build", "vendor", ".symlinks",
    "rebrand_assets"
}

TOKEN_REPLACEMENTS = [
    ("com.nuvio.app.nativebridge", "com.aura.app.nativebridge"),
    ("com.nuvio.app", "com.aura.app"),
    ("com.nuvio.android", "com.aura.android"),
    ("com.nuviodebug.com", "com.auradebug.com"),
    ("com.nuvio.media", "com.aura.media"),
    ("nuvio.composeapp.generated.resources", "aura.composeapp.generated.resources"),
    ("nuvio.android.distribution", "aura.android.distribution"),
    ("nuvio.ios.distribution", "aura.ios.distribution"),
    ("nuvio_loading_indicator", "aura_loading_indicator"),
    ("nuvio_resume_prompt", "aura_resume_prompt"),
    ("nuvio_background", "aura_background"),
    ("nuvio_updates", "aura_updates"),
    ("nuvio_subtitles", "aura_subtitles"),
    ("nuvio_downloads", "aura_downloads"),
    ("nuvio_plugin_scrapers", "aura_plugin_scrapers"),
    ("nuvio.downloads.live_status.payload", "aura.downloads.live_status.payload"),
    ("NuvioDownloadsLiveStatusUpdated", "AuraDownloadsLiveStatusUpdated"),
    ("NuvioPlayerLockLandscape", "AuraPlayerLockLandscape"),
    ("NuvioPlayerUnlockOrientation", "AuraPlayerUnlockOrientation"),
    ("NuvioiOSPlayer", "AuraiOSPlayer"),
    ("NuvioMemberBackgrounds", "AuraMemberBackgrounds"),
    ("NuvioMemberAvatars", "AuraMemberAvatars"),
    ("NuvioMembership", "AuraMembership"),
    ("LocalNuvioThemeTokens", "LocalAuraThemeTokens"),
    ("LocalNuvioTypeScale", "LocalAuraTypeScale"),
    ("NuvioTokens", "AuraTokens"),
    ("NuvioTheme", "AuraTheme"),
    ("NuvioPlayerBridgeFactory", "AuraPlayerBridgeFactory"),
    ("NuvioPlayerBridgeCreator", "AuraPlayerBridgeCreator"),
    ("NuvioPlayerBridge", "AuraPlayerBridge"),
    ("NuvioNativeBottomSheetDelegate", "AuraNativeBottomSheetDelegate"),
    ("usesNativeNuvioBottomSheet", "usesNativeAuraBottomSheet"),
    ("NuvioNativeModalBottomSheet", "AuraNativeModalBottomSheet"),
    ("dismissNativeNuvioBottomSheet", "dismissNativeAuraBottomSheet"),
    ("nuvioPlatformExtraTopPadding", "auraPlatformExtraTopPadding"),
    ("nuvioPlatformExtraBottomPadding", "auraPlatformExtraBottomPadding"),
    ("nuvioBottomNavigationExtraVerticalPadding", "auraBottomNavigationExtraVerticalPadding"),
    ("nuvioBottomNavigationBarInsets", "auraBottomNavigationBarInsets"),
    ("nuvioBackgroundColor", "auraBackgroundColor"),
    ("nuvioComposeViewController", "auraComposeViewController"),
    ("NuvioAppIconCompletion", "AuraAppIconCompletion"),
    ("NuvioSupportsAlternateAppIcons", "AuraSupportsAlternateAppIcons"),
    ("NuvioIsCurrentAlternateAppIcon", "AuraIsCurrentAlternateAppIcon"),
    ("NuvioSetAlternateAppIconName", "AuraSetAlternateAppIconName"),
    ("NuvioNavigator", "AuraNavigator"),
    ("NuvioTabHome", "AuraTabHome"),
    ("NuvioTabSearch", "AuraTabSearch"),
    ("NuvioTabLibrary", "AuraTabLibrary"),
    ("NuvioTabProfile", "AuraTabProfile"),
    ("NuvioMobile", "AuraMobile"),
    ("Nuvio Mobile", "Aura Mobile"),
    ("Theme.Nuvio", "Theme.Aura"),
    ("NUVIO_", "AURA_"),
    ("nuvio://", "aura://"),
    ("rootProject.name = \"Nuvio\"", "rootProject.name = \"Aura\""),
    ("PRODUCT_NAME = Nuvio", "PRODUCT_NAME = Aura"),
    ("PRODUCT_NAME=Nuvio", "PRODUCT_NAME=Aura"),
    ("Nuvio.app", "Aura.app"),
]

TEXT_EXTENSIONS = {
    ".kt", ".kts", ".java", ".xml", ".properties", ".json", ".swift",
    ".h", ".m", ".c", ".def", ".xcconfig", ".plist", ".pbxproj",
    ".txt", ".md", ".toml", ".gradle", ".pro", ".sh"
}


def should_skip_dir(dirpath):
    try:
        parts = Path(dirpath).relative_to(WORKSPACE).parts
    except ValueError:
        return False
    for p in parts:
        if p in EXCLUDE_DIRS:
            return True
    return False


def deep_textual_sweep():
    total_files_scanned = 0
    total_files_updated = 0

    for root, dirs, files in os.walk(WORKSPACE):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not should_skip_dir(os.path.join(root, d))]

        for f in files:
            file_path = Path(root) / f
            ext = file_path.suffix.lower()

            if ext not in TEXT_EXTENSIONS and not f.endswith("xcconfig"):
                continue

            total_files_scanned += 1
            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception:
                continue

            new_content = content
            for src, dst in TOKEN_REPLACEMENTS:
                new_content = new_content.replace(src, dst)

            # String resource brand replacements
            new_content = re.sub(r'(<string\s+name="app_name"[^>]*>)Nuvio(</string>)', r'\1Aura\2', new_content)
            new_content = re.sub(r'(<string\s+name="app_brand_name"[^>]*>)Nuvio(</string>)', r'\1Aura\2', new_content)
            new_content = re.sub(r'\bNuvio\b', 'Aura', new_content)

            if new_content != content:
                file_path.write_text(new_content, encoding="utf-8")
                total_files_updated += 1

    print(f"[REBRAND] Scanned {total_files_scanned} files; Updated {total_files_updated} text files.")
    return total_files_scanned, total_files_updated


def merge_and_move_tree(src: Path, dst: Path):
    """
    Recursively moves files and directories from src into dst,
    merging directories and overwriting existing files.
    """
    if not dst.exists():
        shutil.move(str(src), str(dst))
        return

    for item in list(src.iterdir()):
        target = dst / item.name
        if item.is_dir():
            if target.exists():
                merge_and_move_tree(item, target)
            else:
                shutil.move(str(item), str(target))
        else:
            if target.exists():
                target.unlink()
            shutil.move(str(item), str(target))

    if src.exists():
        try:
            src.rmdir()
        except OSError:
            pass


def refactor_directories_and_files():
    refactored_dirs = []

    # 1. Dynamic file renames for files containing 'Nuvio' or 'nuvio_'
    for root, dirs, files in os.walk(WORKSPACE):
        if should_skip_dir(root):
            continue
        for f in files:
            new_f = f
            if new_f.startswith("Nuvio"):
                new_f = "Aura" + new_f[len("Nuvio"):]
            elif new_f.startswith("nuvio_"):
                new_f = "aura_" + new_f[len("nuvio_"):]
            
            if new_f != f:
                old_path = Path(root) / f
                new_path = Path(root) / new_f
                print(f"[RENAME] {old_path.relative_to(WORKSPACE)} -> {new_f}")
                if new_path.exists():
                    new_path.unlink()
                shutil.move(str(old_path), str(new_path))

    # 2. Dynamic directory renames (e.g., NuvioTab*.imageset)
    for root, dirs, _ in os.walk(WORKSPACE, topdown=False):
        if should_skip_dir(root):
            continue
        for d in dirs:
            if d.startswith("NuvioTab") and d.endswith(".imageset"):
                old_dir = Path(root) / d
                new_dir = Path(root) / ("AuraTab" + d[len("NuvioTab"):])
                print(f"[RENAME DIR] {old_dir.relative_to(WORKSPACE)} -> {new_dir.name}")
                if new_dir.exists():
                    shutil.rmtree(new_dir)
                shutil.move(str(old_dir), str(new_dir))

    # 3. Package Directory Refactoring: com/nuvio -> com/aura across all source sets
    for root, dirs, _ in os.walk(WORKSPACE, topdown=False):
        if should_skip_dir(root):
            continue
        for d in dirs:
            if d == "nuvio":
                parent_path = Path(root)
                if parent_path.name == "com":
                    nuvio_dir = parent_path / "nuvio"
                    aura_dir = parent_path / "aura"
                    print(f"[REFACTOR] Moving and merging {nuvio_dir} -> {aura_dir}")
                    merge_and_move_tree(nuvio_dir, aura_dir)
                    refactored_dirs.append(str(aura_dir.relative_to(WORKSPACE)))

    print(f"[REFACTOR] Completed on-disk directory refactoring: {len(refactored_dirs)} package roots merged.")
    return refactored_dirs


def inject_aura_assets():
    rebrand_dir = WORKSPACE / "rebrand_assets"
    if not rebrand_dir.exists():
        print("[ERROR] rebrand_assets directory does not exist.")
        return

    injected_count = 0
    for root, _, files in os.walk(rebrand_dir):
        for f in files:
            src_file = Path(root) / f
            rel_path = src_file.relative_to(rebrand_dir)
            dst_file = WORKSPACE / rel_path

            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)
            injected_count += 1

    print(f"[INJECT] Successfully injected {injected_count} Aura brand assets into workspace.")


# ==============================================================================
# MAIN EXECUTION ROUTINE
# ==============================================================================

def main():
    print("====================================================================")
    print("      AURAMOBILE AUTOMATED REBRANDING & ASSET PIPELINE")
    print("====================================================================")

    # 1. Asset Generation
    print("\n--- [1/4] Generating Media Player & Mobile Brand Assets ---")
    generate_all_assets()

    # 2. Textual Replacement
    print("\n--- [2/4] Executing Deep Textual Sweep ---")
    scanned, updated = deep_textual_sweep()

    # 3. Directory Refactoring
    print("\n--- [3/4] Refactoring Package Directories & File Paths ---")
    refactored_dirs = refactor_directories_and_files()

    # 4. Asset Injection
    print("\n--- [4/4] Injecting Aura Assets into Project Tree ---")
    inject_aura_assets()

    print("\n====================================================================")
    print(" REBRANDING ENGINE COMPLETE: Workspace transformed to AuraMobile!")
    print(f" Summary: {updated} files updated, {len(refactored_dirs)} package dirs refactored.")
    print("====================================================================")


if __name__ == "__main__":
    main()
