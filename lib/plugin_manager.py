#!/usr/bin/env python3
"""
🎀 Kawaii Plugin Manager
Interface for managing Hello Kitty plugins and extending functionality
"""

import json
import os
import subprocess
import sys
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Hello Kitty themed paths
PLUGIN_PATHS = {
    'plugins_dir': os.path.expanduser('~/.kawaii_plugins'),
    'enabled_dir': os.path.expanduser('~/.kawaii_plugins_enabled'),
    'store_dir': os.path.expanduser('~/.kawaii_plugin_store'),
    'config_dir': os.path.expanduser('~/.kawaii_plugin_config'),
    'cache_dir': os.path.expanduser('~/.kawaii_plugin_cache')
}

# Plugin categories
PLUGIN_CATEGORIES = {
    'theming': '🎨 Theme & Visual Plugins',
    'collaboration': '🤝 Collaboration Enhancers',
    'productivity': '⚡ Productivity Boosters',
    'ai_integration': '🤖 AI Integration Tools',
    'monitoring': '📊 Monitoring & Analytics',
    'entertainment': '🎵 Entertainment & Fun',
    'development': '💻 Development Tools',
    'custom': '🎀 Custom Plugins'
}

# Hello Kitty color palette for plugin visualization
HK_PLUGIN_COLORS = {
    'primary': '#F5A3C8',      # Rogue Pink
    'secondary': '#ED164F',    # Spanish Crimson
    'accent': '#FFE717',       # Vivid Yellow
    'background': '#1E181A',   # Eerie Black
    'text': '#F2F1F2',         # Aragonite White
    'success': '#E9CA01',      # Wild Honey
    'info': '#095D9A'
}


class PluginStatus(Enum):
    """Plugin status states"""
    ENABLED = "enabled"
    DISABLED = "disabled"
    INSTALLED = "installed"
    UPDATING = "updating"
    ERROR = "error"


class PluginType(Enum):
    """Types of plugins"""
    THEME = "theme"
    ENHANCEMENT = "enhancement"
    INTEGRATION = "integration"
    VISUAL = "visual"
    FUNCTIONAL = "functional"
    CUSTOM = "custom"


@dataclass
class PluginManifest:
    """Plugin manifest and metadata"""
    id: str
    name: str
    version: str
    description: str
    author: str
    category: str
    plugin_type: PluginType
    dependencies: List[str]
    conflicts: List[str]
    min_version: str
    max_version: str
    homepage: str
    repository: str
    license: str
    tags: List[str]
    hello_kitty_compatible: bool
    kawaii_level: str
    rating: float
    downloads: int
    created_at: datetime
    updated_at: datetime
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        data['plugin_type'] = self.plugin_type.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PluginManifest':
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        data['plugin_type'] = PluginType(data['plugin_type'])
        return cls(**data)


@dataclass
class PluginInstallation:
    """Plugin installation information"""
    plugin_id: str
    installation_path: str
    status: PluginStatus
    installed_at: datetime
    enabled_at: Optional[datetime]
    configuration: Dict[str, Any]
    usage_stats: Dict[str, Any]
    error_message: Optional[str]
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['status'] = self.status.value
        data['installed_at'] = self.installed_at.isoformat()
        data['enabled_at'] = self.enabled_at.isoformat() if self.enabled_at else None
        return data


class KawaiiPluginManager:
    """Hello Kitty plugin management system"""
    
    def __init__(self):
        self.plugins: Dict[str, PluginManifest] = {}
        self.installations: Dict[str, PluginInstallation] = {}
        
        # Initialize directories
        self._initialize_directories()
        
        # Load installed plugins
        self._load_plugins()
        
        # Initialize default plugins
        self._initialize_default_plugins()
    
    def _initialize_directories(self):
        """Create plugin directory structure"""
        for path in PLUGIN_PATHS.values():
            Path(path).mkdir(parents=True, exist_ok=True)
    
    def _load_plugins(self):
        """Load installed plugins from disk"""
        plugins_file = os.path.join(PLUGIN_PATHS['plugins_dir'], 'installed_plugins.json')
        
        if os.path.exists(plugins_file):
            try:
                with open(plugins_file, 'r') as f:
                    data = json.load(f)
                
                # Load plugins
                for plugin_id, plugin_data in data.get('plugins', {}).items():
                    try:
                        plugin = PluginManifest.from_dict(plugin_data)
                        self.plugins[plugin_id] = plugin
                    except Exception as e:
                        print(f"⚠️ Error loading plugin {plugin_id}: {e}")
                
                # Load installations
                for plugin_id, install_data in data.get('installations', {}).items():
                    try:
                        installation = PluginInstallation(
                            plugin_id=install_data['plugin_id'],
                            installation_path=install_data['installation_path'],
                            status=PluginStatus(install_data['status']),
                            installed_at=datetime.fromisoformat(install_data['installed_at']),
                            enabled_at=datetime.fromisoformat(install_data['enabled_at']) if install_data['enabled_at'] else None,
                            configuration=install_data.get('configuration', {}),
                            usage_stats=install_data.get('usage_stats', {}),
                            error_message=install_data.get('error_message')
                        )
                        self.installations[plugin_id] = installation
                    except Exception as e:
                        print(f"⚠️ Error loading installation {plugin_id}: {e}")
                        
            except Exception as e:
                print(f"❌ Error loading plugins: {e}")
    
    def _save_plugins(self):
        """Save plugins to disk"""
        plugins_file = os.path.join(PLUGIN_PATHS['plugins_dir'], 'installed_plugins.json')
        
        try:
            data = {
                'plugins': {plugin_id: plugin.to_dict() for plugin_id, plugin in self.plugins.items()},
                'installations': {plugin_id: installation.to_dict() for plugin_id, installation in self.installations.items()},
                'last_updated': datetime.now().isoformat()
            }
            
            with open(plugins_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error saving plugins: {e}")
    
    def _initialize_default_plugins(self):
        """Initialize default Hello Kitty plugins"""
        if self.plugins:
            return  # Already initialized
        
        default_plugins = [
            PluginManifest(
                id="hello_kitty_theme",
                name="🎨 Hello Kitty Enhanced Theme",
                version="1.2.0",
                description="Beautiful Hello Kitty styling for all Kawaii TUI components. Includes enhanced colors, fonts, and visual elements.",
                author="Kawaii System Team",
                category="theming",
                plugin_type=PluginType.THEME,
                dependencies=[],
                conflicts=[],
                min_version="1.0.0",
                max_version="2.0.0",
                homepage="https://kawaii-tui.github.io",
                repository="https://github.com/kawaii-tui/hello-kitty-theme",
                license="MIT",
                tags=["theme", "hello_kitty", "visual", "styling"],
                hello_kitty_compatible=True,
                kawaii_level="MAXIMUM",
                rating=5.0,
                downloads=0,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            
            PluginManifest(
                id="ai_smart_assistant",
                name="🤖 AI Smart Assistant",
                version="2.1.0",
                description="Enhanced AI interaction features including smart prompts, conversation memory, and collaboration insights.",
                author="Kawaii AI Team",
                category="ai_integration",
                plugin_type=PluginType.INTEGRATION,
                dependencies=["hello_kitty_theme"],
                conflicts=[],
                min_version="1.0.0",
                max_version="2.0.0",
                homepage="https://kawaii-tui.github.io",
                repository="https://github.com/kawaii-tui/ai-assistant",
                license="Apache-2.0",
                tags=["ai", "assistant", "collaboration", "smart"],
                hello_kitty_compatible=True,
                kawaii_level="MAXIMUM",
                rating=4.8,
                downloads=0,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            
            PluginManifest(
                id="collaboration_analytics",
                name="📊 Kawaii Collaboration Analytics",
                version="1.0.5",
                description="Track and analyze your collaboration sessions with beautiful charts and insights. Perfect for optimizing your AI teamwork!",
                author="Kawaii Analytics Team",
                category="monitoring",
                plugin_type=PluginType.ENHANCEMENT,
                dependencies=["hello_kitty_theme"],
                conflicts=[],
                min_version="1.0.0",
                max_version="2.0.0",
                homepage="https://kawaii-tui.github.io",
                repository="https://github.com/kawaii-tui/analytics",
                license="MIT",
                tags=["analytics", "collaboration", "tracking", "insights"],
                hello_kitty_compatible=True,
                kawaii_level="MAXIMUM",
                rating=4.7,
                downloads=0,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            
            PluginManifest(
                id="ambient_kawaii_sounds",
                name="🎵 Ambient Kawaii Sounds",
                version="1.3.0",
                description="Add adorable ambient sounds to your collaboration sessions. Choose from nature sounds, kawaii chimes, and productivity music.",
                author="Kawaii Audio Team",
                category="entertainment",
                plugin_type=PluginType.VISUAL,
                dependencies=[],
                conflicts=[],
                min_version="1.0.0",
                max_version="2.0.0",
                homepage="https://kawaii-tui.github.io",
                repository="https://github.com/kawaii-tui/sounds",
                license="MIT",
                tags=["audio", "sounds", "ambient", "productivity"],
                hello_kitty_compatible=True,
                kawaii_level="MAXIMUM",
                rating=4.6,
                downloads=0,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            
            PluginManifest(
                id="ai_memory_manager",
                name="🧠 AI Memory Manager",
                version="1.1.0",
                description="Intelligent memory system for AI collaborations. Remembers past sessions, learns preferences, and provides contextual suggestions.",
                author="Kawaii Memory Team",
                category="collaboration",
                plugin_type=PluginType.FUNCTIONAL,
                dependencies=["ai_smart_assistant"],
                conflicts=[],
                min_version="1.0.0",
                max_version="2.0.0",
                homepage="https://kawaii-tui.github.io",
                repository="https://github.com/kawaii-tui/memory",
                license="Apache-2.0",
                tags=["memory", "ai", "learning", "context"],
                hello_kitty_compatible=True,
                kawaii_level="MAXIMUM",
                rating=4.9,
                downloads=0,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            
            PluginManifest(
                id="kawaii_notifications",
                name="⭐ Kawaii Notifications",
                version="1.0.8",
                description="Cute and helpful notification system for collaboration events, achievements, and system status updates.",
                author="Kawaii Notification Team",
                category="theming",
                plugin_type=PluginType.VISUAL,
                dependencies=["hello_kitty_theme"],
                conflicts=[],
                min_version="1.0.0",
                max_version="2.0.0",
                homepage="https://kawaii-tui.github.io",
                repository="https://github.com/kawaii-tui/notifications",
                license="MIT",
                tags=["notifications", "alerts", "visual", "cute"],
                hello_kitty_compatible=True,
                kawaii_level="MAXIMUM",
                rating=4.5,
                downloads=0,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        
        # Add default plugins
        for plugin in default_plugins:
            self.plugins[plugin.id] = plugin
        
        self._save_plugins()
    
    def list_plugins(self, 
                    category: Optional[str] = None,
                    plugin_type: Optional[PluginType] = None,
                    status_filter: Optional[PluginStatus] = None) -> List[Tuple[PluginManifest, PluginStatus]]:
        """List plugins with optional filtering"""
        results = []
        
        for plugin_id, plugin in self.plugins.items():
            # Apply filters
            if category and plugin.category != category:
                continue
            
            if plugin_type and plugin.plugin_type != plugin_type:
                continue
            
            # Get installation status
            installation = self.installations.get(plugin_id)
            status = installation.status if installation else PluginStatus.DISABLED
            
            if status_filter and status != status_filter:
                continue
            
            results.append((plugin, status))
        
        # Sort by rating and name
        results.sort(key=lambda x: (x[0].rating, x[0].name), reverse=True)
        
        return results
    
    def get_plugin(self, plugin_id: str) -> Optional[PluginManifest]:
        """Get plugin by ID"""
        return self.plugins.get(plugin_id)
    
    def install_plugin(self, plugin_id: str, source: str = "local") -> bool:
        """Install a plugin"""
        try:
            plugin = self.plugins.get(plugin_id)
            if not plugin:
                print(f"❌ Plugin '{plugin_id}' not found")
                return False
            
            # Check dependencies
            if not self._check_dependencies(plugin):
                print(f"❌ Dependencies not satisfied for '{plugin_id}'")
                return False
            
            # Check conflicts
            if self._check_conflicts(plugin):
                print(f"❌ Conflicts detected for '{plugin_id}'")
                return False
            
            # Create installation
            installation_path = os.path.join(PLUGIN_PATHS['plugins_dir'], plugin_id)
            installation = PluginInstallation(
                plugin_id=plugin_id,
                installation_path=installation_path,
                status=PluginStatus.INSTALLED,
                installed_at=datetime.now(),
                enabled_at=None,
                configuration={},
                usage_stats={},
                error_message=None
            )
            
            # Create plugin directory
            os.makedirs(installation_path, exist_ok=True)
            
            # Install plugin files (simplified)
            self._install_plugin_files(plugin_id, installation_path)
            
            # Store installation
            self.installations[plugin_id] = installation
            self._save_plugins()
            
            print(f"📦 Plugin '{plugin.name}' installed successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error installing plugin '{plugin_id}': {e}")
            return False
    
    def _check_dependencies(self, plugin: PluginManifest) -> bool:
        """Check if plugin dependencies are satisfied"""
        for dep_id in plugin.dependencies:
            if dep_id not in self.installations:
                print(f"  ❌ Missing dependency: {dep_id}")
                return False
            
            dep_install = self.installations[dep_id]
            if dep_install.status != PluginStatus.ENABLED:
                print(f"  ❌ Dependency not enabled: {dep_id}")
                return False
        
        return True
    
    def _check_conflicts(self, plugin: PluginManifest) -> bool:
        """Check for plugin conflicts"""
        for conflict_id in plugin.conflicts:
            if conflict_id in self.installations:
                conflict_install = self.installations[conflict_id]
                if conflict_install.status == PluginStatus.ENABLED:
                    print(f"  ❌ Conflict with enabled plugin: {conflict_id}")
                    return True
        return False
    
    def _install_plugin_files(self, plugin_id: str, installation_path: str):
        """Install plugin files (placeholder implementation)"""
        # Create basic plugin structure
        plugin_files = {
            'plugin.py': f'''#!/usr/bin/env python3
"""
🎀 {plugin_id.title()} Plugin
Hello Kitty compatible plugin
"""

def initialize_plugin():
    """Initialize the plugin"""
    print("🎀 {plugin_id} plugin initialized! ♡")

def get_plugin_info():
    """Get plugin information"""
    return {{
        'name': '{plugin_id}',
        'version': '1.0.0',
        'kawaii_level': 'MAXIMUM'
    }}
            ''',
            'config.json': json.dumps({
                'plugin_id': plugin_id,
                'enabled': True,
                'settings': {},
                'hello_kitty_theme': True
            }, indent=2),
            'README.md': f'''# {plugin_id.title()} Plugin

🎀 Hello Kitty Compatible Plugin

## Features
✨ Hello Kitty theme integration
🤖 Enhanced functionality
💖 Maximum cuteness level

## Usage
This plugin automatically integrates with Kawaii TUI!

## Configuration
Configure through Kawaii TUI Plugin Manager.
            '''
        }
        
        for filename, content in plugin_files.items():
            file_path = os.path.join(installation_path, filename)
            with open(file_path, 'w') as f:
                f.write(content)
    
    def enable_plugin(self, plugin_id: str) -> bool:
        """Enable an installed plugin"""
        try:
            if plugin_id not in self.installations:
                print(f"❌ Plugin '{plugin_id}' not installed")
                return False
            
            installation = self.installations[plugin_id]
            plugin = self.plugins[plugin_id]
            
            # Re-check dependencies before enabling
            if not self._check_dependencies(plugin):
                print(f"❌ Cannot enable '{plugin_id}' - dependencies not satisfied")
                return False
            
            # Enable plugin
            installation.status = PluginStatus.ENABLED
            installation.enabled_at = datetime.now()
            self._save_plugins()
            
            # Load plugin (simplified)
            self._load_plugin(plugin_id)
            
            print(f"✅ Plugin '{plugin.name}' enabled successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error enabling plugin '{plugin_id}': {e}")
            return False
    
    def disable_plugin(self, plugin_id: str) -> bool:
        """Disable an installed plugin"""
        try:
            if plugin_id not in self.installations:
                print(f"❌ Plugin '{plugin_id}' not installed")
                return False
            
            installation = self.installations[plugin_id]
            plugin = self.plugins[plugin_id]
            
            # Disable plugin
            installation.status = PluginStatus.DISABLED
            self._save_plugins()
            
            print(f"💤 Plugin '{plugin.name}' disabled. See you later! (òωó)")
            return True
            
        except Exception as e:
            print(f"❌ Error disabling plugin '{plugin_id}': {e}")
            return False
    
    def _load_plugin(self, plugin_id: str):
        """Load and initialize plugin (simplified implementation)"""
        installation = self.installations[plugin_id]
        plugin_file = os.path.join(installation.installation_path, 'plugin.py')
        
        if os.path.exists(plugin_file):
            # In a real implementation, this would properly load the plugin
            # For now, just verify it exists and print success message
            print(f"  🎀 Loading {plugin_id} plugin...")
    
    def uninstall_plugin(self, plugin_id: str) -> bool:
        """Uninstall a plugin completely"""
        try:
            if plugin_id not in self.installations:
                print(f"❌ Plugin '{plugin_id}' not installed")
                return False
            
            installation = self.installations[plugin_id]
            plugin = self.plugins[plugin_id]
            
            # Disable first if enabled
            if installation.status == PluginStatus.ENABLED:
                self.disable_plugin(plugin_id)
            
            # Remove plugin directory
            if os.path.exists(installation.installation_path):
                shutil.rmtree(installation.installation_path)
            
            # Remove from tracking
            del self.installations[plugin_id]
            self._save_plugins()
            
            print(f"🗑️ Plugin '{plugin.name}' uninstalled completely. Bye bye! (òωó)")
            return True
            
        except Exception as e:
            print(f"❌ Error uninstalling plugin '{plugin_id}': {e}")
            return False
    
    def configure_plugin(self, plugin_id: str, config: Dict[str, Any]) -> bool:
        """Configure plugin settings"""
        try:
            if plugin_id not in self.installations:
                print(f"❌ Plugin '{plugin_id}' not installed")
                return False
            
            installation = self.installations[plugin_id]
            installation.configuration.update(config)
            self._save_plugins()
            
            plugin = self.plugins[plugin_id]
            print(f"⚙️ Plugin '{plugin.name}' configured successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error configuring plugin '{plugin_id}': {e}")
            return False
    
    def get_plugin_config(self, plugin_id: str) -> Dict[str, Any]:
        """Get plugin configuration"""
        if plugin_id not in self.installations:
            return {}
        
        return self.installations[plugin_id].configuration
    
    def update_plugin(self, plugin_id: str, new_version: str = None) -> bool:
        """Update plugin to newer version"""
        try:
            if plugin_id not in self.plugins:
                print(f"❌ Plugin '{plugin_id}' not found")
                return False
            
            plugin = self.plugins[plugin_id]
            print(f"🔄 Updating {plugin.name} to version {new_version or 'latest'}...")
            
            # In a real implementation, this would download and install the update
            # For now, just simulate the update
            plugin.version = new_version or plugin.version
            plugin.updated_at = datetime.now()
            
            self._save_plugins()
            print(f"✨ Plugin '{plugin.name}' updated successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error updating plugin '{plugin_id}': {e}")
            return False
    
    def create_custom_plugin(self, 
                           plugin_name: str,
                           plugin_type: PluginType,
                           category: str,
                           description: str,
                           author: str = "Custom") -> bool:
        """Create a new custom plugin"""
        try:
            plugin_id = self._generate_plugin_id(plugin_name)
            
            # Create plugin manifest
            plugin = PluginManifest(
                id=plugin_id,
                name=plugin_name,
                version="1.0.0",
                description=description,
                author=author,
                category=category,
                plugin_type=plugin_type,
                dependencies=[],
                conflicts=[],
                min_version="1.0.0",
                max_version="2.0.0",
                homepage="",
                repository="",
                license="MIT",
                tags=["custom"],
                hello_kitty_compatible=True,
                kawaii_level="CUSTOM",
                rating=0.0,
                downloads=0,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Create installation
            installation_path = os.path.join(PLUGIN_PATHS['plugins_dir'], plugin_id)
            installation = PluginInstallation(
                plugin_id=plugin_id,
                installation_path=installation_path,
                status=PluginStatus.DISABLED,
                installed_at=datetime.now(),
                enabled_at=None,
                configuration={},
                usage_stats={},
                error_message=None
            )
            
            # Create plugin files
            os.makedirs(installation_path, exist_ok=True)
            self._create_custom_plugin_files(plugin_id, plugin_name, description)
            
            # Store plugin and installation
            self.plugins[plugin_id] = plugin
            self.installations[plugin_id] = installation
            self._save_plugins()
            
            print(f"🎨 Custom plugin '{plugin_name}' created successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error creating custom plugin: {e}")
            return False
    
    def _generate_plugin_id(self, plugin_name: str) -> str:
        """Generate unique plugin ID"""
        import re
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', plugin_name).lower()
        clean_name = re.sub(r'\s+', '_', clean_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{clean_name}_{timestamp}"
    
    def _create_custom_plugin_files(self, plugin_id: str, name: str, description: str):
        """Create files for custom plugin"""
        plugin_file = os.path.join(PLUGIN_PATHS['plugins_dir'], plugin_id, 'plugin.py')
        
        plugin_content = f'''#!/usr/bin/env python3
"""
🎀 Custom Plugin: {name}
{description}
"""

class CustomPlugin:
    def __init__(self):
        self.name = "{name}"
        self.kawaii_level = "CUSTOM"
    
    def initialize(self):
        print(f"🎀 Custom plugin {self.name} initialized! ♡")
        print("Custom functionality goes here!")
    
    def get_info(self):
        return {{
            'name': self.name,
            'kawaii_level': self.kawaii_level,
            'custom': True
        }}

# Plugin entry point
plugin = CustomPlugin()

def initialize_plugin():
    plugin.initialize()

def get_plugin_info():
    return plugin.get_info()
        '''
        
        with open(plugin_file, 'w') as f:
            f.write(plugin_content)
    
    def get_plugin_stats(self, plugin_id: str) -> Dict[str, Any]:
        """Get plugin usage statistics"""
        if plugin_id not in self.installations:
            return {}
        
        return self.installations[plugin_id].usage_stats
    
    def get_all_plugin_stats(self) -> Dict[str, Any]:
        """Get overall plugin statistics"""
        enabled_plugins = [p for p, s in self.installations.items() if s.status == PluginStatus.ENABLED]
        installed_plugins = list(self.installations.keys())
        
        # Count by category
        category_counts = {}
        for plugin_id in installed_plugins:
            plugin = self.plugins[plugin_id]
            category_counts[plugin.category] = category_counts.get(plugin.category, 0) + 1
        
        return {
            'total_plugins': len(self.plugins),
            'installed_plugins': len(installed_plugins),
            'enabled_plugins': len(enabled_plugins),
            'by_category': category_counts,
            'kawaii_coverage': f"{len([p for p in self.plugins.values() if p.hello_kitty_compatible])}/{len(self.plugins)} plugins",
            'average_rating': sum(p.rating for p in self.plugins.values()) / len(self.plugins) if self.plugins else 0
        }
    
    def search_plugins(self, query: str) -> List[PluginManifest]:
        """Search plugins by name, description, or tags"""
        query_lower = query.lower()
        matches = []
        
        for plugin in self.plugins.values():
            if (query_lower in plugin.name.lower() or
                query_lower in plugin.description.lower() or
                any(query_lower in tag.lower() for tag in plugin.tags)):
                matches.append(plugin)
        
        # Sort by relevance and rating
        def sort_key(plugin):
            relevance = 0
            if query_lower in plugin.name.lower():
                relevance += 10
            if query_lower in plugin.description.lower():
                relevance += 5
            if any(query_lower in tag.lower() for tag in plugin.tags):
                relevance += 3
            return (relevance, plugin.rating)
        
        matches.sort(key=sort_key, reverse=True)
        return matches
    
    def export_plugin_config(self, export_path: str) -> bool:
        """Export plugin configuration"""
        try:
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'exported_by': 'kawaii_tui',
                'plugins': {pid: plugin.to_dict() for pid, plugin in self.plugins.items()},
                'installations': {pid: inst.to_dict() for pid, inst in self.installations.items()},
                'statistics': self.get_all_plugin_stats()
            }
            
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"📤 Plugin configuration exported to {export_path}! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting plugin config: {e}")
            return False
    
    def generate_plugin_report(self) -> str:
        """Generate kawaii plugin report"""
        stats = self.get_all_plugin_stats()
        
        report = f"""
🔌 Kawaii Plugin Manager Report ♡
─────────────────────────────────
📦 Total Plugins: {stats['total_plugins']}
✅ Installed: {stats['installed_plugins']}
⚡ Enabled: {stats['enabled_plugins']}
⭐ Average Rating: {stats['average_rating']:.1f}/5.0
💖 Kawaii Coverage: {stats['kawaii_coverage']}

📂 Categories:
{self._format_plugin_categories(stats['by_category'])}

🎀 Your plugin arsenal is ready for kawaii collaboration! (òωó)
💖 Plugins make everything more adorable and functional! ♡
        """
        
        return report
    
    def _format_plugin_categories(self, category_counts: Dict[str, int]) -> str:
        """Format category counts for report"""
        lines = []
        for category, count in category_counts.items():
            category_name = PLUGIN_CATEGORIES.get(category, category.title())
            lines.append(f"  {category_name}: {count} plugins")
        return '\n'.join(lines) if lines else "  No plugins installed yet"


# Demo function
def demo_kawaii_plugin_manager():
    """Demonstrate kawaii plugin manager"""
    print("🎀 Kawaii Plugin Manager Demo (òωó)")
    print("=" * 50)
    
    manager = KawaiiPluginManager()
    
    # Show all plugins
    print("\n📋 Available Plugins:")
    for plugin, status in manager.list_plugins():
        status_icon = "✅" if status == PluginStatus.ENABLED else "📦" if status == PluginStatus.INSTALLED else "❌"
        print(f"  {status_icon} {plugin.name} (⭐{plugin.rating})")
    
    # Show statistics
    print("\n📊 Plugin Statistics:")
    stats = manager.get_all_plugin_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Show categories
    print("\n📂 Plugin Categories:")
    for category_id, category_name in PLUGIN_CATEGORIES.items():
        print(f"  {category_name}")
    
    # Search demo
    print("\n🔍 Search Demo:")
    results = manager.search_plugins("theme")
    for plugin in results[:2]:
        print(f"  🎨 {plugin.name}")
    
    print("\n💖 Demo complete! Ready to manage kawaii plugins! ♡")


if __name__ == "__main__":
    demo_kawaii_plugin_manager()