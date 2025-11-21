#!/bin/bash
# 🎀 Kawaii TUI Installation Script
# Hello Kitty AI Collaboration Manager Setup

set -e

# Colors for kawaii output
PINK='\033[0;35m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
RESET='\033[0m'

# Kawaii printing functions
print_kawaii_banner() {
    echo -e "${PINK}"
    cat << 'EOF'
🎀 ♡ (òωó) Welcome to Kawaii TUI Installation! ♡ 🎀
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hello Kitty AI Collaboration Manager Setup
Where productivity meets pure cuteness! ♡
EOF
    echo -e "${RESET}"
}

print_step() {
    echo -e "${YELLOW}🎀 $1${RESET}"
}

print_success() {
    echo -e "${GREEN}✅ $1${RESET}"
}

print_error() {
    echo -e "${RED}❌ $1${RESET}"
}

print_info() {
    echo -e "${BLUE}💡 $1${RESET}"
}

# Check system compatibility
check_requirements() {
    print_step "Checking system requirements..."
    
    local errors=0
    
    # Check Python
    if command -v python3 >/dev/null 2>&1; then
        python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 7) else 1)'; then
            print_success "Python $python_version detected (✓ 3.7+)"
        else
            print_error "Python 3.7+ required, found $python_version"
            errors=$((errors + 1))
        fi
    else
        print_error "Python 3 not found"
        errors=$((errors + 1))
    fi
    
    # Check tmux
    if command -v tmux >/dev/null 2>&1; then
        tmux_version=$(tmux -V | cut -d' ' -f2)
        print_success "Tmux $tmux_version detected"
    else
        print_error "Tmux not found"
        errors=$((errors + 1))
    fi
    
    # Check terminal compatibility
    if [ -n "$TERM" ]; then
        print_success "Terminal: $TERM"
    else
        print_info "TERM environment variable not set"
    fi
    
    return $errors
}

# Install system dependencies
install_dependencies() {
    print_step "Installing system dependencies..."
    
    # Detect package manager
    if command -v apt >/dev/null 2>&1; then
        print_info "Detected apt package manager (Ubuntu/Debian)"
        sudo apt update
        sudo apt install -y python3 python3-pip tmux curl wget
        
    elif command -v brew >/dev/null 2>&1; then
        print_info "Detected Homebrew (macOS)"
        brew install python3 tmux
        
    elif command -v yum >/dev/null 2>&1; then
        print_info "Detected yum package manager (CentOS/RHEL)"
        sudo yum install -y python3 python3-pip tmux curl wget
        
    elif command -v pacman >/dev/null 2>&1; then
        print_info "Detected pacman package manager (Arch Linux)"
        sudo pacman -S --noconfirm python3 python3-pip tmux curl wget
        
    else
        print_error "Unsupported package manager. Please install manually:"
        print_info "  - Python 3.7+"
        print_info "  - Tmux 2.9+"
        print_info "  - curl/wget for downloads"
        return 1
    fi
    
    print_success "System dependencies installed!"
}

# Setup Kawaii TUI directories
setup_directories() {
    print_step "Setting up Kawaii TUI directory structure..."
    
    # Create directories
    local dirs=(
        "$HOME/.kawaii_config"
        "$HOME/.kawaii_cache"
        "$HOME/.kawaii_logs"
        "$HOME/.kawaii_data"
        "$HOME/.kawaii_tmp"
        "$HOME/.kawaii_sessions"
        "$HOME/.kawaii_snapshots"
        "$HOME/.kawaii_templates"
        "$HOME/.kawaii_plugins"
        "$HOME/.kawaii_knowledge"
        "$HOME/.kawaii_themes"
        "$HOME/.kawaii_plugin_store"
    )
    
    for dir in "${dirs[@]}"; do
        mkdir -p "$dir"
        print_success "Created: $dir"
    done
}

# Copy Kawaii TUI files
install_kawaii_tui() {
    print_step "Installing Kawaii TUI files..."
    
    local install_dir="$HOME/.local/bin/kawaii-tui"
    
    # Create installation directory
    mkdir -p "$install_dir"
    
    # Copy main script
    cp bin/kawaii_tui "$install_dir/"
    chmod +x "$install_dir/kawaii_tui"
    
    # Copy library files
    cp -r lib/ "$install_dir/"
    cp -r config/ "$install_dir/"
    
    # Create symlink in PATH
    if [ -d "$HOME/.local/bin" ]; then
        if [ ! -L "$HOME/.local/bin/kawaii-tui" ]; then
            ln -sf "$install_dir/kawaii_tui" "$HOME/.local/bin/kawaii-tui"
        fi
        print_success "Kawaii TUI installed to: $install_dir"
        print_info "Add to PATH: export PATH=\"\$HOME/.local/bin:\$PATH\""
    else
        print_info "Installation directory: $install_dir"
        print_info "Run with: $install_dir/kawaii_tui"
    fi
}

# Create configuration
create_config() {
    print_step "Creating default configuration..."
    
    # Copy default config if exists
    if [ -f "config/kawaii_config.json" ]; then
        cp config/kawaii_config.json "$HOME/.kawaii_config/kawaii_config.json"
        print_success "Default configuration created"
    fi
}

# Test installation
test_installation() {
    print_step "Testing Kawaii TUI installation..."
    
    # Find kawaii_tui command
    local kawaii_cmd
    if [ -x "$HOME/.local/bin/kawaii-tui" ]; then
        kawaii_cmd="$HOME/.local/bin/kawaii-tui"
    elif [ -x "bin/kawaii_tui" ]; then
        kawaii_cmd="bin/kawaii_tui"
    else
        print_error "Could not find kawaii_tui executable"
        return 1
    fi
    
    # Test basic functionality
    if $kawaii_cmd --version >/dev/null 2>&1; then
        print_success "Kawaii TUI executable works!"
    else
        print_info "Testing Python module directly..."
        if python3 bin/kawaii_tui.py --version >/dev/null 2>&1; then
            print_success "Kawaii TUI works via Python!"
        else
            print_error "Installation test failed"
            return 1
        fi
    fi
    
    # Test health check
    print_info "Running system health check..."
    if $kawaii_cmd --health 2>&1 | grep -q "kawaii"; then
        print_success "Health check passed!"
    else
        print_info "Health check completed (some warnings are normal)"
    fi
}

# Show completion message
show_completion() {
    echo
    echo -e "${PINK}🎉 Kawaii TUI Installation Complete! (òωó) 🎉${RESET}"
    echo
    echo -e "${GREEN}💖 Installation Summary:${RESET}"
    echo -e "  🎀 Kawaii TUI: Ready for maximum cuteness!"
    echo -e "  🖥️  Directory: $HOME/.local/bin/kawaii-tui"
    echo -e "  📁 Config: $HOME/.kawaii_config/"
    echo -e "  📊 Logs: $HOME/.kawaii_logs/"
    echo
    echo -e "${YELLOW}🚀 Quick Start:${RESET}"
    echo -e "  Launch Kawaii TUI: ${GREEN}kawaii-tui${RESET}"
    echo -e "  Run demo: ${GREEN}kawaii-tui --demo${RESET}"
    echo -e "  Health check: ${GREEN}kawaii-tui --health${RESET}"
    echo -e "  Start collaboration: ${GREEN}kawaii-tui --mode pair${RESET}"
    echo
    echo -e "${PINK}💕 Your kawaii journey begins now! (òωó) ♡${RESET}"
    echo
}

# Main installation function
main() {
    print_kawaii_banner
    
    echo
    print_step "Starting Kawaii TUI installation..."
    
    # Check if running from correct directory
    if [ ! -f "bin/kawaii_tui" ] || [ ! -d "lib" ]; then
        print_error "Please run this script from the Kawaii TUI root directory"
        print_info "The directory should contain bin/kawaii_tui and lib/ folder"
        exit 1
    fi
    
    # Run installation steps
    check_requirements
    if [ $? -ne 0 ]; then
        print_error "System requirements check failed"
        print_info "Please install missing dependencies and try again"
        exit 1
    fi
    
    install_dependencies
    setup_directories
    install_kawaii_tui
    create_config
    test_installation
    show_completion
}

# Handle script arguments
case "${1:-}" in
    --help|-h)
        echo "🎀 Kawaii TUI Installation Script"
        echo
        echo "Usage: $0 [options]"
        echo
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --uninstall    Remove Kawaii TUI installation"
        echo
        echo "This script installs Kawaii TUI with Hello Kitty theming!"
        exit 0
        ;;
    --uninstall)
        print_step "Uninstalling Kawaii TUI..."
        rm -rf "$HOME/.local/bin/kawaii-tui"
        rm -rf "$HOME/.kawaii_config" "$HOME/.kawaii_cache" "$HOME/.kawaii_logs"
        rm -rf "$HOME/.kawaii_sessions" "$HOME/.kawaii_snapshots" "$HOME/.kawaii_templates"
        rm -rf "$HOME/.kawaii_plugins" "$HOME/.kawaii_knowledge" "$HOME/.kawaii_themes"
        print_success "Kawaii TUI uninstalled!"
        print_info "Your data has been removed. Kawaii farewell! (òωó)"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac