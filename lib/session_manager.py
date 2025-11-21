#!/usr/bin/env python3
"""
🎀 Kawaii Session Manager
Hello Kitty themed tmux session management with enhanced collaboration features
"""

import json
import os
import shutil
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Hello Kitty themed paths
HK_PATHS = {
    'session_dir': os.path.expanduser('~/.kawaii_sessions'),
    'snapshots_dir': os.path.expanduser('~/.kawaii_snapshots'),
    'templates_dir': os.path.expanduser('~/.kawaii_templates'),
    'logs_dir': os.path.expanduser('~/.kawaii_logs')
}

# Hello Kitty color palette for session theming
HK_SESSION_COLORS = {
    'primary': '#F5A3C8',      # Rogue Pink
    'secondary': '#ED164F',    # Spanish Crimson
    'accent': '#FFE717',       # Vivid Yellow
    'background': '#1E181A',   # Eerie Black
    'text': '#F2F1F2',         # Aragonite White
    'success': '#E9CA01',      # Wild Honey
    'warning': '#F2D925',
    'info': '#095D9A'
}


class SessionType(Enum):
    """Types of kawaii sessions"""
    COLLABORATION = "collaboration"
    DEVELOPMENT = "development"
    MONITORING = "monitoring"
    PRESENTATION = "presentation"
    LEARNING = "learning"
    CUSTOM = "custom"


class SessionStatus(Enum):
    """Session status states"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


@dataclass
class KawaiiSession:
    """Kawaii session data structure"""
    name: str
    session_type: SessionType
    status: SessionStatus
    created_at: datetime
    last_activity: datetime
    collaborators: List[str]
    description: str
    kawaii_level: str
    metadata: Dict
    tmux_config: Dict
    hello_kitty_theme: bool
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['last_activity'] = self.last_activity.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'KawaiiSession':
        """Create from dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_activity'] = datetime.fromisoformat(data['last_activity'])
        data['session_type'] = SessionType(data['session_type'])
        data['status'] = SessionStatus(data['status'])
        return cls(**data)


@dataclass
class SessionTemplate:
    """Pre-configured session template"""
    name: str
    session_type: SessionType
    description: str
    tmux_config: Dict
    initial_commands: List[str]
    hello_kitty_config: Dict
    tags: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        data = asdict(self)
        data['session_type'] = self.session_type.value
        return data


class KawaiiSessionManager:
    """Enhanced session manager with Hello Kitty theming"""
    
    def __init__(self):
        self.sessions: Dict[str, KawaiiSession] = {}
        self.templates: Dict[str, SessionTemplate] = {}
        self.session_history: List[str] = []
        
        # Initialize directories
        self._initialize_directories()
        
        # Load existing sessions
        self._load_sessions()
        
        # Initialize default templates
        self._initialize_default_templates()
    
    def _initialize_directories(self):
        """Create kawaii directory structure"""
        for path in HK_PATHS.values():
            Path(path).mkdir(parents=True, exist_ok=True)
            
        # Create subdirectories
        Path(HK_PATHS['session_dir']).mkdir(exist_ok=True)
        Path(HK_PATHS['snapshots_dir']).mkdir(exist_ok=True)
        Path(HK_PATHS['templates_dir']).mkdir(exist_ok=True)
        Path(HK_PATHS['logs_dir']).mkdir(exist_ok=True)
    
    def _load_sessions(self):
        """Load existing sessions from disk"""
        sessions_file = os.path.join(HK_PATHS['session_dir'], 'sessions.json')
        
        if os.path.exists(sessions_file):
            try:
                with open(sessions_file, 'r') as f:
                    data = json.load(f)
                    
                for session_name, session_data in data.items():
                    try:
                        session = KawaiiSession.from_dict(session_data)
                        self.sessions[session_name] = session
                    except Exception as e:
                        print(f"⚠️ Error loading session {session_name}: {e}")
                        
            except Exception as e:
                print(f"❌ Error loading sessions: {e}")
    
    def _save_sessions(self):
        """Save sessions to disk"""
        sessions_file = os.path.join(HK_PATHS['session_dir'], 'sessions.json')
        
        try:
            data = {name: session.to_dict() for name, session in self.sessions.items()}
            
            with open(sessions_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error saving sessions: {e}")
    
    def _initialize_default_templates(self):
        """Initialize default Hello Kitty session templates"""
        templates = [
            SessionTemplate(
                name="Kawaii Collaboration",
                session_type=SessionType.COLLABORATION,
                description="Perfect for AI collaboration sessions with Hello Kitty theming",
                tmux_config={
                    "layout": "even-horizontal",
                    "synchronize_panes": True,
                    "window_name": "kawaii_collaboration"
                },
                initial_commands=[
                    "echo '🎀 Welcome to Kawaii Collaboration! ♡'",
                    "clear"
                ],
                hello_kitty_config={
                    "theme_colors": HK_SESSION_COLORS,
                    "kawaii_messages": True,
                    "cute_notifications": True
                },
                tags=["collaboration", "ai", "hello_kitty", "kawaii"]
            ),
            
            SessionTemplate(
                name="Development Workspace",
                session_type=SessionType.DEVELOPMENT,
                description="Optimized for development work with kawaii styling",
                tmux_config={
                    "layout": "tiled",
                    "synchronize_panes": False,
                    "window_name": "kawaii_dev_workspace"
                },
                initial_commands=[
                    "echo '💻 Kawaii Development Workspace Ready! (òωó)'",
                    "clear"
                ],
                hello_kitty_config={
                    "theme_colors": HK_SESSION_COLORS,
                    "development_tools": True,
                    "cute_prompts": True
                },
                tags=["development", "coding", "hello_kitty", "productivity"]
            ),
            
            SessionTemplate(
                name="Kawaii Monitoring",
                session_type=SessionType.MONITORING,
                description="System monitoring with adorable Hello Kitty interface",
                tmux_config={
                    "layout": "even-vertical",
                    "synchronize_panes": False,
                    "window_name": "kawaii_monitor"
                },
                initial_commands=[
                    "echo '📊 Kawaii Monitoring Station Active! ♡'",
                    "echo 'System health: MAXIMUM KAWAII LEVEL! (òωó)'",
                    "clear"
                ],
                hello_kitty_config={
                    "monitoring_colors": True,
                    "kawaii_metrics": True,
                    "cute_alerts": True
                },
                tags=["monitoring", "system", "hello_kitty", "observability"]
            ),
            
            SessionTemplate(
                name="Presentation Mode",
                session_type=SessionType.PRESENTATION,
                description="Beautiful presentation setup with Hello Kitty theming",
                tmux_config={
                    "layout": "even-horizontal",
                    "synchronize_panes": False,
                    "window_name": "kawaii_presentation"
                },
                initial_commands=[
                    "echo '🎭 Kawaii Presentation Ready! ♡'",
                    "echo 'Prepare for maximum cuteness! (òωó)'",
                    "clear"
                ],
                hello_kitty_config={
                    "presentation_theme": True,
                    "hello_kitty_branding": True,
                    "cute_transitions": True
                },
                tags=["presentation", "demo", "hello_kitty", "showcase"]
            ),
            
            SessionTemplate(
                name="Learning Circle",
                session_type=SessionType.LEARNING,
                description="Educational sessions with kawaii learning environment",
                tmux_config={
                    "layout": "tiled",
                    "synchronize_panes": False,
                    "window_name": "kawaii_learning"
                },
                initial_commands=[
                    "echo '📚 Kawaii Learning Circle Active! ♡'",
                    "echo 'Knowledge sharing with maximum cuteness! (òωó)'",
                    "clear"
                ],
                hello_kitty_config={
                    "educational_theme": True,
                    "kawaii_icons": True,
                    "learning_rewards": True
                },
                tags=["learning", "education", "hello_kitty", "knowledge"]
            )
        ]
        
        for template in templates:
            self.templates[template.name] = template
    
    def create_session(self, 
                      name: str, 
                      session_type: SessionType = SessionType.COLLABORATION,
                      template_name: Optional[str] = None,
                      collaborators: Optional[List[str]] = None,
                      description: str = "",
                      hello_kitty_theme: bool = True) -> bool:
        """Create a new kawaii session"""
        try:
            # Validate session name
            if not self._validate_session_name(name):
                print(f"❌ Invalid session name: {name}")
                return False
            
            # Check if session already exists
            if name in self.sessions:
                print(f"❌ Session '{name}' already exists")
                return False
            
            # Get template if specified
            template = None
            if template_name:
                template = self.templates.get(template_name)
                if not template:
                    print(f"❌ Template '{template_name}' not found")
                    return False
            
            # Create tmux session
            if not self._create_tmux_session(name, template):
                return False
            
            # Create session object
            now = datetime.now()
            session = KawaiiSession(
                name=name,
                session_type=session_type,
                status=SessionStatus.ACTIVE,
                created_at=now,
                last_activity=now,
                collaborators=collaborators or [],
                description=description or f"Kawaii {session_type.value} session",
                kawaii_level="MAXIMUM",
                metadata={},
                tmux_config=template.tmux_config if template else {},
                hello_kitty_theme=hello_kitty_theme
            )
            
            # Store session
            self.sessions[name] = session
            self._save_sessions()
            
            # Apply Hello Kitty theme if enabled
            if hello_kitty_theme:
                self._apply_hello_kitty_theme(name, template)
            
            # Send initial commands
            if template and template.initial_commands:
                self._send_initial_commands(name, template.initial_commands)
            
            # Display success message
            self._display_creation_success(name, session_type, template_name)
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating session '{name}': {e}")
            return False
    
    def _validate_session_name(self, name: str) -> bool:
        """Validate session name"""
        if not name or len(name) > 50:
            return False
        
        # Allow alphanumeric, hyphens, underscores, and dots
        import re
        return re.match(r'^[a-zA-Z0-9._-]+$', name) is not None
    
    def _create_tmux_session(self, name: str, template: Optional[SessionTemplate]) -> bool:
        """Create tmux session"""
        try:
            # Create basic session
            window_name = template.tmux_config.get('window_name', name) if template else name
            
            cmd = ['tmux', 'new-session', '-d', '-s', name, '-n', window_name]
            subprocess.run(cmd, check=True)
            
            # Apply layout if specified
            if template and 'layout' in template.tmux_config:
                layout = template.tmux_config['layout']
                subprocess.run(['tmux', 'select-layout', '-t', f'{name}:0', layout], check=True)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create tmux session: {e}")
            return False
    
    def _apply_hello_kitty_theme(self, 
                               session_name: str, 
                               template: Optional[SessionTemplate]):
        """Apply Hello Kitty theme to session"""
        colors = template.hello_kitty_config.get('theme_colors', HK_SESSION_COLORS) if template else HK_SESSION_COLORS
        
        theme_commands = [
            # Status bar theming
            f"tmux set-option -t {session_name} status-style 'bg={colors['primary']} fg={colors['background']}'",
            f"tmux set-option -t {session_name} status-left '#[bg={colors['primary']} fg={colors['background']}]🎀 Kawaii #[bg={colors['background']} fg={colors['accent']}] Mode #[default]'",
            f"tmux set-option -t {session_name} status-right '#[bg={colors['accent']} fg={colors['background']}]♡ oωo ♡ #[bg={colors['background']} fg={colors['primary']}]%H:%M #[default]'",
            
            # Window status
            f"tmux set-window-option -t {session_name} window-status-current-style 'fg={colors['accent']} bg={colors['background']} bold'",
            f"tmux set-window-option -t {session_name} window-status-style 'fg={colors['primary']} bg={colors['background']}'",
            
            # Pane borders
            f"tmux set-option -t {session_name} pane-border-style 'fg={colors['primary']}'",
            f"tmux set-option -t {session_name} pane-active-border-style 'fg={colors['accent']} bold'",
            
            # Messages
            f"tmux set-option -t {session_name} message-style 'bg={colors['accent']} fg={colors['background']} bold'"
        ]
        
        for cmd in theme_commands:
            try:
                subprocess.run(cmd.split(), check=True)
            except subprocess.CalledProcessError:
                continue
    
    def _send_initial_commands(self, session_name: str, commands: List[str]):
        """Send initial commands to session"""
        for i, cmd in enumerate(commands):
            time.sleep(0.1)  # Small delay between commands
            try:
                subprocess.run(['tmux', 'send-keys', '-t', f'{session_name}:0', cmd, 'Enter'], check=True)
            except subprocess.CalledProcessError:
                continue
    
    def _display_creation_success(self, 
                                name: str, 
                                session_type: SessionType, 
                                template_name: Optional[str]):
        """Display kawaii creation success message"""
        success_msg = f"""
🎀 Kawaii Session Created Successfully! ♡
──────────────────────────────────────
Session: {name}
Type: {session_type.value.title()}
Template: {template_name or 'Custom'}
Theme: Hello Kitty (Maximum Cuteness!)

🚀 Quick Commands:
• Attach: tmux attach -t {name}
• Detach: Ctrl+b then d
• List: tmux list-sessions

💖 Ready for kawaii collaboration! (òωó)

Happy creating! ♡
        """
        print(success_msg)
    
    def list_sessions(self, status_filter: Optional[SessionStatus] = None) -> List[KawaiiSession]:
        """List all sessions, optionally filtered by status"""
        sessions = list(self.sessions.values())
        
        if status_filter:
            sessions = [s for s in sessions if s.status == status_filter]
        
        # Sort by last activity (most recent first)
        sessions.sort(key=lambda s: s.last_activity, reverse=True)
        return sessions
    
    def get_session(self, name: str) -> Optional[KawaiiSession]:
        """Get session by name"""
        return self.sessions.get(name)
    
    def attach_to_session(self, name: str) -> bool:
        """Attach to a session"""
        if name not in self.sessions:
            print(f"❌ Session '{name}' not found")
            return False
        
        # Update last activity
        self.sessions[name].last_activity = datetime.now()
        self._save_sessions()
        
        try:
            subprocess.run(['tmux', 'attach', '-t', name], check=True)
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to attach to session '{name}'")
            return False
    
    def suspend_session(self, name: str) -> bool:
        """Suspend a session (detach all clients)"""
        if name not in self.sessions:
            print(f"❌ Session '{name}' not found")
            return False
        
        try:
            subprocess.run(['tmux', 'suspend-client', '-t', name], check=True)
            
            self.sessions[name].status = SessionStatus.SUSPENDED
            self.sessions[name].last_activity = datetime.now()
            self._save_sessions()
            
            print(f"💤 Session '{name}' suspended gracefully! ♡")
            return True
            
        except subprocess.CalledProcessError:
            print(f"❌ Failed to suspend session '{name}'")
            return False
    
    def kill_session(self, name: str) -> bool:
        """Kill a session"""
        if name not in self.sessions:
            print(f"❌ Session '{name}' not found")
            return False
        
        try:
            subprocess.run(['tmux', 'kill-session', '-t', name], check=True)
            
            # Remove from local tracking
            del self.sessions[name]
            self._save_sessions()
            
            print(f"💔 Session '{name}' ended. Bye bye! (òωó)")
            return True
            
        except subprocess.CalledProcessError:
            print(f"❌ Failed to kill session '{name}'")
            return False
    
    def create_snapshot(self, name: str, description: str = "") -> bool:
        """Create a session snapshot"""
        if name not in self.sessions:
            print(f"❌ Session '{name}' not found")
            return False
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_name = f"{name}_snapshot_{timestamp}"
            
            # Create snapshot directory
            snapshot_dir = os.path.join(HK_PATHS['snapshots_dir'], snapshot_name)
            os.makedirs(snapshot_dir, exist_ok=True)
            
            # Capture tmux session info
            session_info = {
                'name': name,
                'snapshot_time': timestamp,
                'description': description or f"Snapshot of {name}",
                'session_data': self.sessions[name].to_dict(),
                'created_by': 'kawaii_tui'
            }
            
            # Save session info
            with open(os.path.join(snapshot_dir, 'session_info.json'), 'w') as f:
                json.dump(session_info, f, indent=2)
            
            # Capture tmux layout
            result = subprocess.run([
                'tmux', 'list-windows', '-t', name, '-F', 
                '#{window_index} #{window_name} #{window_layout} #{window_panes}'
            ], capture_output=True, text=True, check=True)
            
            windows_info = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split(' ', 3)
                    if len(parts) >= 4:
                        windows_info.append({
                            'index': parts[0],
                            'name': parts[1],
                            'layout': parts[2],
                            'panes': parts[3]
                        })
            
            with open(os.path.join(snapshot_dir, 'windows_info.json'), 'w') as f:
                json.dump(windows_info, f, indent=2)
            
            print(f"📸 Snapshot '{snapshot_name}' created successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error creating snapshot: {e}")
            return False
    
    def restore_snapshot(self, snapshot_name: str, new_session_name: str = None) -> bool:
        """Restore a session from snapshot"""
        try:
            snapshot_dir = os.path.join(HK_PATHS['snapshots_dir'], snapshot_name)
            
            if not os.path.exists(snapshot_dir):
                print(f"❌ Snapshot '{snapshot_name}' not found")
                return False
            
            # Load snapshot info
            with open(os.path.join(snapshot_dir, 'session_info.json'), 'r') as f:
                snapshot_info = json.load(f)
            
            session_data = snapshot_info['session_data']
            session_data['name'] = new_session_name or snapshot_name
            session_data['created_at'] = datetime.now()
            session_data['last_activity'] = datetime.now()
            
            # Create new session
            new_session = KawaiiSession.from_dict(session_data)
            
            # Restore in tmux (this would need tmux session restore functionality)
            print(f"🔄 Snapshot restoration would be implemented here")
            print(f"📝 Would restore session from: {snapshot_name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error restoring snapshot: {e}")
            return False
    
    def list_snapshots(self) -> List[Dict]:
        """List available snapshots"""
        snapshots = []
        snapshots_dir = HK_PATHS['snapshots_dir']
        
        if os.path.exists(snapshots_dir):
            for item in os.listdir(snapshots_dir):
                item_path = os.path.join(snapshots_dir, item)
                if os.path.isdir(item):
                    snapshot_info_file = os.path.join(item_path, 'session_info.json')
                    if os.path.exists(snapshot_info_file):
                        try:
                            with open(snapshot_info_file, 'r') as f:
                                snapshot_info = json.load(f)
                            snapshots.append({
                                'name': item,
                                'original_session': snapshot_info['name'],
                                'created': snapshot_info['snapshot_time'],
                                'description': snapshot_info['description']
                            })
                        except Exception:
                            continue
        
        # Sort by creation time (newest first)
        snapshots.sort(key=lambda s: s['created'], reverse=True)
        return snapshots
    
    def list_templates(self) -> List[SessionTemplate]:
        """List available session templates"""
        return list(self.templates.values())
    
    def create_template(self, 
                       name: str,
                       description: str,
                       session_type: SessionType,
                       base_session: Optional[str] = None) -> bool:
        """Create template from existing session"""
        try:
            if base_session and base_session not in self.sessions:
                print(f"❌ Base session '{base_session}' not found")
                return False
            
            # Capture session state if base session provided
            tmux_config = {}
            initial_commands = []
            
            if base_session:
                # Get window layout
                result = subprocess.run([
                    'tmux', 'display-message', '-t', f'{base_session}:0', '-p', '#{window_layout}'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    tmux_config['layout'] = result.stdout.strip()
                else:
                    tmux_config['layout'] = 'even-horizontal'
                
                tmux_config['window_name'] = f'template_{name}'
            
            template = SessionTemplate(
                name=name,
                session_type=session_type,
                description=description,
                tmux_config=tmux_config,
                initial_commands=initial_commands,
                hello_kitty_config={'theme_colors': HK_SESSION_COLORS},
                tags=['custom']
            )
            
            # Save template
            templates_file = os.path.join(HK_PATHS['templates_dir'], 'templates.json')
            templates_data = {}
            
            if os.path.exists(templates_file):
                with open(templates_file, 'r') as f:
                    templates_data = json.load(f)
            
            templates_data[name] = template.to_dict()
            
            with open(templates_file, 'w') as f:
                json.dump(templates_data, f, indent=2)
            
            # Load template into memory
            self.templates[name] = template
            
            print(f"🎨 Template '{name}' created successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error creating template: {e}")
            return False
    
    def get_session_stats(self) -> Dict:
        """Get session statistics"""
        total_sessions = len(self.sessions)
        active_sessions = len([s for s in self.sessions.values() if s.status == SessionStatus.ACTIVE])
        
        # Calculate total session time
        total_time = 0
        for session in self.sessions.values():
            duration = session.last_activity - session.created_at
            total_time += duration.total_seconds()
        
        # Most used session types
        type_counts = {}
        for session in self.sessions.values():
            session_type = session.session_type.value
            type_counts[session_type] = type_counts.get(session_type, 0) + 1
        
        return {
            'total_sessions': total_sessions,
            'active_sessions': active_sessions,
            'inactive_sessions': total_sessions - active_sessions,
            'total_runtime_hours': total_time / 3600,
            'average_session_duration': (total_time / total_sessions / 3600) if total_sessions > 0 else 0,
            'session_types': type_counts,
            'kawaii_level': 'MAXIMUM' if active_sessions > 0 else 'STANDBY'
        }
    
    def cleanup_old_sessions(self, days: int = 30) -> int:
        """Clean up old inactive sessions"""
        cutoff_date = datetime.now() - timedelta(days=days)
        cleaned_count = 0
        
        sessions_to_remove = []
        for name, session in self.sessions.items():
            if (session.status == SessionStatus.INACTIVE and 
                session.last_activity < cutoff_date):
                sessions_to_remove.append(name)
        
        for name in sessions_to_remove:
            # Clean up tmux session
            try:
                subprocess.run(['tmux', 'kill-session', '-t', name], 
                             capture_output=True)
            except subprocess.CalledProcessError:
                pass
            
            # Remove from tracking
            del self.sessions[name]
            cleaned_count += 1
        
        if cleaned_count > 0:
            self._save_sessions()
            print(f"🧹 Cleaned up {cleaned_count} old kawaii sessions! ♡")
        
        return cleaned_count
    
    def export_session(self, name: str, export_path: str) -> bool:
        """Export session configuration"""
        if name not in self.sessions:
            print(f"❌ Session '{name}' not found")
            return False
        
        try:
            session_data = self.sessions[name].to_dict()
            session_data['exported_at'] = datetime.now().isoformat()
            session_data['exported_by'] = 'kawaii_tui'
            
            with open(export_path, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            print(f"📤 Session '{name}' exported to {export_path}! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting session: {e}")
            return False
    
    def import_session(self, import_path: str, new_name: Optional[str] = None) -> bool:
        """Import session configuration"""
        try:
            with open(import_path, 'r') as f:
                session_data = json.load(f)
            
            # Create new session from imported data
            original_name = session_data['name']
            session_data['name'] = new_name or f"{original_name}_imported"
            session_data['created_at'] = datetime.now().isoformat()
            session_data['last_activity'] = datetime.now()
            
            new_session = KawaiiSession.from_dict(session_data)
            self.sessions[new_session.name] = new_session
            self._save_sessions()
            
            print(f"📥 Session '{original_name}' imported as '{new_session.name}'! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error importing session: {e}")
            return False


# Demo function
def demo_kawaii_session_manager():
    """Demonstrate kawaii session manager"""
    print("🎀 Kawaii Session Manager Demo (òωó)")
    print("=" * 50)
    
    manager = KawaiiSessionManager()
    
    # Show available templates
    print("\n📋 Available Templates:")
    for template in manager.list_templates():
        print(f"  🎭 {template.name}: {template.description}")
    
    # Show statistics
    print("\n📊 Session Statistics:")
    stats = manager.get_session_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # List existing sessions
    print("\n💼 Current Sessions:")
    sessions = manager.list_sessions()
    if sessions:
        for session in sessions:
            print(f"  🖥️ {session.name} ({session.session_type.value}) - {session.status.value}")
    else:
        print("  📭 No sessions created yet")
    
    print("\n💖 Demo complete! Ready to manage kawaii sessions! ♡")


if __name__ == "__main__":
    demo_kawaii_session_manager()