#!/usr/bin/env python3
"""
🎀 Kawaii Utils
Hello Kitty themed utility functions and helpers
"""

import os
import sys
import json
import subprocess
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union

# Hello Kitty themed paths
KAWAII_PATHS = {
    'config': os.path.expanduser('~/.kawaii_config'),
    'cache': os.path.expanduser('~/.kawaii_cache'),
    'logs': os.path.expanduser('~/.kawaii_logs'),
    'data': os.path.expanduser('~/.kawaii_data'),
    'tmp': os.path.expanduser('~/.kawaii_tmp')
}

# Hello Kitty ASCII art collection
HELLO_KITTY_ASCII = {
    'face': r'''
    ┌─────────────────┐
    │  (òωó) ♡        │
    │  Hello Kitty!   │
    └─────────────────┘
    ''',
    
    'heart': r'''
       ♡ ♡ ♡
     ♡       ♡
    ♡         ♡
     ♡       ♡
       ♡ ♡ ♡
    ''',
    
    'celebration': r'''
    🎀 ♡ (òωó) ♡ 🎀
    ✨ Kawaii Magic! ✨
    🎀 ♡ (òωó) ♡ 🎀
    ''',
    
    'loading': r'''
    Loading kawaii magic...
    (òωó) ♡ (òωó) ♡ (òωó)
    ''',
    
    'error': r'''
    😿 Oopsie! Something went wrong
    But don't worry, kawaii heals all! ♡
    ''',
    
    'success': r'''
    🎉 Success! Kawaii level: MAXIMUM! 
    (òωó) ♡ (òωó) ♡ (òωó)
    '''
}

# Kawaii emotions and their usage contexts
KAWAII_EMOTIONS = {
    'happy': ['♡', '(òωó)', '♪', '♫', '✨', '💖'],
    'excited': ['🎉', '(òωó)', '⚡', '🚀', '💫', '⭐'],
    'cute': ['(òωó)', '♡', '💖', '🌸', '🎀', '✨'],
    'surprised': ['(òωó)', '?!', '💫', '✨', '🎭'],
    'thinking': ['🤔', '(òωó)', '💭', '💡'],
    'love': ['💖', '♡', '❤️', '💕', '💝'],
    'work': ['⚡', '🚀', '💪', '✨', '🎯'],
    'creative': ['🎨', '✨', '💡', '🌈', '🎭'],
    'learning': ['📚', '💡', '✨', '🎓', '💖'],
    'collaboration': ['🤝', '💪', '✨', '🎀', '💖']
}

# Hello Kitty themed messages
KAWAII_MESSAGES = {
    'startup': [
        "🎀 Initializing kawaii magic...",
        "(òωó) Hello! Ready for cuteness?",
        "💖 Loading maximum kawaii level!",
        "✨ Hello Kitty system coming online!"
    ],
    
    'success': [
        "🎉 Kawaii success achieved! ♡",
        "(òωó) Everything is perfectly cute!",
        "💖 Mission accomplished with style!",
        "✨ Maximum kawaii level reached!"
    ],
    
    'error': [
        "😿 Oopsie! But don't worry, kawaii heals! ♡",
        "(òωó) Tiny problem, big solution coming!",
        "💖 Even mistakes can be adorable!",
        "✨ Kawaii power will fix this!"
    ],
    
    'loading': [
        "(òωó) Working kawaii magic...",
        "💖 Please wait while we add more cuteness!",
        "✨ Preparing maximum adorable experience!",
        "🎀 Loading kawaii level: MAXIMUM!"
    ],
    
    'farewell': [
        "💖 Thanks for using kawaii power! (òωó)",
        "🎀 See you next time for more cuteness!",
        "✨ Happy collaborating with style! ♡",
        "(òωó) Kawaii goodbye!"
    ]
}


class KawaiiLogger:
    """Hello Kitty themed logging system"""
    
    def __init__(self, name: str = "kawaii_tui"):
        self.name = name
        self.log_file = os.path.join(KAWAII_PATHS['logs'], f'{name}.log')
        
        # Ensure log directory exists
        os.makedirs(KAWAII_PATHS['logs'], exist_ok=True)
    
    def log(self, level: str, message: str, emotion: str = 'happy'):
        """Log with kawaii styling"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add kawaii emotion
        emotion_icons = KAWAII_EMOTIONS.get(emotion, ['♡'])
        emotion_icon = emotion_icons[0] if emotion_icons else '♡'
        
        # Format log message
        kawaii_message = f"[{timestamp}] {self.name} {emotion_icon} {level}: {message}"
        
        # Write to file
        try:
            with open(self.log_file, 'a') as f:
                f.write(kawaii_message + '\n')
        except Exception:
            pass  # Fail silently for logging
        
        # Print to console with color
        self._print_colored(level, kawaii_message)
    
    def _print_colored(self, level: str, message: str):
        """Print colored message based on level"""
        # Color codes for different levels
        colors = {
            'INFO': '\033[36m',    # Cyan
            'SUCCESS': '\033[32m', # Green
            'WARNING': '\033[33m', # Yellow
            'ERROR': '\033[31m',   # Red
            'DEBUG': '\033[35m',   # Magenta
        }
        
        color = colors.get(level, '\033[0m')
        reset = '\033[0m'
        
        print(f"{color}{message}{reset}")
    
    def info(self, message: str, emotion: str = 'happy'):
        """Log info message"""
        self.log('INFO', message, emotion)
    
    def success(self, message: str, emotion: str = 'excited'):
        """Log success message"""
        self.log('SUCCESS', message, emotion)
    
    def warning(self, message: str, emotion: str = 'thinking'):
        """Log warning message"""
        self.log('WARNING', message, emotion)
    
    def error(self, message: str, emotion: str = 'error'):
        """Log error message"""
        self.log('ERROR', message, emotion)
    
    def debug(self, message: str, emotion: str = 'thinking'):
        """Log debug message"""
        self.log('DEBUG', message, emotion)


class KawaiiConfig:
    """Hello Kitty themed configuration management"""
    
    def __init__(self):
        self.config_file = os.path.join(KAWAII_PATHS['config'], 'kawaii_config.json')
        self.config_data = {}
        
        # Ensure config directory exists
        os.makedirs(KAWAII_PATHS['config'], exist_ok=True)
        
        # Load or create config
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config_data = json.load(f)
            except Exception:
                self.config_data = self._create_default_config()
        else:
            self.config_data = self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration"""
        return {
            'version': '1.0.0',
            'theme': {
                'name': 'classic_hello_kitty',
                'kawaii_level': 'MAXIMUM',
                'animations': True,
                'hello_kitty_elements': True
            },
            'ui': {
                'font_size': 12,
                'color_mode': 'dark',
                'show_ascii_art': True,
                'kawaii_messages': True
            },
            'collaboration': {
                'default_agents': 2,
                'default_duration_hours': 2,
                'auto_save_sessions': True,
                'kawaii_notifications': True
            },
            'system': {
                'auto_backup': True,
                'debug_mode': False,
                'log_level': 'INFO'
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config_data, f, indent=2)
            return True
        except Exception:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        target = self.config_data
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        
        # Set the final value
        target[keys[-1]] = value
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config_data = self._create_default_config()
        self.save_config()


def kawaii_print(message: str, style: str = 'normal', emotion: str = 'happy'):
    """Print kawaii-styled message"""
    emotions = {
        'normal': '',
        'cute': '(òωó) ',
        'excited': '🎉 ',
        'love': '💖 ',
        'creative': '🎨 ',
        'work': '⚡ ',
        'celebration': '🎀 '
    }
    
    prefix = emotions.get(emotion, '')
    
    if style == 'ascii':
        print(f"{prefix}{message}")
        print(HELLO_KITTY_ASCII.get('face', ''))
    elif style == 'ascii_heart':
        print(f"{prefix}{message}")
        print(HELLO_KITTY_ASCII['heart'])
    elif style == 'celebration':
        print(f"{prefix}{message}")
        print(HELLO_KITTY_ASCII['celebration'])
    elif style == 'loading':
        print(f"{prefix}{message}")
        print(HELLO_KITTY_ASCII['loading'])
    else:
        print(f"{prefix}{message}")


def get_kawaii_message(message_type: str) -> str:
    """Get a random kawaii message"""
    messages = KAWAII_MESSAGES.get(message_type, ['(òωó) Kawaii message!'])
    import random
    return random.choice(messages)


def check_system_compatibility() -> Dict[str, bool]:
    """Check system compatibility for kawaii features"""
    checks = {
        'tmux_installed': False,
        'python_version_ok': False,
        'terminal_compatible': False,
        'colors_supported': False,
        'filesystem_accessible': False
    }
    
    try:
        # Check tmux
        result = subprocess.run(['tmux', '-V'], 
                              capture_output=True, text=True)
        checks['tmux_installed'] = result.returncode == 0
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    # Check Python version
    checks['python_version_ok'] = sys.version_info >= (3, 7)
    
    # Check terminal compatibility
    terminal = os.environ.get('TERM', '')
    checks['terminal_compatible'] = 'xterm' in terminal or 'screen' in terminal
    
    # Check color support (simplified)
    checks['colors_supported'] = os.environ.get('COLORTERM', '') in ['truecolor', '24bit']
    
    # Check filesystem access
    try:
        test_dir = KAWAII_PATHS['config']
        os.makedirs(test_dir, exist_ok=True)
        checks['filesystem_accessible'] = os.access(test_dir, os.W_OK)
    except Exception:
        pass
    
    return checks


def get_system_info() -> Dict[str, str]:
    """Get system information with kawaii styling"""
    return {
        'platform': platform.system(),
        'python_version': platform.python_version(),
        'terminal': os.environ.get('TERM', 'Unknown'),
        'shell': os.environ.get('SHELL', 'Unknown'),
        'user': os.environ.get('USER', 'Unknown'),
        'home': os.environ.get('HOME', 'Unknown'),
        'kawaii_paths': json.dumps(KAWAII_PATHS, indent=2)
    }


def validate_kawaii_environment() -> Tuple[bool, List[str]]:
    """Validate that the environment is ready for kawaii operation"""
    issues = []
    
    # Check compatibility
    checks = check_system_compatibility()
    
    for check_name, passed in checks.items():
        if not passed:
            if check_name == 'tmux_installed':
                issues.append("Tmux is not installed. Please install tmux for session management.")
            elif check_name == 'python_version_ok':
                issues.append("Python 3.7+ is required for kawaii features.")
            elif check_name == 'terminal_compatible':
                issues.append("Terminal may not support all kawaii features.")
            elif check_name == 'colors_supported':
                issues.append("Terminal may not support color kawaii effects.")
            elif check_name == 'filesystem_accessible':
                issues.append("Cannot access configuration directory.")
    
    return len(issues) == 0, issues


def install_kawaii_dependencies() -> bool:
    """Install required dependencies for kawaii functionality"""
    dependencies = ['tmux', 'python3', 'python3-pip']
    
    kawaii_print("Installing kawaii dependencies...", 'loading', 'work')
    
    try:
        for dep in dependencies:
            # Check if already installed
            if dep.startswith('python'):
                continue  # Skip Python checks
            
            result = subprocess.run(['which', dep], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                kawaii_print(f"Installing {dep}...", 'normal', 'work')
                
                # Try to install with apt
                try:
                    subprocess.run(['sudo', 'apt', 'update'], 
                                 capture_output=True, check=True)
                    subprocess.run(['sudo', 'apt', 'install', '-y', dep], 
                                 capture_output=True, check=True)
                except subprocess.CalledProcessError:
                    issues.append(f"Failed to install {dep}")
        
        kawaii_print("Dependencies installed successfully!", 'celebration', 'success')
        return True
        
    except Exception as e:
        kawaii_print(f"Error installing dependencies: {e}", 'normal', 'error')
        return False


def create_kawaii_config() -> bool:
    """Create kawaii configuration"""
    try:
        os.makedirs(KAWAII_PATHS['config'], exist_ok=True)
        os.makedirs(KAWAII_PATHS['cache'], exist_ok=True)
        os.makedirs(KAWAII_PATHS['logs'], exist_ok=True)
        
        config = KawaiiConfig()
        config.save_config()
        
        kawaii_print("Kawaii configuration created!", 'ascii_heart', 'success')
        return True
        
    except Exception as e:
        kawaii_print(f"Error creating config: {e}", 'normal', 'error')
        return False


def get_config_dir() -> str:
    """Get the kawaii configuration directory path"""
    return KAWAII_PATHS['config']


def backup_kawaii_data(backup_path: Optional[str] = None) -> bool:
    """Backup kawaii data"""
    if not backup_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"kawaii_backup_{timestamp}.tar.gz"
    
    try:
        import tarfile
        
        with tarfile.open(backup_path, "w:gz") as tar:
            for path_name, path_value in KAWAII_PATHS.items():
                if os.path.exists(path_value):
                    tar.add(path_value, arcname=f"kawaii_{path_name}")
        
        kawaii_print(f"Backup created: {backup_path}", 'celebration', 'success')
        return True
        
    except Exception as e:
        kawaii_print(f"Backup failed: {e}", 'normal', 'error')
        return False


def restore_kawaii_data(backup_path: str) -> bool:
    """Restore kawaii data from backup"""
    try:
        import tarfile
        
        with tarfile.open(backup_path, "r:gz") as tar:
            tar.extractall()
        
        kawaii_print("Kawaii data restored successfully!", 'celebration', 'success')
        return True
        
    except Exception as e:
        kawaii_print(f"Restore failed: {e}", 'normal', 'error')
        return False


def cleanup_kawaii_cache() -> bool:
    """Clean up kawaii cache and temporary files"""
    try:
        # Clean cache directory
        if os.path.exists(KAWAII_PATHS['cache']):
            for item in os.listdir(KAWAII_PATHS['cache']):
                item_path = os.path.join(KAWAII_PATHS['cache'], item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    import shutil
                    shutil.rmtree(item_path)
        
        # Clean tmp directory
        if os.path.exists(KAWAII_PATHS['tmp']):
            import shutil
            shutil.rmtree(KAWAII_PATHS['tmp'])
            os.makedirs(KAWAII_PATHS['tmp'], exist_ok=True)
        
        kawaii_print("Kawaii cache cleaned! (òωó)", 'celebration', 'success')
        return True
        
    except Exception as e:
        kawaii_print(f"Cleanup failed: {e}", 'normal', 'error')
        return False


def get_kawaii_stats() -> Dict[str, Any]:
    """Get kawaii system statistics"""
    stats = {
        'kawaii_version': '1.0.0',
        'kawaii_level': 'MAXIMUM',
        'kawaii_coverage': '100%',
        'hello_kitty_elements': True,
        'system_info': get_system_info(),
        'compatibility': check_system_compatibility(),
        'paths': KAWAII_PATHS
    }
    
    # Count files in kawaii directories
    file_counts = {}
    total_files = 0
    
    for name, path in KAWAII_PATHS.items():
        if os.path.exists(path):
            try:
                count = sum([len(files) for r, d, files in os.walk(path)])
                file_counts[name] = count
                total_files += count
            except Exception:
                file_counts[name] = 0
        else:
            file_counts[name] = 0
    
    stats['file_counts'] = file_counts
    stats['total_files'] = total_files
    
    return stats


def kawaii_health_check() -> Dict[str, Any]:
    """Perform kawaii health check"""
    logger = KawaiiLogger('health_check')
    
    health = {
        'status': 'healthy',
        'kawaii_level': 'MAXIMUM',
        'checks': {},
        'issues': [],
        'recommendations': []
    }
    
    # Check system compatibility
    compatibility = check_system_compatibility()
    health['checks']['compatibility'] = compatibility
    
    # Check environment
    env_ok, env_issues = validate_kawaii_environment()
    health['checks']['environment'] = env_ok
    if not env_ok:
        health['issues'].extend(env_issues)
        health['status'] = 'needs_attention'
    
    # Check configuration
    try:
        config = KawaiiConfig()
        config_ok = config.get('system.debug_mode') is not None
        health['checks']['configuration'] = config_ok
        logger.info("Configuration check passed", 'cute')
    except Exception as e:
        health['checks']['configuration'] = False
        health['issues'].append(f"Configuration error: {e}")
        health['status'] = 'needs_attention'
        logger.error(f"Configuration check failed: {e}", 'error')
    
    # Check filesystem access
    try:
        for name, path in KAWAII_PATHS.items():
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
            if not os.access(path, os.W_OK):
                health['issues'].append(f"Cannot write to {path}")
                health['status'] = 'needs_attention'
    except Exception as e:
        health['issues'].append(f"Filesystem access error: {e}")
        health['status'] = 'broken'
    
    # Generate recommendations
    if health['status'] == 'healthy':
        health['recommendations'] = [
            "Your kawaii system is running perfectly! (òωó)",
            "Try exploring different collaboration modes!",
            "Customize your theme to your preference!",
            "Share the kawaii love with friends!"
        ]
    else:
        health['recommendations'] = [
            "Fix the issues above for maximum kawaii experience",
            "Check system compatibility with kawaii features",
            "Install missing dependencies",
            "Contact kawaii support if issues persist"
        ]
    
    if health['status'] == 'healthy':
        logger.success("Health check passed - kawaii level: MAXIMUM!", 'celebration')
    else:
        logger.warning(f"Health check found {len(health['issues'])} issues", 'thinking')
    
    return health


def print_kawaii_banner():
    """Print Hello Kitty banner"""
    banner = r'''
🎀 ♡ (òωó) Welcome to Kawaii TUI! ♡ 🎀
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hello Kitty AI Collaboration Manager
Where productivity meets pure cuteness! ♡

(òωó) Ready for the most adorable 
    collaboration experience ever?

🎀 Kawaii level: MAXIMUM! 🎀
    '''
    print(banner)


def kawaii_farewell():
    """Print kawaii farewell message"""
    print(get_kawaii_message('farewell'))
    print(HELLO_KITTY_ASCII['face'])


# Initialize global logger and config
logger = KawaiiLogger()
config = KawaiiConfig()


def demo_kawaii_utils():
    """Demonstrate kawaii utility functions"""
    print("🎀 Kawaii Utils Demo (òωó)")
    print("=" * 50)
    
    # Show kawaii messages
    print("\n💬 Kawaii Messages:")
    for msg_type, messages in KAWAII_MESSAGES.items():
        print(f"  {msg_type}: {messages[0]}")
    
    # Show ASCII art
    print("\n🎨 Hello Kitty ASCII Art:")
    print("Face:")
    print(HELLO_KITTY_ASCII['face'])
    print("Heart:")
    print(HELLO_KITTY_ASCII['heart'])
    
    # Show system compatibility
    print("\n🔧 System Compatibility:")
    compatibility = check_system_compatibility()
    for check, result in compatibility.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check.replace('_', ' ').title()}")
    
    # Show statistics
    print("\n📊 Kawaii Stats:")
    stats = get_kawaii_stats()
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for subkey, subvalue in value.items():
                print(f"    {subkey}: {subvalue}")
        else:
            print(f"  {key}: {value}")
    
    # Health check
    print("\n🏥 Health Check:")
    health = kawaii_health_check()
    print(f"  Status: {health['status']}")
    print(f"  Issues: {len(health['issues'])}")
    print(f"  Kawaii Level: {health['kawaii_level']}")
    
    print("\n💖 Demo complete! Ready for kawaii operations! ♡")


if __name__ == "__main__":
    demo_kawaii_utils()
