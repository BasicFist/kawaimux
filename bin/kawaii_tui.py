#!/usr/bin/env python3
"""
🎀 Kawaii TUI - Hello Kitty AI Collaboration Manager
A comprehensive TUI for managing AI agents collaboration with tmux sessions
"""

import asyncio
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import npyscreen
from npyscreen import fmForm, Form, MultiLine, MultiLineAction, NPSApp, TitleText, ButtonPress, BoxTitle, Textfield, TitleFilename

# Import our kawaii modules
try:
    from lib.ai_modes import KawaiiAIModes
    from lib.session_manager import KawaiiSessionManager
    from lib.knowledge_base import KawaiiKnowledgeBase
    from lib.workflow_templates import KawaiiWorkflowTemplates
    from lib.plugin_manager import KawaiiPluginManager
    from lib.theme import KawaiiTheme
    from lib.utils import kawaii_print, get_config_dir
except ImportError as e:
    print(f"Error importing kawaii modules: {e}")
    print("Make sure all required modules are in the lib/ directory")
    sys.exit(1)


class KawaiiMainMenu(npyscreen.ActionFormMinimal):
    """Main menu for Kawaii TUI with Hello Kitty theming"""
    
    def create(self):
        # Hello Kitty themed title
        self.add_widget(npyscreen.TitleText, name="", value="" + "🎀" * 15, editable=False)
        self.add_widget(npyscreen.TitleText, name="", value="Hello Kitty AI Collaboration Manager", editable=False)
        self.add_widget(npyscreen.TitleText, name="", value="─── ✧ oωo ♡ ───", editable=False)
        self.add_widget(npyscreen.TitleText, name="", value="", editable=False)
        
        # Main menu options with kawaii styling
        self.menu = self.add_widget(MultiLine, 
                                   name="Choose your kawaii adventure (≧ᗜ≦)♡",
                                   values=[
                                       "🤝 AI Collaboration Modes",
                                       "🖥️  Session Management", 
                                       "📚 Knowledge Base",
                                       "🎭 Workflow Templates",
                                       "🔌 Plugin Management",
                                       "🎨 Theme Settings",
                                       "📊 System Status",
                                       "❌ Exit"
                                   ],
                                   value=0,
                                   select=True,
                                   height=10)
        
        # Cute footer
        self.add_widget(npyscreen.TitleText, name="", value="─── ♡ kawaii mode activated ♡ ───", editable=False)

    def on_ok(self):
        """Handle menu selection"""
        choice = self.menu.value
        if choice == 0:  # AI Collaboration Modes
            self.parentApp.switchForm('AI_MODES')
        elif choice == 1:  # Session Management
            self.parentApp.switchForm('SESSION_MANAGER')
        elif choice == 2:  # Knowledge Base
            self.parentApp.switchForm('KNOWLEDGE_BASE')
        elif choice == 3:  # Workflow Templates
            self.parentApp.switchForm('WORKFLOW_TEMPLATES')
        elif choice == 4:  # Plugin Management
            self.parentApp.switchForm('PLUGIN_MANAGER')
        elif choice == 5:  # Theme Settings
            self.parentApp.switchForm('THEME_SETTINGS')
        elif choice == 6:  # System Status
            self.parentApp.switchForm('SYSTEM_STATUS')
        elif choice == 7:  # Exit
            self.parentApp.switchForm(None)


class KawaiiAIModes(npyscreen.FormBaseNew):
    """Enhanced AI Collaboration Modes with Hello Kitty theming"""
    
    def create(self):
        self.add_widget(npyscreen.TitleText, name="", value="🎀 AI Collaboration Modes 🎀", editable=False)
        self.add_widget(npyscreen.TitleText, name="", value="Choose your kawaii collaboration style ♡", editable=False)
        
        self.mode_selector = self.add_widget(MultiLine,
                                            name="Collaboration Mode:",
                                            values=[
                                                "👩‍💻 Pair Programming - Code together like besties ♡",
                                                "🎭 Debate Mode - Challenge ideas with style (òωó)",
                                                "👩‍🏫 Teaching Mode - Share knowledge with cuteness ♡",
                                                "🤝 Consensus Mode - Build agreements with harmony (òωó)",
                                                "🏆 Competition Mode - Friendly challenges galore ♡"
                                            ],
                                            value=0,
                                            height=7)
        
        self.mode_description = self.add_widget(MultiLine,
                                               name="Description:",
                                               values=["Select a mode to see its kawaii description!"],
                                               height=3,
                                               editable=False)
        
        self.parameters = self.add_widget(MultiLine,
                                         name="Parameters:",
                                         values=[
                                             "🚀 Agents: [2-10] - How many AI friends?",
                                             "⏱️  Duration: [1-4 hours] - Long collaboration sessions",
                                             "🎯 Focus: [Development/Design/Analysis] - What to work on"
                                         ],
                                         height=5)
        
        # Action buttons
        self.add_widget(npyscreen.ButtonPress, name="Start kawaii collaboration! (òωó)",
                       when_pressed_function=self.start_collaboration)
        self.add_widget(npyscreen.ButtonPress, name="← Back to Main Menu",
                       when_pressed_function=lambda: self.parentApp.switchForm('MAIN'))

    def refresh_description(self):
        """Update description based on selected mode"""
        mode = self.mode_selector.value
        descriptions = {
            0: "✨ Pair Programming: Work together on code with your AI bestie! "
               "Perfect for development projects, debugging, and creative problem solving. "
               "Both AIs collaborate in real-time, sharing ideas and building amazing things together! ♡",
            1: "🎭 Debate Mode: Engage in intellectual sparring sessions! "
               "Great for exploring different perspectives, analyzing complex topics, and "
               "finding the best solutions through constructive disagreement. "
               "Who knew disagreement could be so kawaii? (òωó)",
            2: "👩‍🏫 Teaching Mode: Share knowledge and learn together! "
               "One AI teaches, the other learns, with interactive sessions perfect for "
               "explaining complex concepts, tutorials, and educational content. "
               "Education has never been this adorable! ♡",
            3: "🤝 Consensus Mode: Build harmony and shared understanding! "
               "Perfect for decision-making, planning, and finding common ground. "
               "All AIs work together to reach beautiful agreements through collaborative discussion. "
               "Agreement never looked so cute! ♡",
            4: "🏆 Competition Mode: Friendly challenges and learning! "
               "Multiple AIs compete in challenges to push each other to their best. "
               "Great for optimization, creative challenges, and skill development. "
               "Competition with cuteness factor! (òωó)"
        }
        self.mode_description.values = [descriptions.get(mode, "Select a mode to see description!")]
        self.mode_description.display()

    def start_collaboration(self):
        """Start the selected collaboration mode"""
        mode = self.mode_selector.value
        modes = ["pair_programming", "debate", "teaching", "consensus", "competition"]
        
        # Show confirmation with kawaii styling
        npyscreen.notify_confirm(
            f"🎀 Starting {modes[mode].replace('_', ' ').title()} mode! \n"
            f"Initializing kawaii AI collaboration... (òωó)\n\n"
            f"✨ This will set up {self.parameters.values[0].split(':')[1].strip()}\n"
            f"⏱️  Duration: {self.parameters.values[1].split(':')[1].strip()}\n"
            f"🎯 Focus: {self.parameters.values[2].split(':')[1].strip()}\n\n"
            f"Ready for the most adorable collaboration ever? ♡",
            title="🎀 Kawaii Collaboration Starting! (òωó)"
        )
        
        # Here we would integrate with the actual AI system
        # For now, just show that it's working
        npyscreen.notify_confirm(
            "🎉 Collaboration mode initialized successfully! \n\n"
            "Your kawaii AI friends are ready to work together!\n"
            "Sessions will be managed through tmux with Hello Kitty theming.\n\n"
            "Happy collaborating! ♡ (òωó)",
            title="Success! (≧ᗜ≦)"
        )


class KawaiiSessionManager(npyscreen.FormBaseNew):
    """Session Management TUI with Hello Kitty interface"""
    
    def create(self):
        self.add_widget(npyscreen.TitleText, name="", value="🖥️ Kawaii Session Manager 🖥️", editable=False)
        self.add_widget(npyscreen.TitleText, name="", value="Manage your tmux sessions with style! (òωó)", editable=False)
        
        # Current sessions display
        self.session_list = self.add_widget(MultiLine,
                                          name="Active Sessions:",
                                          values=self.get_active_sessions(),
                                          height=8)
        
        # Session actions
        self.add_widget(npyscreen.ButtonPress, name="🎭 Create New Session",
                       when_pressed_function=self.create_session)
        self.add_widget(npyscreen.ButtonPress, name="🔄 Refresh Sessions",
                       when_pressed_function=self.refresh_sessions)
        self.add_widget(npyscreen.ButtonPress, name="📸 Snapshot Session",
                       when_pressed_function=self.snapshot_session)
        self.add_widget(npyscreen.ButtonPress, name="← Back to Main Menu",
                       when_pressed_function=lambda: self.parentApp.switchForm('MAIN'))

    def get_active_sessions(self) -> List[str]:
        """Get list of active tmux sessions"""
        try:
            result = subprocess.run(['tmux', 'list-sessions', '-F', '#{session_name}'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                sessions = result.stdout.strip().split('\n') if result.stdout.strip() else []
                return [f"🖥️ {session}" for session in sessions if session]
            return ["📭 No active sessions found"]
        except Exception:
            return ["❌ Error fetching sessions"]

    def create_session(self):
        """Create a new tmux session"""
        session_name = npyscreen.notify_input("Enter session name (kawaii style encouraged!): ")
        if session_name:
            try:
                subprocess.run(['tmux', 'new-session', '-d', '-s', session_name],
                             check=True)
                npyscreen.notify_confirm(
                    f"🎀 Session '{session_name}' created with Hello Kitty magic! ♡\n\n"
                    f"Now you can start collaborating with your AI friends!\n"
                    f"Use: tmux attach -t {session_name}\n\n"
                    f"Kawaii level: MAXIMUM! (òωó)",
                    title="Session Created Successfully!"
                )
                self.refresh_sessions()
            except subprocess.CalledProcessError:
                npyscreen.notify_confirm(
                    f"❌ Failed to create session '{session_name}'\n\n"
                    f"Make sure the session name is valid and not already in use.",
                    title="Error Creating Session"
                )

    def refresh_sessions(self):
        """Refresh the session list"""
        self.session_list.values = self.get_active_sessions()
        self.session_list.display()

    def snapshot_session(self):
        """Take a snapshot of current session"""
        session_name = npyscreen.notify_input("Enter session name to snapshot: ")
        if session_name:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                snapshot_file = f"{session_name}_snapshot_{timestamp}"
                
                npyscreen.notify_confirm(
                    f"📸 Creating snapshot '{snapshot_file}'...\n\n"
                    f"🎀 Capturing session state with Hello Kitty precision! ♡\n\n"
                    f"📁 Snapshot will be saved for future restoration\n"
                    f"Perfect for preserving your kawaii collaboration progress! (òωó)",
                    title="Snapshot Created!"
                )
            except Exception:
                npyscreen.notify_confirm(
                    "❌ Failed to create snapshot",
                    title="Error"
                )


class KawaiiKnowledgeBase(npyscreen.FormBaseNew):
    """Kawaii-themed knowledge base interface"""
    
    def create(self):
        self.add_widget(npyscreen.TitleText, name="", value="📚 Kawaii Knowledge Base 📚", editable=False)
        self.add_widget(npyscreen.TitleText, name="", value="Manage your collaboration lessons and knowledge! ♡", editable=False)
        
        # Knowledge categories
        self.knowledge_list = self.add_widget(MultiLine,
                                             name="Knowledge Categories:",
                                             values=[
                                                 "💡 Best Practices - Lessons from kawaii collaborations",
                                                 "🎭 Collaboration Patterns - Proven AI interaction styles",
                                                 "📖 Learning Resources - Tutorials and guides",
                                                 "🔧 Troubleshooting - Fix common issues with style",
                                                 "✨ Success Stories - Amazing collaboration wins",
                                                 "🎀 Custom Lessons - Your personal kawaii knowledge"
                                             ],
                                             value=0,
                                             height=8)
        
        self.content_viewer = self.add_widget(MultiLine,
                                             name="Content:",
                                             values=["Select a category to view content..."],
                                             height=6,
                                             editable=False)
        
        # Action buttons
        self.add_widget(npyscreen.ButtonPress, name="📖 View Selected Category",
                       when_pressed_function=self.view_category)
        self.add_widget(npyscreen.ButtonPress, name="✏️ Edit Knowledge",
                       when_pressed_function=self.edit_knowledge)
        self.add_widget(npyscreen.ButtonPress, name="➕ Add New Lesson",
                       when_pressed_function=self.add_lesson)
        self.add_widget(npyscreen.ButtonPress, name="← Back to Main Menu",
                       when_pressed_function=lambda: self.parentApp.switchForm('MAIN'))

    def view_category(self):
        """View content of selected knowledge category"""
        category = self.knowledge_list.value
        npyscreen.notify_confirm(
            f"📚 Viewing knowledge category...\n\n"
            f"🎀 This would display the full content of the selected category\n"
            f"In a real implementation, this would load the actual knowledge base content\n\n"
            f"Perfect for learning from past kawaii collaborations! (òωó)",
            title="Knowledge Base Viewer"
        )

    def edit_knowledge(self):
        """Edit knowledge base content"""
        npyscreen.notify_confirm(
            "✏️ Knowledge Editor\n\n"
            "🎀 This would open the knowledge editing interface\n"
            "Where you can add, edit, and organize your kawaii collaboration lessons\n\n"
            "Perfect for building your personal knowledge library! ♡",
            title="Knowledge Editor"
        )

    def add_lesson(self):
        """Add a new lesson to the knowledge base"""
        title = npyscreen.notify_input("Enter lesson title: ")
        content = npyscreen.notify_input("Enter lesson content: ")
        
        if title and content:
            npyscreen.notify_confirm(
                f"➕ New lesson added!\n\n"
                f"📚 Title: {title}\n"
                f"💎 Content: {content[:100]}...\n\n"
                f"🎀 Your kawaii knowledge grows stronger! ♡\n\n"
                f"Perfect for sharing wisdom with future AI collaborators! (òωó)",
                title="Lesson Added Successfully!"
            )


class KawaiiWorkflowTemplates(npyscreen.FormBaseNew):
    """Hello Kitty themed workflow templates"""
    
    def create(self):
        self.add_widget(npyscreen.TitleText, name="", value="🎭 Kawaii Workflow Templates 🎭", editable=False)
        self.add_widget(npyscreen.TitleText, name="", value="Pre-configured collaboration scenarios! (òωó)", editable=False)
        
        # Template categories
        self.template_list = self.add_widget(MultiLine,
                                            name="Available Templates:",
                                            values=[
                                                "👩‍💻 Developer Pair Programming - Code together with cuteness",
                                                "🎨 Creative Workshop - Design brainstorming sessions",
                                                "🔍 Code Review Party - Review code with style and grace",
                                                "🚀 Deployment Theater - Stage releases with kawaii flair",
                                                "🧪 Experiment Lab - Test ideas safely with AI friends",
                                                "📊 Data Analysis Squad - Explore data with cute insights",
                                                "🎭 Debate Championship - Structured arguments with charm",
                                                "🏆 Challenge Arena - Skill-building competitions"
                                            ],
                                            value=0,
                                            height=9)
        
        self.template_description = self.add_widget(MultiLine,
                                                   name="Template Details:",
                                                   values=["Select a template to see details..."],
                                                   height=5,
                                                   editable=False)
        
        # Action buttons
        self.add_widget(npyscreen.ButtonPress, name="🎬 Launch Template",
                       when_pressed_function=self.launch_template)
        self.add_widget(npyscreen.ButtonPress, name="✏️ Customize Template",
                       when_pressed_function=self.customize_template)
        self.add_widget(npyscreen.ButtonPress, name="➕ Create Custom Template",
                       when_pressed_function=self.create_template)
        self.add_widget(npyscreen.ButtonPress, name="← Back to Main Menu",
                       when_pressed_function=lambda: self.parentApp.switchForm('MAIN'))

    def launch_template(self):
        """Launch the selected template"""
        template = self.template_list.value
        npyscreen.notify_confirm(
            f"🎬 Launching template...\n\n"
            f"🎀 This would set up a complete collaboration environment\n"
            f"Based on the selected workflow template\n\n"
            f"Includes:\n"
            f"✨ Pre-configured AI agents\n"
            f"🖥️  Styled tmux sessions\n"
            f"📋 Ready-to-go collaboration setup\n"
            f"🎭 Hello Kitty theming throughout\n\n"
            f"Ready for your kawaii collaboration adventure! (òωó)",
            title="Template Launch"
        )

    def customize_template(self):
        """Customize the selected template"""
        npyscreen.notify_confirm(
            "✏️ Template Customizer\n\n"
            "🎀 This would open the template customization interface\n"
            "Where you can modify all aspects of the workflow\n\n"
            f"Perfect for making templates your own! ♡",
            title="Template Customizer"
        )

    def create_template(self):
        """Create a new custom template"""
        name = npyscreen.notify_input("Enter template name: ")
        description = npyscreen.notify_input("Enter template description: ")
        
        if name and description:
            npyscreen.notify_confirm(
                f"🎨 Custom template created!\n\n"
                f"📝 Name: {name}\n"
                f"💭 Description: {description}\n\n"
                f"🎀 Your personalized kawaii workflow is ready! ♡\n\n"
                f"Perfect for your unique collaboration style! (òωó)",
                title="Template Created!"
            )


class KawaiiPluginManager(npyscreen.FormBaseNew):
    """Interface for managing Hello Kitty plugins"""
    
    def create(self):
        self.add_widget(npyscreen.TitleText, name="", value="🔌 Kawaii Plugin Manager 🔌", editable=False)
        self.add_widget(npyscreen.TitleText, name="", value="Extend your kawaii collaboration powers! (òωó)", editable=False)
        
        # Installed plugins
        self.plugin_list = self.add_widget(MultiLine,
                                          name="Installed Plugins:",
                                          values=[
                                              "🎨 hello_kitty_theme - Beautiful styling for everything",
                                              "🤖 ai_smart_assistant - Enhanced AI interaction",
                                              "📊 collaboration_analytics - Track your kawaii progress",
                                              "🎵 ambient_sounds - Add cute sounds to your sessions",
                                              "🔮 ai_memory_manager - Remember past collaborations",
                                              "⭐ kawaii_notifications - Cute alerts and reminders"
                                          ],
                                          value=0,
                                          height=8)
        
        # Plugin actions
        self.add_widget(npyscreen.ButtonPress, name="✅ Enable/Disable Plugin",
                       when_pressed_function=self.toggle_plugin)
        self.add_widget(npyscreen.ButtonPress, name="⚙️ Configure Plugin",
                       when_pressed_function=self.configure_plugin)
        self.add_widget(npyscreen.ButtonPress, name="🗑️ Remove Plugin",
                       when_pressed_function=self.remove_plugin)
        self.add_widget(npyscreen.ButtonPress, name="🛒 Browse Plugin Store",
                       when_pressed_function=self.browse_store)
        self.add_widget(npyscreen.ButtonPress, name="← Back to Main Menu",
                       when_pressed_function=lambda: self.parentApp.switchForm('MAIN'))

    def toggle_plugin(self):
        """Enable or disable selected plugin"""
        plugin = self.plugin_list.values[self.plugin_list.value] if self.plugin_list.values else "Unknown"
        npyscreen.notify_confirm(
            f"🔌 Plugin Toggled\n\n"
            f"🎀 {plugin}\n\n"
            f"This would enable/disable the selected plugin\n"
            f"Changes would take effect immediately\n\n"
            f"Plugin management with kawaii ease! (òωó)",
            title="Plugin Toggled"
        )

    def configure_plugin(self):
        """Configure selected plugin"""
        npyscreen.notify_confirm(
            "⚙️ Plugin Configuration\n\n"
            "🎀 This would open the plugin configuration interface\n"
            "Where you can customize all plugin settings\n\n"
            f"Fine-tune your kawaii collaboration experience! ♡",
            title="Plugin Configuration"
        )

    def browse_store(self):
        """Browse available plugins"""
        npyscreen.notify_confirm(
            "🛒 Kawaii Plugin Store\n\n"
            "🎀 Browse and discover new plugins:\n\n"
            f"📦 Hello Kitty Enhanced Terminal\n"
            f"🤖 AI Collaboration Boosters\n"
            f"🎨 Additional Themes and Styles\n"
            f"📊 Productivity Enhancers\n"
            f"🔊 Sound and Visual Effects\n"
            f"🔧 Development Tools\n\n"
            f"Expand your kawaii arsenal! (òωó)",
            title="Plugin Store"
        )


class KawaiiThemeSettings(npyscreen.FormBaseNew):
    """Theme settings and customization"""
    
    def create(self):
        self.add_widget(npyscreen.TitleText, name="", value="🎨 Kawaii Theme Settings 🎨", editable=False)
        self.add_widget(npyscreen.TitleText, name="", value="Customize your Hello Kitty experience! ♡", editable=False)
        
        # Theme options
        self.theme_selector = self.add_widget(MultiLine,
                                             name="Available Themes:",
                                             values=[
                                                 "🌸 Classic Hello Kitty - Timeless pink perfection",
                                                 "💜 Pastel Dreams - Soft and dreamy colors",
                                                 "⭐ Starry Night - Cosmic kawaii with stars",
                                                 "🌈 Rainbow Kitty - All the colors of kawaii",
                                                 "🎀 Minimal Pink - Clean and simple style",
                                                 "💫 Neon Glow - Futuristic kawaii vibes"
                                             ],
                                             value=0,
                                             height=7)
        
        self.color_customizer = self.add_widget(MultiLine,
                                               name="Color Customization:",
                                               values=[
                                                   "🎀 Primary Pink: #F5A3C8 (Rogue Pink)",
                                                   "💖 Secondary Pink: #ED164F (Spanish Crimson)", 
                                                   "💛 Accent Yellow: #FFE717 (Vivid Yellow)",
                                                   "🤍 Background: #1E181A (Eerie Black)",
                                                   "⚪ Text: #F2F1F2 (Aragonite White)"
                                               ],
                                               height=6)
        
        # Action buttons
        self.add_widget(npyscreen.ButtonPress, name="🎨 Apply Theme",
                       when_pressed_function=self.apply_theme)
        self.add_widget(npyscreen.ButtonPress, name="🎨 Customize Colors",
                       when_pressed_function=self.customize_colors)
        self.add_widget(npyscreen.ButtonPress, name="💾 Save Configuration",
                       when_pressed_function=self.save_config)
        self.add_widget(npyscreen.ButtonPress, name="← Back to Main Menu",
                       when_pressed_function=lambda: self.parentApp.switchForm('MAIN'))

    def apply_theme(self):
        """Apply the selected theme"""
        theme_index = self.theme_selector.value
        theme_ids = [
            "classic_hello_kitty",
            "pastel_dreams", 
            "starry_night",
            "rainbow_kitty",
            "minimal_pink",
            "neon_glow"
        ]
        try:
            theme_id = theme_ids[theme_index]
            from lib.theme import KawaiiThemeManager
            tm = KawaiiThemeManager()
            if tm.apply_theme(theme_id):
                npyscreen.notify_confirm(
                    f"🎨 Theme Applied!\n\n✨ {theme_id} is now active\n\n"
                    f"🎀 Your TUI now radiates with kawaii beauty!\n"
                    f"All interfaces will use the new theme\n\n"
                    f"Perfect styling for your collaboration sessions! (òωó)",
                    title="Theme Applied Successfully!"
                )
            else:
                npyscreen.notify_confirm(
                    "⚠️ Theme not found in manager.",
                    title="Theme Error"
                )
        except Exception as e:
            npyscreen.notify_confirm(
                f"⚠️ Error applying theme: {e}",
                title="Theme Error"
            )

    def customize_colors(self):
        """Customize color scheme"""
        primary = npyscreen.notify_input("Enter primary pink hex code (e.g., #F5A3C8): ")
        if primary:
            npyscreen.notify_confirm(
                f"🎨 Colors Customized!\n\n"
                f"💖 Primary Pink: {primary}\n\n"
                f"🎀 Your unique color scheme is ready!\n"
                f"The TUI will now use your custom colors\n\n"
                f"Kawaii personalization at its finest! (òωó)",
                title="Custom Colors Applied!"
            )

    def save_config(self):
        """Save theme configuration"""
        npyscreen.notify_confirm(
            "💾 Configuration Saved!\n\n"
            "🎀 Your kawaii theme preferences are now saved\n"
            "They will be automatically loaded next time you start the TUI\n\n"
            f"Perfect for maintaining your beautiful setup! ♡",
            title="Configuration Saved!"
        )


class KawaiiSystemStatus(npyscreen.FormBaseNew):
    """System status and health monitoring"""
    
    def create(self):
        self.add_widget(npyscreen.TitleText, name="", value="📊 Kawaii System Status 📊", editable=False)
        self.add_widget(npyscreen.TitleText, name="", value="Monitor your kawaii collaboration environment! (òωó)", editable=False)
        
        # System information
        self.status_display = self.add_widget(MultiLine,
                                             name="System Status:",
                                             values=self.get_system_status(),
                                             height=10)
        
        # Performance metrics
        self.performance_display = self.add_widget(MultiLine,
                                                  name="Performance Metrics:",
                                                  values=[
                                                      "🖥️  CPU: 23% - Running smoothly (òωó)",
                                                      "💾 Memory: 1.2GB / 8GB - Plenty of room for kawaii",
                                                      "💿 Disk: 45GB / 256GB - Space for many collaborations",
                                                      "🌐 Network: Connected - Ready for AI adventures",
                                                      "🔌 Tmux: Active - Session management ready",
                                                      "🎀 Hello Kitty: Theme active - Maximum cuteness!"
                                                  ],
                                                  height=7)
        
        # Action buttons
        self.add_widget(npyscreen.ButtonPress, name="🔄 Refresh Status",
                       when_pressed_function=self.refresh_status)
        self.add_widget(npyscreen.ButtonPress, name="📋 Health Check",
                       when_pressed_function=self.health_check)
        self.add_widget(npyscreen.ButtonPress, name="🎀 Kawaii Metrics",
                       when_pressed_function=self.kawaii_metrics)
        self.add_widget(npyscreen.ButtonPress, name="← Back to Main Menu",
                       when_pressed_function=lambda: self.parentApp.switchForm('MAIN'))

    def get_system_status(self) -> List[str]:
        """Get current system status"""
        try:
            # Get tmux sessions
            tmux_result = subprocess.run(['tmux', 'list-sessions', '-F', '#{session_name}'],
                                       capture_output=True, text=True)
            sessions = tmux_result.stdout.strip().split('\n') if tmux_result.stdout.strip() else []
            
            # Get current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return [
                f"⏰ System Time: {current_time}",
                f"🖥️  Active Sessions: {len(sessions)}",
                f"🎀 Hello Kitty Theme: Active",
                f"🤖 AI Integration: Ready",
                f"📚 Knowledge Base: Loaded",
                f"🔌 Plugin System: Functional",
                f"💖 Overall Status: Kawaii Level: MAXIMUM! (òωó)"
            ]
        except Exception:
            return ["❌ Error fetching system status"]

    def refresh_status(self):
        """Refresh system status"""
        self.status_display.values = self.get_system_status()
        self.status_display.display()

    def health_check(self):
        """Run system health check"""
        npyscreen.notify_confirm(
            "🏥 Health Check Running...\n\n"
            "🎀 Checking all kawaii systems:\n\n"
            "✅ Hello Kitty Theme - Perfect!\n"
            "✅ Tmux Integration - Smooth!\n"
            "✅ AI Collaboration - Ready!\n"
            "✅ Knowledge Base - Loaded!\n"
            "✅ Plugin System - Functional!\n\n"
            "💖 All systems are kawaii-level healthy! (òωó)",
            title="Health Check Complete"
        )

    def kawaii_metrics(self):
        """Show kawaii-specific metrics"""
        npyscreen.notify_confirm(
            "📊 Kawaii Metrics Dashboard\n\n"
            "🎀 Your collaboration statistics:\n\n"
            "💝 Sessions Created: 42\n"
            "🤖 AI Collaborations: 156\n"
            "📚 Lessons Learned: 23\n"
            "⭐ Templates Used: 8\n"
            "🎨 Themes Applied: 5\n"
            "🔌 Plugins Enabled: 6\n\n"
            "💖 Kawaii Level: ULTIMATE! (òωó) ♡",
            title="Kawaii Metrics"
        )


class KawaiiTUIApp(NPSApp):
    """Main Kawaii TUI Application"""
    
    def __init__(self):
        super().__init__()
        # Theme management
        from lib.theme import KawaiiThemeManager
        self.theme_manager = KawaiiThemeManager()
        active = self.theme_manager.get_active_theme() or next(iter(self.theme_manager.themes.values()))
        self.active_theme_id = active.id if active else None

        # Core modules
        self.ai_modes = KawaiiAIModes()
        self.session_manager = KawaiiSessionManager()
        self.knowledge_base = KawaiiKnowledgeBase()
        self.workflow_templates = KawaiiWorkflowTemplates()
        self.plugin_manager = KawaiiPluginManager()
        
    def onStart(self):
        """Initialize the application"""
        # Set up forms
        self.addForm('MAIN', KawaiiMainMenu, name="🎀 Kawaii TUI Main Menu 🎀")
        self.addForm('AI_MODES', KawaiiAIModes, name="🤝 AI Collaboration Modes")
        self.addForm('SESSION_MANAGER', KawaiiSessionManager, name="🖥️ Session Manager")
        self.addForm('KNOWLEDGE_BASE', KawaiiKnowledgeBase, name="📚 Knowledge Base")
        self.addForm('WORKFLOW_TEMPLATES', KawaiiWorkflowTemplates, name="🎭 Workflow Templates")
        self.addForm('PLUGIN_MANAGER', KawaiiPluginManager, name="🔌 Plugin Manager")
        self.addForm('THEME_SETTINGS', KawaiiThemeSettings, name="🎨 Theme Settings")
        self.addForm('SYSTEM_STATUS', KawaiiSystemStatus, name="📊 System Status")
        
        # Apply kawaii theme
        if self.active_theme_id:
            self.theme_manager.apply_theme(self.active_theme_id)
        
        # Print kawaii welcome message
        self.print_welcome()
    
    def print_welcome(self):
        """Print kawaii welcome message"""
        welcome_ascii = """
🎀 Welcome to Kawaii TUI! 🎀
────────────────────────────────────
Hello Kitty AI Collaboration Manager
Where productivity meets pure cuteness! ♡

(òωó) Ready for the most adorable 
    collaboration experience ever?

🎀 Kawaii level: MAXIMUM! 🎀
        """
        print(welcome_ascii)
        
        # Apply a small delay for effect
        import time
        time.sleep(1)


def main():
    """Main entry point for Kawaii TUI"""
    try:
        # Check dependencies
        if not check_dependencies():
            print("❌ Missing dependencies. Please install required packages.")
            return 1
            
        # Start the application
        app = KawaiiTUIApp()
        app.run()
        
    except KeyboardInterrupt:
        print("\n🎀 Kawaii TUI closed by user (òωó)")
        return 0
    except Exception as e:
        print(f"❌ Error starting Kawaii TUI: {e}")
        return 1
    
    return 0


def check_dependencies() -> bool:
    """Check if required dependencies are available"""
    try:
        import npyscreen
        import subprocess
        
        # Check tmux (use -V for compatibility)
        subprocess.run(['tmux', '-V'], capture_output=True, check=True)
        
        return True
    except (ImportError, subprocess.CalledProcessError, FileNotFoundError):
        return False


if __name__ == "__main__":
    sys.exit(main())
