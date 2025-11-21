# 🎀 Kawaii TUI Quick Reference Guide

## 🚀 Essential Commands

### Quick Start
```bash
# Launch interactive TUI (most common)
kawaii-tui

# Run system health check
kawaii-tui --health

# Run full demonstration
kawaii-tui --demo
```

### AI Collaboration Modes
```bash
# Pair Programming (2 agents)
kawaii-tui --mode pair --session my_project

# Debate Mode (3-4 agents)
kawaii-tui --mode debate --agents 4 --duration 1.5

# Teaching Mode (3-6 agents)
kawaii-tui --mode teaching --agents 5 --duration 2.0

# Consensus Mode (3-5 agents)
kawaii-tui --mode consensus --agents 4 --duration 1.0

# Competition Mode (2-6 agents)
kawaii-tui --mode competition --agents 3 --duration 2.5
```

### Session Management
```bash
# Create named session
tmux new-session -d -s kawaii_project

# Attach to session
tmux attach -t kawaii_project

# List all sessions
kawaii-tui --list sessions

# Switch sessions in tmux
tmux switch-client -t kawaii_project

# Kill session
tmux kill-session -t kawaii_project
```

### Theme Management
```bash
# Apply themes
kawaii-tui --theme classic    # Classic Hello Kitty
kawaii-tui --theme pastel     # Pastel Dreams
kawaii-tui --theme starry     # Starry Night
kawaii-tui --theme rainbow    # Rainbow Kitty
kawaii-tui --theme minimal    # Minimal Pink
kawaii-tui --theme neon       # Neon Glow

# List available themes
kawaii-tui --list themes
```

### System Information
```bash
# List all components
kawaii-tui --list modes       # Collaboration modes
kawaii-tui --list templates   # Workflow templates
kawaii-tui --list plugins     # Available plugins
kawaii-tui --list sessions    # Active sessions

# Debug and verbose output
kawaii-tui --verbose
```

## 🎭 Workflow Template Quick Start

### Developer Pair Programming
1. **Setup** (5 min): Hello Kitty environment setup
2. **Planning** (20 min): Project scope and architecture
3. **Coding Sprint** (2 hours): Driver/navigator rotation
4. **Code Review** (30 min): Quality assurance
5. **Celebration** (10 min): Success acknowledgment

### Creative Workshop
1. **Warm-up** (10 min): Creative mindset activation
2. **Idea Storm** (30 min): Free-flowing brainstorming
3. **Evaluation** (25 min): Constructive discussion
4. **Development** (45 min): Concept refinement

### Learning Circle
1. **Assessment** (15 min): Knowledge level evaluation
2. **Teaching** (45 min): Structured knowledge transfer
3. **Practice** (40 min): Interactive skill development
4. **Validation** (20 min): Understanding verification
5. **Reflection** (10 min): Learning consolidation

## 🔧 Configuration

### Quick Config Changes
```bash
# Edit configuration file
nano ~/.kawaii_config/kawaii_config.json

# Common settings:
{
  "collaboration": {
    "default_agents": 2,
    "default_duration_hours": 2,
    "auto_save_sessions": true
  },
  "theme": {
    "name": "classic_hello_kitty",
    "kawaii_level": "MAXIMUM"
  }
}
```

### Environment Variables
```bash
# Add to ~/.bashrc or ~/.zshrc
export KAWAII_THEME_NAME="classic_hello_kitty"
export KAWAII_ANIMATIONS=true
export KAWAII_LOG_LEVEL=INFO
```

## 📚 Keyboard Shortcuts (In TUI)

### Navigation
- **↑↓** - Navigate menu items
- **Enter** - Select/confirm
- **Esc** - Cancel/go back
- **q** - Quit current screen

### Tmux Shortcuts (In Sessions)
- **Ctrl+b d** - Detach from session
- **Ctrl+b c** - Create new window
- **Ctrl+b n** - Next window
- **Ctrl+b p** - Previous window
- **Ctrl+b ↑↓←→** - Navigate panes
- **Ctrl+b z** - Toggle pane zoom

## 🎀 Kawaii Shortcuts

### In Interactive TUI
- **1** - AI Collaboration Modes
- **2** - Session Management  
- **3** - Knowledge Base
- **4** - Workflow Templates
- **5** - Plugin Management
- **6** - Theme Settings
- **7** - System Status
- **0** - Exit

## 🔌 Plugin Quick Commands

### Enable/Disable Plugins
```bash
# Via TUI: Navigate to Plugin Management
# Or direct tmux commands:
tmux send-keys -t session_name "kawaii-tui --list plugins" Enter
```

### Popular Plugins
- **hello_kitty_theme** - Enhanced styling
- **ai_smart_assistant** - Better AI interaction
- **collaboration_analytics** - Progress tracking
- **ambient_kawaii_sounds** - Cute audio
- **ai_memory_manager** - Session memory
- **kawaii_notifications** - Adorable alerts

## 🏥 Troubleshooting Quick Fixes

### Session Issues
```bash
# List sessions
tmux list-sessions

# Force detach all clients
tmux kill-session -t session_name

# Check tmux version
tmux -V
```

### Theme Issues
```bash
# Reapply theme
kawaii-tui --theme classic

# Check terminal colors
echo $COLORTERM

# Reset to defaults
rm ~/.kawaii_config/kawaii_config.json
```

### Permission Issues
```bash
# Make executable
chmod +x ~/.local/bin/kawaii-tui

# Or use Python directly
python3 ~/.local/bin/kawaii-tui
```

### Performance Issues
```bash
# Check system resources
htop

# Clean cache
rm -rf ~/.kawaii_cache/*

# Reduce agent count in complex sessions
kawaii-tui --mode pair --agents 2  # Instead of 6+
```

## 💖 Daily Kawaii Workflow

### Morning Routine
```bash
# 1. Launch Kawaii TUI
kawaii-tui

# 2. Check system health
kawaii-tui --health

# 3. Review yesterday's sessions
kawaii-tui --list sessions

# 4. Start fresh collaboration
kawaii-tui --mode pair
```

### Project Collaboration
```bash
# 1. Create project session
kawaii-tui --mode pair --session my_project --agents 2

# 2. Use workflow template
kawaii-tui --list templates  # Choose appropriate template

# 3. Monitor progress
tmux attach -t my_project

# 4. Take snapshots
# In TUI: Session Management → Snapshot Session
```

### End of Day
```bash
# 1. Save current session
tmux send-keys -t session_name "kawaii-save-session my_session" Enter

# 2. Detach gracefully
tmux send-keys -t session_name C-b d

# 3. Review progress
kawaii-tui --list sessions

# 4. Backup if needed
kawaii-tui --backup  # If backup plugin enabled
```

## 🎨 Theme Switching

### Theme Quick Switch
```bash
# Quick theme changes
kawaii-tui --theme classic   # Default Hello Kitty
kawaii-tui --theme pastel    # Soft pastels
kawaii-tui --theme starry    # Cosmic theme
kawaii-tui --theme rainbow   # Colorful
kawaii-tui --theme minimal   # Clean
kawaii-tui --theme neon      # Futuristic
```

### Custom Theme Creation
```bash
# Via TUI: Navigate to Theme Settings
# Or create programmatically:
python3 -c "
from lib.theme import KawaiiThemeManager
tm = KawaiiThemeManager()
tm.create_custom_theme(
    'My Theme', 'Description', 
    'pastel', 
    {'primary': '#FF69B4', 'secondary': '#FFB6C1'}
)
"
```

## 📊 Monitoring and Analytics

### Real-time Monitoring
```bash
# System status
kawaii-tui --health

# Session analytics
kawaii-tui --list sessions  # View usage stats

# Plugin usage
kawaii-tui --list plugins   # See active plugins
```

### Performance Tips
- Use 2-3 agents for best performance
- Regular session cleanup
- Enable auto-save for important work
- Monitor system resources

## 🎯 Best Practices

### Session Management
1. **Use descriptive names**: `project_alpha_dev`, `client_meeting_2024`
2. **Regular snapshots**: Save progress frequently
3. **Template usage**: Start with workflow templates
4. **Proper detachment**: Always use `Ctrl+b d`

### Collaboration Success
1. **Clear objectives**: Define goals before starting
2. **Appropriate mode**: Choose right collaboration style
3. **Manageable duration**: 1-3 hours optimal
4. **Positive communication**: Maintain kawaii energy!

### Knowledge Management
1. **Regular updates**: Add lessons after each session
2. **Searchable tags**: Use consistent tagging
3. **Success documentation**: Record wins and learnings
4. **Template creation**: Capture reusable patterns

## 🌟 Kawaii Level Achievements

### Kawaii Apprentice
- [ ] Install Kawaii TUI
- [ ] Run health check
- [ ] Launch interactive TUI
- [ ] Try first collaboration mode

### Kawaii Practitioner  
- [ ] Create custom session
- [ ] Apply different themes
- [ ] Use workflow templates
- [ ] Add knowledge to base

### Kawaii Master
- [ ] Create custom workflow
- [ ] Build custom plugin
- [ ] Design custom theme
- [ ] Help others with Kawaii TUI

### Kawaii Guru
- [ ] Contribute to project
- [ ] Create comprehensive tutorials
- [ ] Mentor new kawaii users
- [ ] Achieve maximum kawaii level!

---

## 💕 Remember

**Every command is better with kawaii! (òωó) ♡**

*Need help? Run `kawaii-tui --demo` for a complete walkthrough!*

---

🎀 **Kawaii TUI - Where productivity meets pure cuteness!** 🎀