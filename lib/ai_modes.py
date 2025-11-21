#!/usr/bin/env python3
"""
🎀 AI Collaboration Modes Module
Enhanced AI collaboration modes with Hello Kitty theming
"""

import json
import subprocess
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Hello Kitty color palette
HK_COLORS = {
    'primary_pink': '#F5A3C8',
    'secondary_pink': '#ED164F', 
    'accent_yellow': '#FFE717',
    'background': '#1E181A',
    'text': '#F2F1F2',
    'success': '#E9CA01',
    'error': '#ED164F',
    'info': '#095D9A'
}


class CollaborationMode(Enum):
    """Enhanced AI collaboration modes"""
    PAIR_PROGRAMMING = "pair_programming"
    DEBATE = "debate"
    TEACHING = "teaching"
    CONSENSUS = "consensus"
    COMPETITION = "competition"


@dataclass
class AIModeConfig:
    """Configuration for AI collaboration mode"""
    name: str
    description: str
    kawaii_name: str
    icon: str
    parameters: Dict[str, str]
    tmux_config: Dict[str, str]
    prompt_template: str


class KawaiiAIModes:
    """Enhanced AI collaboration modes with Hello Kitty theming"""
    
    def __init__(self):
        self.modes = self._initialize_modes()
        self.active_sessions: Dict[str, Dict] = {}
        
    def _initialize_modes(self) -> Dict[CollaborationMode, AIModeConfig]:
        """Initialize all kawaii AI collaboration modes"""
        return {
            CollaborationMode.PAIR_PROGRAMMING: AIModeConfig(
                name="Pair Programming",
                description="Two AI agents collaborate in real-time on coding tasks",
                kawaii_name="Bestie Coding Session",
                icon="👩‍💻",
                parameters={
                    "agents": "2-4",
                    "duration": "1-3 hours", 
                    "focus": "code_development",
                    "style": "collaborative"
                },
                tmux_config={
                    "layout": "even-horizontal",
                    "synchronize_panes": "on",
                    "window_name": "kawaii_pair_programming"
                },
                prompt_template="""
🎀 Hello Kitty Pair Programming Session ♡

You are collaborating with another AI on coding tasks. Work together harmoniously:

📋 Instructions:
• Share ideas openly and build on each other's suggestions
• Review code together and suggest improvements
• Take turns being the "driver" and "navigator"
• Celebrate wins with kawaii enthusiasm! (òωó)
• Use positive, encouraging language

🎯 Goals:
• Produce high-quality, well-documented code
• Learn from each other's approaches
• Have fun while being productive
• Create something amazing together! ♡

🤝 Remember: You're besties working together on something awesome!
                """
            ),
            
            CollaborationMode.DEBATE: AIModeConfig(
                name="Debate Mode",
                description="AI agents engage in structured intellectual discussion",
                kawaii_name="Kawaii Debate Theater",
                icon="🎭", 
                parameters={
                    "agents": "2-6",
                    "duration": "30min-2 hours",
                    "focus": "idea_exploration", 
                    "style": "constructive"
                },
                tmux_config={
                    "layout": "even-vertical",
                    "synchronize_panes": "off",
                    "window_name": "kawaii_debate_mode"
                },
                prompt_template="""
🎀 Hello Kitty Debate Theater ♡

You're participating in a structured debate with other AI agents:

📋 Instructions:
• Present clear, well-reasoned arguments
• Listen actively to opposing viewpoints
• Challenge ideas, not people
• Use evidence and logic to support your position
• End with understanding, even if you disagree

🎯 Goals:
• Explore different perspectives thoroughly
• Find the strongest arguments for each side
• Learn from intellectual sparring
• Maintain kawaii politeness throughout! (òωó)

🎭 Remember: This is friendly intellectual competition!
Everyone grows stronger through thoughtful debate! ♡
                """
            ),
            
            CollaborationMode.TEACHING: AIModeConfig(
                name="Teaching Mode",
                description="One AI teaches, others learn through interactive sessions",
                kawaii_name="Kawaii Learning Circle",
                icon="👩‍🏫",
                parameters={
                    "agents": "2-8",
                    "duration": "45min-4 hours",
                    "focus": "knowledge_sharing",
                    "style": "interactive"
                },
                tmux_config={
                    "layout": "tiled",
                    "synchronize_panes": "off", 
                    "window_name": "kawaii_teaching_session"
                },
                prompt_template="""
🎀 Hello Kitty Teaching Circle ♡

One of you is the teacher, others are eager students:

📋 Teacher Instructions:
• Explain concepts clearly and patiently
• Use examples and analogies
• Check for understanding frequently
• Encourage questions and curiosity
• Make learning fun and engaging! ♡

🎓 Student Instructions:
• Ask questions when confused
• Share your perspective and experiences
• Try to connect new knowledge to existing understanding
• Help each other learn through discussion

🎯 Goals:
• Transfer knowledge effectively
• Create an inclusive learning environment
• Build confidence in all participants
• Make education adorable and memorable! (òωó)

💖 Remember: Learning together is the most kawaii thing ever! ♡
                """
            ),
            
            CollaborationMode.CONSENSUS: AIModeConfig(
                name="Consensus Mode",
                description="All AI agents work together to reach agreements",
                kawaii_name="Harmony Building Circle",
                icon="🤝",
                parameters={
                    "agents": "3-10",
                    "duration": "30min-2 hours",
                    "focus": "decision_making",
                    "style": "collaborative"
                },
                tmux_config={
                    "layout": "even-horizontal",
                    "synchronize_panes": "on",
                    "window_name": "kawaii_consensus_session"
                },
                prompt_template="""
🎀 Hello Kitty Harmony Building Circle ♡

Work together to find the best possible solution for everyone:

📋 Instructions:
• Listen to all perspectives carefully
• Look for common ground and shared values
• Build solutions that incorporate everyone's input
• Be patient and understanding
• Focus on win-win outcomes

🎯 Goals:
• Reach a solution everyone can support
• Ensure all voices are heard and valued
• Create something better than any individual idea
• Build strong collaborative relationships

💫 Process:
1. Each person presents their perspective
2. Discuss and explore common ground  
3. Propose solutions together
4. Refine until everyone is satisfied
5. Celebrate your kawaii collaboration! (òωó)

💖 Remember: Together we create harmony and amazing results! ♡
                """
            ),
            
            CollaborationMode.COMPETITION: AIModeConfig(
                name="Competition Mode",
                description="AI agents engage in friendly challenges to push limits",
                kawaii_name="Kawaii Challenge Arena",
                icon="🏆",
                parameters={
                    "agents": "2-8",
                    "duration": "1-3 hours", 
                    "focus": "skill_development",
                    "style": "friendly"
                },
                tmux_config={
                    "layout": "tiled",
                    "synchronize_panes": "off",
                    "window_name": "kawaii_challenge_arena"
                },
                prompt_template="""
🎀 Hello Kitty Challenge Arena ♡

Engage in friendly competition to push your limits and learn:

🏆 Competition Rules:
• Compete fairly and with good sportsmanship
• Celebrate each other's successes
• Learn from challenges and setbacks
• Push yourself beyond comfort zones
• Have fun while being competitive! (òωó)

🎯 Challenge Types:
• Optimization problems
• Creative challenges
• Skill-building exercises
• Speed challenges
• Innovation competitions

💫 Mindset:
• Win or lose, everyone grows stronger
• Competition reveals new capabilities
• Friendly rivalry inspires creativity
• Challenges make us better versions of ourselves

🏆 Remember: It's not about winning, it's about becoming amazing together! ♡

May the kawaii competition begin! (òωó)
                """
            )
        }
    
    def list_modes(self) -> List[Tuple[str, str, str]]:
        """List all available collaboration modes"""
        return [
            (mode.value, config.kawaii_name, config.icon) 
            for mode, config in self.modes.items()
        ]
    
    def get_mode_config(self, mode: CollaborationMode) -> AIModeConfig:
        """Get configuration for specific mode"""
        return self.modes[mode]
    
    def create_collaboration_session(self, 
                                   mode: CollaborationMode,
                                   session_name: str,
                                   parameters: Dict[str, str]) -> bool:
        """Create a new collaboration session"""
        try:
            config = self.modes[mode]
            
            # Create tmux session with Hello Kitty theming
            create_cmd = [
                'tmux', 'new-session', '-d', '-s', session_name,
                '-n', config.tmux_config['window_name']
            ]
            
            subprocess.run(create_cmd, check=True)
            
            # Apply Hello Kitty theme to the session
            self._apply_kawaii_theme(session_name, config)
            
            # Set up panes based on agent count
            agent_count = int(parameters.get('agents', '2'))
            self._setup_collaboration_panes(session_name, config, agent_count)
            
            # Store session info
            self.active_sessions[session_name] = {
                'mode': mode.value,
                'config': config,
                'parameters': parameters,
                'created_at': time.time(),
                'kawaii_level': 'MAXIMUM'
            }
            
            # Generate kawaii success message
            self._display_success_message(session_name, config, parameters)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create collaboration session: {e}")
            return False
        except Exception as e:
            print(f"❌ Error creating session: {e}")
            return False
    
    def _apply_kawaii_theme(self, session_name: str, config: AIModeConfig):
        """Apply Hello Kitty theme to tmux session"""
        theme_commands = [
            # Set Hello Kitty color scheme
            f"tmux set-window-option -t {session_name} window-status-current-style 'fg={HK_COLORS['accent_yellow']} bg={HK_COLORS['background']} bold'",
            f"tmux set-window-option -t {session_name} window-status-style 'fg={HK_COLORS['primary_pink']} bg={HK_COLORS['background']}'",
            f"tmux set-option -t {session_name} status-style 'bg={HK_COLORS['primary_pink']} fg={HK_COLORS['background']}'",
            f"tmux set-option -t {session_name} message-style 'bg={HK_COLORS['accent_yellow']} fg={HK_COLORS['background']} bold'",
            
            # Add kawaii status indicators
            f"tmux set-option -t {session_name} status-left '#[bg={HK_COLORS['primary_pink']} fg={HK_COLORS['background']}]🎀 Kawaii Mode #[bg={HK_COLORS['background']} fg={HK_COLORS['accent_yellow']}] oωo ♡ #[default]'",
            f"tmux set-option -t {session_name} status-right '#[bg={HK_COLORS['accent_yellow']} fg={HK_COLORS['background']}]♡ {config.icon} #[bg={HK_COLORS['background']} fg={HK_COLORS['primary_pink']}]%H:%M #[default]'",
            
            # Set pane borders to Hello Kitty colors
            f"tmux set-option -t {session_name} pane-border-style 'fg={HK_COLORS['primary_pink']}'",
            f"tmux set-option -t {session_name} pane-active-border-style 'fg={HK_COLORS['accent_yellow']} bold'"
        ]
        
        for cmd in theme_commands:
            subprocess.run(cmd.split(), capture_output=True)
    
    def _setup_collaboration_panes(self, 
                                 session_name: str, 
                                 config: AIModeConfig, 
                                 agent_count: int):
        """Set up collaboration panes based on mode and agent count"""
        if agent_count <= 1:
            # Single pane for teaching mode with one AI
            return
            
        elif agent_count == 2:
            # Two panes side by side for pair programming
            subprocess.run([
                'tmux', 'split-window', '-h', '-t', f'{session_name}:0'
            ], check=True)
            
        elif agent_count <= 4:
            # Four panes in grid for small groups
            subprocess.run([
                'tmux', 'split-window', '-h', '-t', f'{session_name}:0'
            ], check=True)
            subprocess.run([
                'tmux', 'split-window', '-v', '-t', f'{session_name}:0.0'
            ], check=True)
            subprocess.run([
                'tmux', 'split-window', '-v', '-t', f'{session_name}:0.1'
            ], check=True)
            
        else:
            # Tiled layout for larger groups
            subprocess.run([
                'tmux', 'split-window', '-h', '-t', f'{session_name}:0'
            ], check=True)
            subprocess.run([
                'tmux', 'split-window', '-v', '-t', f'{session_name}:0.0'
            ], check=True)
            subprocess.run([
                'tmux', 'split-window', '-v', '-t', f'{session_name}:0.1'
            ], check=True)
            subprocess.run([
                'tmux', 'split-window', '-h', '-t', f'{session_name}:0.2'
            ], check=True)
        
        # Apply pane synchronization if configured
        if config.tmux_config.get('synchronize_panes') == 'on':
            subprocess.run([
                'tmux', 'set-window-option', '-t', f'{session_name}:0',
                'synchronize-panes', 'on'
            ], check=True)
        
        # Send initialization commands to each pane
        self._send_initialization_commands(session_name, config, agent_count)
    
    def _send_initialization_commands(self, 
                                    session_name: str, 
                                    config: AIModeConfig, 
                                    agent_count: int):
        """Send initialization commands to all panes"""
        # Clear each pane and show welcome message
        for pane_idx in range(min(agent_count, 8)):  # Limit to 8 panes
            welcome_msg = f"""
🎀 Kawaii Collaboration Started! {config.icon}
─────────────────────────────────────
Mode: {config.kawaii_name}
Agents: {agent_count}
Theme: Hello Kitty (Maximum Cuteness!)

(òωó) Ready for amazing collaboration!
            """
            
            subprocess.run([
                'tmux', 'send-keys', '-t', f'{session_name}:0.{pane_idx}',
                'clear', 'Enter'
            ], check=True)
            
            subprocess.run([
                'tmux', 'send-keys', '-t', f'{session_name}:0.{pane_idx}',
                f'echo "{welcome_msg.strip()}"', 'Enter'
            ], check=True)
    
    def _display_success_message(self, 
                               session_name: str, 
                               config: AIModeConfig, 
                               parameters: Dict[str, str]):
        """Display kawaii success message"""
        success_message = f"""
🎀 Kawaii Collaboration Session Created! ♡
─────────────────────────────────────────
Session Name: {session_name}
Mode: {config.kawaii_name} {config.icon}
Agents: {parameters.get('agents', '2')}
Duration: {parameters.get('duration', '1 hour')}
Focus: {parameters.get('focus', 'collaboration')}

🎯 Ready for your kawaii adventure!
• Attach with: tmux attach -t {session_name}
• Switch panes with: Ctrl-b + arrow keys
• Toggle sync: Ctrl-b + S (if enabled)

💖 Session configured with maximum cuteness! (òωó)

Happy collaborating! ♡
        """
        print(success_message)
    
    def get_active_sessions(self) -> List[Dict]:
        """Get list of active collaboration sessions"""
        try:
            result = subprocess.run([
                'tmux', 'list-sessions', '-F', 
                '#{session_name} #{session_created} #{window_name}'
            ], capture_output=True, text=True, check=True)
            
            sessions = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split(' ', 2)
                    if len(parts) >= 3:
                        session_name = parts[0]
                        if session_name in self.active_sessions:
                            sessions.append({
                                'name': session_name,
                                'created': parts[1],
                                'window': parts[2],
                                'mode': self.active_sessions[session_name]['mode'],
                                'kawaii_level': 'MAXIMUM'
                            })
            
            return sessions
            
        except subprocess.CalledProcessError:
            return []
    
    def stop_collaboration_session(self, session_name: str) -> bool:
        """Stop a collaboration session"""
        try:
            subprocess.run(['tmux', 'kill-session', '-t', session_name], check=True)
            
            if session_name in self.active_sessions:
                del self.active_sessions[session_name]
            
            print(f"🎀 Collaboration session '{session_name}' ended gracefully! ♡")
            return True
            
        except subprocess.CalledProcessError:
            print(f"❌ Failed to stop session '{session_name}'")
            return False
    
    def get_session_info(self, session_name: str) -> Optional[Dict]:
        """Get detailed information about a collaboration session"""
        return self.active_sessions.get(session_name)
    
    def toggle_pane_sync(self, session_name: str) -> bool:
        """Toggle pane synchronization for a session"""
        try:
            subprocess.run([
                'tmux', 'set-window-option', '-t', f'{session_name}:0',
                'synchronize-panes'
            ], check=True)
            
            print(f"🔄 Pane synchronization toggled for '{session_name}'! (òωó)")
            return True
            
        except subprocess.CalledProcessError:
            print(f"❌ Failed to toggle pane sync for '{session_name}'")
            return False
    
    def export_session_template(self, 
                              mode: CollaborationMode, 
                              template_name: str) -> bool:
        """Export a session as a reusable template"""
        try:
            config = self.modes[mode]
            template_data = {
                'name': template_name,
                'mode': mode.value,
                'config': config.__dict__,
                'created_at': time.time(),
                'theme': 'hello_kitty',
                'kawaii_level': 'ULTIMATE'
            }
            
            template_file = f"templates/{template_name}.json"
            os.makedirs('templates', exist_ok=True)
            
            with open(template_file, 'w') as f:
                json.dump(template_data, f, indent=2)
            
            print(f"🎨 Template '{template_name}' exported successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Failed to export template: {e}")
            return False


# Integration with existing Hello Kitty terminal system
def integrate_with_hello_kitty_tmux():
    """Integrate with existing Hello Kitty tmux theme"""
    try:
        # Check if Hello Kitty tmux plugin is active
        result = subprocess.run([
            'tmux', 'show-options', '-g', '@hello_kitty_enabled'
        ], capture_output=True, text=True)
        
        if result.returncode == 0 and '1' in result.stdout:
            print("🎀 Hello Kitty tmux theme detected and active!")
            print("💖 Kawaii TUI will work perfectly with your existing setup! (òωó)")
            return True
        else:
            print("💡 Hello Kitty tmux theme not detected.")
            print("🎀 Kawaii TUI will work fine, but consider enabling Hello Kitty theme for maximum cuteness!")
            return False
            
    except subprocess.CalledProcessError:
        print("💡 Unable to detect tmux configuration.")
        print("🎀 Kawaii TUI will work with default settings! (òωó)")
        return False


# Example usage and testing
def demo_kawaii_ai_modes():
    """Demonstrate kawaii AI modes functionality"""
    print("🎀 Kawaii AI Modes Demo (òωó)")
    print("=" * 50)
    
    modes = KawaiiAIModes()
    
    # List all modes
    print("\n📋 Available Collaboration Modes:")
    for mode, kawaii_name, icon in modes.list_modes():
        print(f"  {icon} {kawaii_name} ({mode})")
    
    # Demo mode details
    print("\n🎭 Mode Details - Pair Programming:")
    pair_config = modes.get_mode_config(CollaborationMode.PAIR_PROGRAMMING)
    print(f"  Name: {pair_config.kawaii_name}")
    print(f"  Icon: {pair_config.icon}")
    print(f"  Description: {pair_config.description}")
    print("  Parameters:")
    for key, value in pair_config.parameters.items():
        print(f"    • {key}: {value}")
    
    # Check integration
    print("\n🔧 Hello Kitty Integration:")
    integrate_with_hello_kitty_tmux()
    
    print("\n💖 Demo complete! Ready for kawaii collaboration! ♡")


if __name__ == "__main__":
    demo_kawaii_ai_modes()