# 🎀 Kawaii TUI Makefile
# Hello Kitty AI Collaboration Manager - Build and Management

.PHONY: help install demo health test clean uninstall demo-all

# Default target
help:
	@echo "🎀 Kawaii TUI - Makefile Commands"
	@echo "================================="
	@echo ""
	@echo "📋 Available Commands:"
	@echo "  make install     - Install Kawaii TUI system"
	@echo "  make demo        - Run quick demonstration"
	@echo "  make demo-all    - Run complete demo suite"
	@echo "  make health      - Run system health check"
	@echo "  make test        - Test installation"
	@echo "  make clean       - Clean temporary files"
	@echo "  make uninstall   - Remove Kawaii TUI"
	@echo "  make theme       - Apply Hello Kitty theme"
	@echo "  make session     - Create test session"
	@echo "  make help        - Show this help"
	@echo ""
	@echo "💖 Quick Start:"
	@echo "  1. make install"
	@echo "  2. make demo"
	@echo "  3. make health"
	@echo ""
	@echo "🎀 Kawaii level: MAXIMUM! (òωó)"

# Install Kawaii TUI
install:
	@echo "🎀 Installing Kawaii TUI..."
	chmod +x install.sh
	./install.sh

# Quick demonstration
demo:
	@echo "🎭 Running Kawaii TUI Quick Demo..."
	@if [ -f "bin/kawaii_tui" ]; then \
		python3 bin/kawaii_tui --demo; \
	elif [ -x "bin/kawaii_tui" ]; then \
		./bin/kawaii_tui --demo; \
	else \
		echo "❌ Kawaii TUI not found. Run 'make install' first."; \
	fi

# Complete demonstration
demo-all:
	@echo "🎉 Running Complete Kawaii TUI Demo Suite..."
	@echo ""
	@echo "📋 This will demonstrate:"
	@echo "  • AI Collaboration Modes"
	@echo "  • Session Management"
	@echo "  • Knowledge Base"
	@echo "  • Workflow Templates"
	@echo "  • Plugin Management"
	@echo "  • Theme System"
	@echo "  • Utility Functions"
	@echo ""
	@if [ -f "bin/kawaii_tui" ]; then \
		python3 bin/kawaii_tui --demo; \
	elif [ -x "bin/kawaii_tui" ]; then \
		./bin/kawaii_tui --demo; \
	else \
		echo "❌ Kawaii TUI not found. Run 'make install' first."; \
	fi

# System health check
health:
	@echo "🏥 Running Kawaii TUI Health Check..."
	@if [ -f "bin/kawaii_tui" ]; then \
		python3 bin/kawaii_tui --health; \
	elif [ -x "bin/kawaii_tui" ]; then \
		./bin/kawaii_tui --health; \
	else \
		echo "❌ Kawaii TUI not found. Run 'make install' first."; \
	fi

# Test installation
test:
	@echo "🧪 Testing Kawaii TUI Installation..."
	@echo ""
	@echo "🔍 Testing components..."
	@python3 -c "import sys; print('✅ Python version:', sys.version)" || echo "❌ Python test failed"
	@tmux -V >/dev/null 2>&1 && echo "✅ Tmux available" || echo "❌ Tmux not found"
	@echo ""
	@echo "🎀 Testing Kawaii TUI..."
	@if [ -f "bin/kawaii_tui" ]; then \
		python3 bin/kawaii_tui --version >/dev/null 2>&1 && echo "✅ Kawaii TUI executable works" || echo "❌ Kawaii TUI test failed"; \
	elif [ -x "bin/kawaii_tui" ]; then \
		./bin/kawaii_tui --version >/dev/null 2>&1 && echo "✅ Kawaii TUI executable works" || echo "❌ Kawaii TUI test failed"; \
	else \
		echo "❌ Kawaii TUI not found"; \
	fi

# Clean temporary files
clean:
	@echo "🧹 Cleaning Kawaii TUI temporary files..."
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache 2>/dev/null || true
	@rm -rf *.egg-info 2>/dev/null || true
	@echo "✨ Temporary files cleaned!"

# Uninstall Kawaii TUI
uninstall:
	@echo "🗑️ Uninstalling Kawaii TUI..."
	@./install.sh --uninstall

# Apply Hello Kitty theme
theme:
	@echo "🎨 Applying Hello Kitty Theme..."
	@if [ -f "bin/kawaii_tui" ]; then \
		python3 bin/kawaii_tui --theme classic; \
	elif [ -x "bin/kawaii_tui" ]; then \
		./bin/kawaii_tui --theme classic; \
	else \
		echo "❌ Kawaii TUI not found. Run 'make install' first."; \
	fi

# Create test collaboration session
session:
	@echo "🖥️ Creating Test Collaboration Session..."
	@SESSION_NAME="test_kawaii_$$(date +%s)"
	@echo "Session name: $$SESSION_NAME"
	@if [ -f "bin/kawaii_tui" ]; then \
		python3 bin/kawaii_tui --mode pair --session $$SESSION_NAME --agents 2; \
	elif [ -x "bin/kawaii_tui" ]; then \
		./bin/kawaii_tui --mode pair --session $$SESSION_NAME --agents 2; \
	else \
		echo "❌ Kawaii TUI not found. Run 'make install' first."; \
	fi
	@echo "💖 Test session created! Use 'tmux attach -t $$SESSION_NAME' to connect."

# List available themes
themes:
	@echo "🎨 Available Hello Kitty Themes:"
	@if [ -f "bin/kawaii_tui" ]; then \
		python3 bin/kawaii_tui --list themes; \
	elif [ -x "bin/kawaii_tui" ]; then \
		./bin/kawaii_tui --list themes; \
	else \
		echo "  🌸 Classic Hello Kitty"
		echo "  💜 Pastel Dreams"
		echo "  ⭐ Starry Night"
		echo "  🌈 Rainbow Kitty"
		echo "  🎀 Minimal Pink"
		echo "  💫 Neon Glow"
		echo ""
		echo "Run 'make install' to enable theme switching.";
	fi

# Show current sessions
sessions:
	@echo "🖥️ Active Kawaii Sessions:"
	@if [ -f "bin/kawaii_tui" ]; then \
		python3 bin/kawaii_tui --list sessions; \
	elif [ -x "bin/kawaii_tui" ]; then \
		./bin/kawaii_tui --list sessions; \
	else \
		tmux list-sessions 2>/dev/null | while read line; do \
			echo "  🖥️ $$line"; \
		done || echo "  📭 No sessions found"; \
	fi

# Launch interactive TUI
tui:
	@echo "🎀 Launching Kawaii TUI Interactive Interface..."
	@if [ -f "bin/kawaii_tui" ]; then \
		python3 bin/kawaii_tui; \
	elif [ -x "bin/kawaii_tui" ]; then \
		./bin/kawaii_tui; \
	else \
		echo "❌ Kawaii TUI not found. Run 'make install' first."; \
	fi

# Development setup
dev-setup:
	@echo "🛠️ Setting up Kawaii TUI Development Environment..."
	@echo "📁 Creating development directories..."
	@mkdir -p tests
	@mkdir -p docs
	@mkdir -p examples
	@echo "✅ Development environment ready!"

# Run linting
lint:
	@echo "🔍 Running code linting..."
	@python3 -m py_compile bin/kawaii_tui.py 2>/dev/null && echo "✅ Main script syntax OK" || echo "❌ Syntax errors found"
	@find lib/ -name "*.py" -exec python3 -m py_compile {} \; 2>/dev/null && echo "✅ Library syntax OK" || echo "❌ Library syntax errors found"

# Check dependencies
deps:
	@echo "📦 Checking Dependencies..."
	@echo "Python: $$(python3 --version 2>/dev/null || echo 'Not found')"
	@echo "Tmux: $$(tmux -V 2>/dev/null || echo 'Not found')"
	@echo "Terminal: $$TERM"
	@echo "User: $$USER"
	@echo "Home: $$HOME"

# Show system info
info:
	@echo "💖 Kawaii TUI System Information"
	@echo "================================"
	@echo "📂 Project Structure:"
	@find . -type f -name "*.py" -o -name "*.md" -o -name "*.sh" -o -name "*.json" | head -20
	@echo ""
	@make deps

# Update (pull latest changes)
update:
	@echo "🔄 Updating Kawaii TUI..."
	@echo "💡 Note: This is a demo. In real usage, this would:"
	@echo "  • Pull latest changes from repository"
	@echo "  • Update configuration if needed"
	@echo "  • Restart services"
	@echo ""
	@echo "🎀 For updates, check the repository for new releases!"

# Backup configuration
backup:
	@echo "💾 Creating Kawaii TUI Backup..."
	@BACKUP_DIR="kawaii_backup_$$(date +%Y%m%d_%H%M%S)"
	@mkdir -p $$BACKUP_DIR
	@cp -r config/ $$BACKUP_DIR/ 2>/dev/null || true
	@tar -czf $$BACKUP_DIR.tar.gz $$BACKUP_DIR 2>/dev/null || true
	@rm -rf $$BACKUP_DIR 2>/dev/null || true
	@echo "✅ Backup created: $$BACKUP_DIR.tar.gz"

# Restore from backup
restore:
	@echo "🔄 Kawaii TUI Restore"
	@echo "💡 To restore from backup:"
	@echo "  1. Extract backup file"
	@echo "  2. Copy config/ to ~/.kawaii_config/"
	@echo "  3. Restart Kawaii TUI"
	@echo ""
	@echo "📁 Available backups:"
	@ls -la kawaii_backup_*.tar.gz 2>/dev/null || echo "  No backups found"

# Show kawaii status
status:
	@echo "📊 Kawaii TUI Status"
	@echo "==================="
	@echo "🎀 Installation: $$(if [ -f "bin/kawaii_tui" ] || [ -x "bin/kawaii_tui" ]; then echo '✅ Installed'; else echo '❌ Not installed'; fi)"
	@echo "💖 Kawaii Level: MAXIMUM! (òωó)"
	@echo "🎨 Themes Available: 6"
	@echo "🤖 AI Modes: 5"
	@echo "🎭 Templates: 8+"
	@echo "🔌 Plugins: 6+"
	@echo ""
	@make sessions

# Quick start guide
quickstart:
	@echo "🚀 Kawaii TUI Quick Start Guide"
	@echo "==============================="
	@echo ""
	@echo "1️⃣ Installation:"
	@echo "   make install"
	@echo ""
	@echo "2️⃣ First Run:"
	@echo "   make demo"
	@echo "   make health"
	@echo ""
	@echo "3️⃣ Daily Usage:"
	@echo "   make tui              # Launch interactive TUI"
	@echo "   make session          # Create test session"
	@echo "   make theme            # Apply Hello Kitty theme"
	@echo ""
	@echo "4️⃣ Management:"
	@echo "   make status           # Check system status"
	@echo "   make sessions         # View active sessions"
	@echo "   make backup           # Backup configuration"
	@echo ""
	@echo "🎀 Ready to start your kawaii journey! (òωó) ♡"

# All demos
demo-complete: demo-all
	@echo ""
	@echo "🎉 All demos completed!"
	@echo "💖 Kawaii level: MAXIMUM!"
	@echo ""
	@echo "🎀 Next steps:"
	@echo "  • Run 'make tui' for interactive experience"
	@echo "  • Run 'make session' to try collaboration"
	@echo "  • Check 'make themes' for styling options"
	@echo ""
	@echo "Happy kawaii collaborating! (òωó) ♡"

# Default action
.DEFAULT_GOAL := help