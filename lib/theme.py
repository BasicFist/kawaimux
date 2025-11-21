#!/usr/bin/env python3
"""
🎀 Kawaii Theme System
Hello Kitty themed interface for managing visual appearance and styling
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Hello Kitty themed paths
THEME_PATHS = {
    'themes_dir': os.path.expanduser('~/.kawaii_themes'),
    'active_theme_dir': os.path.expanduser('~/.kawaii_active_theme'),
    'presets_dir': os.path.expanduser('~/.kawaii_theme_presets'),
    'custom_dir': os.path.expanduser('~/.kawaii_custom_themes')
}

# Official Hello Kitty color palette
HELLO_KITTY_COLORS = {
    'rogue_pink': '#F5A3C8',        # Primary pink
    'fluorescent_pink': '#ED0D92',   # Bright pink
    'spanish_crimson': '#ED164F',    # Secondary pink
    'vivid_yellow': '#FFE717',       # Yellow accent
    'eerie_black': '#1E181A',        # Dark background
    'aragonite_white': '#F2F1F2',    # Light foreground
    'wild_honey': '#E9CA01',         # Success yellow
    'hello_kitty_heart': '#B01455',  # Deep pink
    'pastel_blue': '#095D9A',        # Information blue
    'soft_pink': '#F88FB0',          # Gentle pink
    'satin_pillows': '#F2C8D6',      # Soft background
    'khaliki': '#FCFDFF'             # Clean white
}


class ThemeType(Enum):
    """Types of themes"""
    HELLO_KITTY = "hello_kitty"
    PASTEL = "pastel"
    STARRY = "starry"
    RAINBOW = "rainbow"
    MINIMAL = "minimal"
    NEON = "neon"
    CUSTOM = "custom"


class ColorMode(Enum):
    """Color modes"""
    DARK = "dark"
    LIGHT = "light"
    AUTO = "auto"


@dataclass
class KawaiiColor:
    """Individual color definition"""
    name: str
    hex_value: str
    rgb: Tuple[int, int, int]
    hsl: Tuple[float, float, float]
    description: str
    usage: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class KawaiiTheme:
    """Complete theme definition"""
    id: str
    name: str
    description: str
    theme_type: ThemeType
    color_mode: ColorMode
    version: str
    author: str
    created_at: datetime
    updated_at: datetime
    
    # Color scheme
    primary_color: str
    secondary_color: str
    accent_color: str
    background_color: str
    foreground_color: str
    success_color: str
    warning_color: str
    error_color: str
    info_color: str
    
    # Visual elements
    border_style: str
    font_family: str
    font_size: int
    icon_style: str
    
    # Kawaii elements
    kawaii_level: str
    hello_kitty_elements: bool
    emoji_style: str
    animation_level: str
    
    # Metadata
    rating: float
    downloads: int
    tags: List[str]
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        data['theme_type'] = self.theme_type.value
        data['color_mode'] = self.color_mode.value
        return data


class KawaiiThemeManager:
    """Hello Kitty theme management system"""
    
    def __init__(self):
        self.themes: Dict[str, KawaiiTheme] = {}
        self.active_theme_id: Optional[str] = None
        
        # Initialize directories
        self._initialize_directories()
        
        # Load themes
        self._load_themes()
        
        # Initialize default themes
        self._initialize_default_themes()
    
    def _initialize_directories(self):
        """Create theme directory structure"""
        for path in THEME_PATHS.values():
            Path(path).mkdir(parents=True, exist_ok=True)
    
    def _load_themes(self):
        """Load themes from disk"""
        themes_file = os.path.join(THEME_PATHS['themes_dir'], 'themes.json')
        
        if os.path.exists(themes_file):
            try:
                with open(themes_file, 'r') as f:
                    data = json.load(f)
                
                for theme_id, theme_data in data.items():
                    try:
                        theme = self._dict_to_theme(theme_data)
                        self.themes[theme_id] = theme
                    except Exception as e:
                        print(f"⚠️ Error loading theme {theme_id}: {e}")
                
                # Load active theme
                active_file = os.path.join(THEME_PATHS['themes_dir'], 'active_theme.json')
                if os.path.exists(active_file):
                    with open(active_file, 'r') as f:
                        active_data = json.load(f)
                        self.active_theme_id = active_data.get('active_theme_id')
                        
            except Exception as e:
                print(f"❌ Error loading themes: {e}")
    
    def _save_themes(self):
        """Save themes to disk"""
        themes_file = os.path.join(THEME_PATHS['themes_dir'], 'themes.json')
        
        try:
            data = {theme_id: theme.to_dict() for theme_id, theme in self.themes.items()}
            
            with open(themes_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Save active theme
            active_file = os.path.join(THEME_PATHS['themes_dir'], 'active_theme.json')
            with open(active_file, 'w') as f:
                json.dump({'active_theme_id': self.active_theme_id}, f)
                
        except Exception as e:
            print(f"❌ Error saving themes: {e}")
    
    def _dict_to_theme(self, data: Dict) -> KawaiiTheme:
        """Convert dictionary to KawaiiTheme"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        data['theme_type'] = ThemeType(data['theme_type'])
        data['color_mode'] = ColorMode(data['color_mode'])
        return KawaiiTheme(**data)
    
    def _initialize_default_themes(self):
        """Initialize default Hello Kitty themes"""
        if self.themes:
            return  # Already initialized
        
        # Classic Hello Kitty Theme
        classic_theme = KawaiiTheme(
            id="classic_hello_kitty",
            name="🌸 Classic Hello Kitty",
            description="The timeless Hello Kitty experience with rogue pink perfection and elegant white accents.",
            theme_type=ThemeType.HELLO_KITTY,
            color_mode=ColorMode.DARK,
            version="1.0.0",
            author="Kawaii Design Team",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            primary_color=HELLO_KITTY_COLORS['rogue_pink'],
            secondary_color=HELLO_KITTY_COLORS['fluorescent_pink'],
            accent_color=HELLO_KITTY_COLORS['vivid_yellow'],
            background_color=HELLO_KITTY_COLORS['eerie_black'],
            foreground_color=HELLO_KITTY_COLORS['aragonite_white'],
            success_color=HELLO_KITTY_COLORS['wild_honey'],
            warning_color=HELLO_KITTY_COLORS['vivid_yellow'],
            error_color=HELLO_KITTY_COLORS['spanish_crimson'],
            info_color=HELLO_KITTY_COLORS['pastel_blue'],
            border_style="rounded",
            font_family="Monaco, Consolas, monospace",
            font_size=12,
            icon_style="hello_kitty",
            kawaii_level="MAXIMUM",
            hello_kitty_elements=True,
            emoji_style="kawaii",
            animation_level="subtle",
            rating=5.0,
            downloads=0,
            tags=["classic", "hello_kitty", "elegant", "timeless"]
        )
        
        # Pastel Dreams Theme
        pastel_theme = KawaiiTheme(
            id="pastel_dreams",
            name="💜 Pastel Dreams",
            description="Soft and dreamy colors that create a gentle, soothing kawaii atmosphere.",
            theme_type=ThemeType.PASTEL,
            color_mode=ColorMode.DARK,
            version="1.0.0",
            author="Kawaii Dream Team",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            primary_color=HELLO_KITTY_COLORS['soft_pink'],
            secondary_color=HELLO_KITTY_COLORS['satin_pillows'],
            accent_color=HELLO_KITTY_COLORS['pastel_blue'],
            background_color=HELLO_KITTY_COLORS['eerie_black'],
            foreground_color=HELLO_KITTY_COLORS['aragonite_white'],
            success_color=HELLO_KITTY_COLORS['wild_honey'],
            warning_color=HELLO_KITTY_COLORS['vivid_yellow'],
            error_color=HELLO_KITTY_COLORS['hello_kitty_heart'],
            info_color=HELLO_KITTY_COLORS['pastel_blue'],
            border_style="soft",
            font_family="SF Mono, Monaco, Consolas, monospace",
            font_size=13,
            icon_style="soft",
            kawaii_level="MAXIMUM",
            hello_kitty_elements=True,
            emoji_style="soft",
            animation_level="gentle",
            rating=4.8,
            downloads=0,
            tags=["pastel", "soft", "dreamy", "gentle"]
        )
        
        # Starry Night Theme
        starry_theme = KawaiiTheme(
            id="starry_night",
            name="⭐ Starry Night",
            description="Cosmic kawaii with sparkling stars and deep space beauty.",
            theme_type=ThemeType.STARRY,
            color_mode=ColorMode.DARK,
            version="1.0.0",
            author="Kawaii Cosmic Team",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            primary_color=HELLO_KITTY_COLORS['spanish_crimson'],
            secondary_color=HELLO_KITTY_COLORS['vivid_yellow'],
            accent_color=HELLO_KITTY_COLORS['vivid_yellow'],
            background_color=HELLO_KITTY_COLORS['eerie_black'],
            foreground_color=HELLO_KITTY_COLORS['khaliki'],
            success_color=HELLO_KITTY_COLORS['wild_honey'],
            warning_color=HELLO_KITTY_COLORS['vivid_yellow'],
            error_color=HELLO_KITTY_COLORS['spanish_crimson'],
            info_color=HELLO_KITTY_COLORS['pastel_blue'],
            border_style="cosmic",
            font_family="JetBrains Mono, Fira Code, monospace",
            font_size=12,
            icon_style="cosmic",
            kawaii_level="MAXIMUM",
            hello_kitty_elements=True,
            emoji_style="stars",
            animation_level="sparkly",
            rating=4.9,
            downloads=0,
            tags=["cosmic", "stars", "space", "sparkly"]
        )
        
        # Rainbow Kitty Theme
        rainbow_theme = KawaiiTheme(
            id="rainbow_kitty",
            name="🌈 Rainbow Kitty",
            description="All the colors of kawaii! A vibrant celebration of rainbow aesthetics.",
            theme_type=ThemeType.RAINBOW,
            color_mode=ColorMode.DARK,
            version="1.0.0",
            author="Kawaii Rainbow Team",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            primary_color=HELLO_KITTY_COLORS['rogue_pink'],
            secondary_color=HELLO_KITTY_COLORS['fluorescent_pink'],
            accent_color=HELLO_KITTY_COLORS['vivid_yellow'],
            background_color=HELLO_KITTY_COLORS['eerie_black'],
            foreground_color=HELLO_KITTY_COLORS['khaliki'],
            success_color=HELLO_KITTY_COLORS['wild_honey'],
            warning_color=HELLO_KITTY_COLORS['vivid_yellow'],
            error_color=HELLO_KITTY_COLORS['spanish_crimson'],
            info_color=HELLO_KITTY_COLORS['pastel_blue'],
            border_style="rainbow",
            font_family="Fira Code, JetBrains Mono, monospace",
            font_size=12,
            icon_style="rainbow",
            kawaii_level="MAXIMUM",
            hello_kitty_elements=True,
            emoji_style="rainbow",
            animation_level="colorful",
            rating=4.7,
            downloads=0,
            tags=["rainbow", "colorful", "vibrant", "celebration"]
        )
        
        # Minimal Pink Theme
        minimal_theme = KawaiiTheme(
            id="minimal_pink",
            name="🎀 Minimal Pink",
            description="Clean and simple styling with just the right amount of kawaii pink.",
            theme_type=ThemeType.MINIMAL,
            color_mode=ColorMode.LIGHT,
            version="1.0.0",
            author="Kawaii Minimal Team",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            primary_color=HELLO_KITTY_COLORS['rogue_pink'],
            secondary_color=HELLO_KITTY_COLORS['soft_pink'],
            accent_color=HELLO_KITTY_COLORS['pastel_blue'],
            background_color=HELLO_KITTY_COLORS['khaliki'],
            foreground_color=HELLO_KITTY_COLORS['eerie_black'],
            success_color=HELLO_KITTY_COLORS['wild_honey'],
            warning_color=HELLO_KITTY_COLORS['vivid_yellow'],
            error_color=HELLO_KITTY_COLORS['spanish_crimson'],
            info_color=HELLO_KITTY_COLORS['pastel_blue'],
            border_style="clean",
            font_family="SF Pro Text, Helvetica, Arial, sans-serif",
            font_size=13,
            icon_style="minimal",
            kawaii_level="MAXIMUM",
            hello_kitty_elements=True,
            emoji_style="minimal",
            animation_level="minimal",
            rating=4.6,
            downloads=0,
            tags=["minimal", "clean", "simple", "elegant"]
        )
        
        # Neon Glow Theme
        neon_theme = KawaiiTheme(
            id="neon_glow",
            name="💫 Neon Glow",
            description="Futuristic kawaii vibes with electric neon colors and glowing effects.",
            theme_type=ThemeType.NEON,
            color_mode=ColorMode.DARK,
            version="1.0.0",
            author="Kawaii Neon Team",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            primary_color=HELLO_KITTY_COLORS['fluorescent_pink'],
            secondary_color=HELLO_KITTY_COLORS['vivid_yellow'],
            accent_color=HELLO_KITTY_COLORS['vivid_yellow'],
            background_color=HELLO_KITTY_COLORS['eerie_black'],
            foreground_color=HELLO_KITTY_COLORS['khaliki'],
            success_color=HELLO_KITTY_COLORS['wild_honey'],
            warning_color=HELLO_KITTY_COLORS['vivid_yellow'],
            error_color=HELLO_KITTY_COLORS['spanish_crimson'],
            info_color=HELLO_KITTY_COLORS['pastel_blue'],
            border_style="neon",
            font_family="Space Mono, Consolas, monospace",
            font_size=12,
            icon_style="neon",
            kawaii_level="MAXIMUM",
            hello_kitty_elements=True,
            emoji_style="neon",
            animation_level="electric",
            rating=4.8,
            downloads=0,
            tags=["neon", "futuristic", "glow", "electric"]
        )
        
        # Add all themes
        for theme in [classic_theme, pastel_theme, starry_theme, rainbow_theme, minimal_theme, neon_theme]:
            self.themes[theme.id] = theme
        
        # Set classic theme as default
        self.active_theme_id = classic_theme.id
        self._save_themes()
    
    def list_themes(self, 
                   theme_type: Optional[ThemeType] = None,
                   color_mode: Optional[ColorMode] = None) -> List[KawaiiTheme]:
        """List available themes with optional filtering"""
        themes = list(self.themes.values())
        
        # Apply filters
        if theme_type:
            themes = [t for t in themes if t.theme_type == theme_type]
        
        if color_mode:
            themes = [t for t in themes if t.color_mode == color_mode]
        
        # Sort by rating and name
        themes.sort(key=lambda t: (t.rating, t.name), reverse=True)
        
        return themes
    
    def get_theme(self, theme_id: str) -> Optional[KawaiiTheme]:
        """Get theme by ID"""
        return self.themes.get(theme_id)
    
    def get_active_theme(self) -> Optional[KawaiiTheme]:
        """Get currently active theme"""
        if not self.active_theme_id:
            return None
        return self.themes.get(self.active_theme_id)
    
    def apply_theme(self, theme_id: str) -> bool:
        """Apply a theme"""
        try:
            theme = self.themes.get(theme_id)
            if not theme:
                print(f"❌ Theme '{theme_id}' not found")
                return False
            
            # Set as active theme
            self.active_theme_id = theme_id
            theme.updated_at = datetime.now()
            
            # Apply theme to system (simplified implementation)
            self._apply_theme_to_system(theme)
            
            # Save changes
            self._save_themes()
            
            print(f"🎨 Theme '{theme.name}' applied successfully! ♡")
            print(f"💖 Kawaii level: {theme.kawaii_level}")
            return True
            
        except Exception as e:
            print(f"❌ Error applying theme '{theme_id}': {e}")
            return False
    
    def _apply_theme_to_system(self, theme: KawaiiTheme):
        """Apply theme to the system (simplified implementation)"""
        # In a real implementation, this would:
        # 1. Update terminal colors
        # 2. Apply CSS themes for web interfaces
        # 3. Update TUI styling
        # 4. Save theme configuration
        # 5. Notify system of theme change
        
        # Create theme application script
        theme_script = os.path.join(THEME_PATHS['active_theme_dir'], 'apply_theme.sh')
        
        script_content = f'''#!/bin/bash
# Theme application script for {theme.name}
# Generated on {datetime.now().isoformat()}

echo "🎀 Applying {theme.name} theme..."

# Set terminal colors (simplified)
export KAWAII_THEME_NAME="{theme.name}"
export KAWAII_PRIMARY="{theme.primary_color}"
export KAWAII_SECONDARY="{theme.secondary_color}"
export KAWAII_ACCENT="{theme.accent_color}"
export KAWAII_BACKGROUND="{theme.background_color}"
export KAWAII_FOREGROUND="{theme.foreground_color}"

# Apply theme-specific configurations
{"export KAWAII_HELLO_KITTY_ELEMENTS=true" if theme.hello_kitty_elements else "export KAWAII_HELLO_KITTY_ELEMENTS=false"}
{"export KAWAII_ANIMATIONS=enabled" if theme.animation_level != "minimal" else "export KAWAII_ANIMATIONS=minimal"}

echo "✨ {theme.name} theme applied!"
echo "💖 Kawaii level: {theme.kawaii_level}"
        '''
        
        with open(theme_script, 'w') as f:
            f.write(script_content)
        
        # Make script executable
        os.chmod(theme_script, 0o755)
        
        print(f"  🎨 Theme script created: {theme_script}")
    
    def create_custom_theme(self, 
                          name: str,
                          description: str,
                          theme_type: ThemeType,
                          color_scheme: Dict[str, str],
                          author: str = "Custom") -> bool:
        """Create a custom theme"""
        try:
            theme_id = self._generate_theme_id(name)
            
            # Create custom theme
            theme = KawaiiTheme(
                id=theme_id,
                name=name,
                description=description,
                theme_type=theme_type,
                color_mode=ColorMode.DARK,  # Default
                version="1.0.0",
                author=author,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                primary_color=color_scheme.get('primary', HELLO_KITTY_COLORS['rogue_pink']),
                secondary_color=color_scheme.get('secondary', HELLO_KITTY_COLORS['fluorescent_pink']),
                accent_color=color_scheme.get('accent', HELLO_KITTY_COLORS['vivid_yellow']),
                background_color=color_scheme.get('background', HELLO_KITTY_COLORS['eerie_black']),
                foreground_color=color_scheme.get('foreground', HELLO_KITTY_COLORS['aragonite_white']),
                success_color=color_scheme.get('success', HELLO_KITTY_COLORS['wild_honey']),
                warning_color=color_scheme.get('warning', HELLO_KITTY_COLORS['vivid_yellow']),
                error_color=color_scheme.get('error', HELLO_KITTY_COLORS['spanish_crimson']),
                info_color=color_scheme.get('info', HELLO_KITTY_COLORS['pastel_blue']),
                border_style="custom",
                font_family="Monaco, Consolas, monospace",
                font_size=12,
                icon_style="custom",
                kawaii_level="CUSTOM",
                hello_kitty_elements=True,
                emoji_style="custom",
                animation_level="custom",
                rating=0.0,
                downloads=0,
                tags=["custom"]
            )
            
            self.themes[theme_id] = theme
            self._save_themes()
            
            print(f"🎨 Custom theme '{name}' created successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error creating custom theme: {e}")
            return False
    
    def _generate_theme_id(self, name: str) -> str:
        """Generate unique theme ID"""
        import re
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', name).lower()
        clean_name = re.sub(r'\s+', '_', clean_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{clean_name}_{timestamp}"
    
    def customize_theme(self, 
                       theme_id: str,
                       updates: Dict[str, Any]) -> bool:
        """Customize an existing theme"""
        try:
            theme = self.themes.get(theme_id)
            if not theme:
                print(f"❌ Theme '{theme_id}' not found")
                return False
            
            # Update allowed fields
            allowed_fields = [
                'name', 'description', 'primary_color', 'secondary_color', 'accent_color',
                'background_color', 'foreground_color', 'success_color', 'warning_color',
                'error_color', 'info_color', 'font_family', 'font_size', 'icon_style'
            ]
            
            for field, value in updates.items():
                if field in allowed_fields:
                    setattr(theme, field, value)
            
            theme.updated_at = datetime.now()
            self._save_themes()
            
            print(f"🎨 Theme '{theme.name}' customized successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error customizing theme: {e}")
            return False
    
    def delete_theme(self, theme_id: str) -> bool:
        """Delete a theme"""
        if theme_id not in self.themes:
            print(f"❌ Theme '{theme_id}' not found")
            return False
        
        # Don't allow deletion of default themes
        default_themes = ['classic_hello_kitty', 'pastel_dreams', 'starry_night', 
                         'rainbow_kitty', 'minimal_pink', 'neon_glow']
        if theme_id in default_themes:
            print(f"❌ Cannot delete default theme '{theme_id}'")
            return False
        
        try:
            name = self.themes[theme_id].name
            del self.themes[theme_id]
            
            # Reset active theme if it was deleted
            if self.active_theme_id == theme_id:
                self.active_theme_id = 'classic_hello_kitty'
            
            self._save_themes()
            
            print(f"🗑️ Theme '{name}' deleted. Bye bye! (òωó)")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting theme: {e}")
            return False
    
    def export_theme(self, theme_id: str, export_path: str) -> bool:
        """Export theme to file"""
        theme = self.themes.get(theme_id)
        if not theme:
            print(f"❌ Theme '{theme_id}' not found")
            return False
        
        try:
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'exported_by': 'kawaii_tui',
                'theme': theme.to_dict()
            }
            
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"📤 Theme '{theme.name}' exported to {export_path}! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting theme: {e}")
            return False
    
    def import_theme(self, import_path: str) -> bool:
        """Import theme from file"""
        try:
            with open(import_path, 'r') as f:
                import_data = json.load(f)
            
            theme_data = import_data['theme']
            theme_data['created_at'] = datetime.now().isoformat()
            theme_data['updated_at'] = datetime.now().isoformat()
            
            # Generate new ID to avoid conflicts
            theme_data['id'] = self._generate_theme_id(theme_data['name'])
            
            theme = self._dict_to_theme(theme_data)
            self.themes[theme.id] = theme
            self._save_themes()
            
            print(f"📥 Theme '{theme.name}' imported successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error importing theme: {e}")
            return False
    
    def get_theme_preview(self, theme_id: str) -> str:
        """Generate theme preview text"""
        theme = self.themes.get(theme_id)
        if not theme:
            return "❌ Theme not found"
        
        preview = f"""
🎨 Theme Preview: {theme.name}
{'=' * 50}
📝 Description: {theme.description}
🎯 Type: {theme.theme_type.value.title()}
💖 Kawaii Level: {theme.kawaii_level}

🎨 Color Palette:
  Primary: {theme.primary_color}
  Secondary: {theme.secondary_color}
  Accent: {theme.accent_color}
  Background: {theme.background_color}
  Foreground: {theme.foreground_color}

🔤 Typography:
  Font: {theme.font_family}
  Size: {theme.font_size}px
  Style: {theme.icon_style}

✨ Visual Elements:
  Borders: {theme.border_style}
  Icons: {theme.icon_style}
  Animations: {theme.animation_level}
  Hello Kitty Elements: {"Yes" if theme.hello_kitty_elements else "No"}

⭐ Rating: {theme.rating}/5.0
👤 Author: {theme.author}
        """
        
        return preview.strip()
    
    def get_color_scheme(self, theme_id: str) -> Dict[str, str]:
        """Get color scheme for a theme"""
        theme = self.themes.get(theme_id)
        if not theme:
            return {}
        
        return {
            'primary': theme.primary_color,
            'secondary': theme.secondary_color,
            'accent': theme.accent_color,
            'background': theme.background_color,
            'foreground': theme.foreground_color,
            'success': theme.success_color,
            'warning': theme.warning_color,
            'error': theme.error_color,
            'info': theme.info_color
        }
    
    def validate_color_scheme(self, color_scheme: Dict[str, str]) -> Tuple[bool, List[str]]:
        """Validate a color scheme"""
        errors = []
        
        required_colors = ['primary', 'secondary', 'accent', 'background', 'foreground']
        for color in required_colors:
            if color not in color_scheme:
                errors.append(f"Missing required color: {color}")
            elif not self._is_valid_hex(color_scheme[color]):
                errors.append(f"Invalid hex color for {color}: {color_scheme[color]}")
        
        return len(errors) == 0, errors
    
    def _is_valid_hex(self, color: str) -> bool:
        """Check if color is valid hex format"""
        import re
        return re.match(r'^#[0-9A-Fa-f]{6}$', color) is not None
    
    def generate_theme_report(self) -> str:
        """Generate kawaii theme report"""
        themes = list(self.themes.values())
        active_theme = self.get_active_theme()
        
        # Calculate statistics
        themes_by_type = {}
        themes_by_mode = {}
        avg_rating = sum(t.rating for t in themes) / len(themes) if themes else 0
        
        for theme in themes:
            themes_by_type[theme.theme_type.value] = themes_by_type.get(theme.theme_type.value, 0) + 1
            themes_by_mode[theme.color_mode.value] = themes_by_mode.get(theme.color_mode.value, 0) + 1
        
        report = f"""
🎨 Kawaii Theme Manager Report ♡
─────────────────────────────────
📦 Total Themes: {len(themes)}
🎯 Active Theme: {active_theme.name if active_theme else 'None'}
⭐ Average Rating: {avg_rating:.1f}/5.0

🎨 By Theme Type:
{self._format_theme_type_stats(themes_by_type)}

🌙 By Color Mode:
{self._format_color_mode_stats(themes_by_mode)}

💖 All themes feature Hello Kitty compatibility!
🎀 Your kawaii aesthetic is always on point! (òωó)
        """
        
        return report
    
    def _format_theme_type_stats(self, type_stats: Dict[str, int]) -> str:
        """Format theme type statistics"""
        lines = []
        for theme_type, count in type_stats.items():
            type_name = theme_type.replace('_', ' ').title()
            lines.append(f"  {type_name}: {count} themes")
        return '\n'.join(lines)
    
    def _format_color_mode_stats(self, mode_stats: Dict[str, int]) -> str:
        """Format color mode statistics"""
        lines = []
        for mode, count in mode_stats.items():
            mode_name = mode.title()
            lines.append(f"  {mode_name} Mode: {count} themes")
        return '\n'.join(lines)


# Demo function
def demo_kawaii_theme_system():
    """Demonstrate kawaii theme system"""
    print("🎀 Kawaii Theme System Demo (òωó)")
    print("=" * 50)
    
    theme_manager = KawaiiThemeManager()
    
    # Show available themes
    print("\n🎨 Available Themes:")
    for theme in theme_manager.list_themes():
        status = "👑" if theme.id == theme_manager.active_theme_id else "  "
        print(f"  {status} {theme.name} (⭐{theme.rating})")
    
    # Show theme preview
    print("\n🔍 Theme Preview (Classic Hello Kitty):")
    print(theme_manager.get_theme_preview('classic_hello_kitty'))
    
    # Show color scheme
    print("\n🎨 Color Scheme (Classic Hello Kitty):")
    colors = theme_manager.get_color_scheme('classic_hello_kitty')
    for color_name, hex_value in colors.items():
        print(f"  {color_name.title()}: {hex_value}")
    
    # Show statistics
    print("\n📊 Theme Statistics:")
    report = theme_manager.generate_theme_report()
    print(report)
    
    print("\n💖 Demo complete! Ready to customize your kawaii aesthetic! ♡")


if __name__ == "__main__":
    demo_kawaii_theme_system()