#!/bin/bash

# shōmei Linux Installation Script
# This script installs shōmei on Linux systems

set -e

# Display ASCII logo
cat << 'EOF'

███████╗██╗  ██╗ ██████╗ ███╗   ███╗███████╗██╗
██╔════╝██║  ██║██╔═══██╗████╗ ████║██╔════╝██║
███████╗███████║██║   ██║██╔████╔██║█████╗  ██║
╚════██║██╔══██║██║   ██║██║╚██╔╝██║██╔══╝  ██║
███████║██║  ██║╚██████╔╝██║ ╚═╝ ██║███████╗██║
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝

EOF

echo "🚀 Installing shomei on Linux..."

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root"
   echo "Please run without sudo: ./install.sh"
   exit 1
fi

# Detect Linux distribution
if command -v apt-get &> /dev/null; then
    PACKAGE_MANAGER="apt"
elif command -v dnf &> /dev/null; then
    PACKAGE_MANAGER="dnf"
elif command -v yum &> /dev/null; then
    PACKAGE_MANAGER="yum"
elif command -v pacman &> /dev/null; then
    PACKAGE_MANAGER="pacman"
else
    echo "❌ Unsupported package manager. Please install manually."
    exit 1
fi

echo "📦 Detected package manager: $PACKAGE_MANAGER"

# Install system dependencies
echo "🔧 Installing system dependencies..."
case $PACKAGE_MANAGER in
    "apt")
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv git curl
        ;;
    "dnf")
        sudo dnf install -y python3 python3-pip python3-venv git curl
        ;;
    "yum")
        sudo yum install -y python3 python3-pip python3-venv git curl
        ;;
    "pacman")
        sudo pacman -S --noconfirm python python-pip python-virtualenv git curl
        ;;
esac

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv ~/.shomei-env

# Activate environment and install shomei
echo "📥 Installing shomei..."
source ~/.shomei-env/bin/activate
pip install --upgrade pip
pip install shomei

# Add to shell profile
SHELL_PROFILE=""
if [[ -f ~/.bashrc ]]; then
    SHELL_PROFILE=~/.bashrc
elif [[ -f ~/.zshrc ]]; then
    SHELL_PROFILE=~/.zshrc
elif [[ -f ~/.profile ]]; then
    SHELL_PROFILE=~/.profile
fi

if [[ -n "$SHELL_PROFILE" ]]; then
    echo "🔗 Adding shomei to your PATH in $SHELL_PROFILE"
    echo 'export PATH="$HOME/.shomei-env/bin:$PATH"' >> "$SHELL_PROFILE"
else
    echo "⚠️  Could not find shell profile. Please manually add to your PATH:"
    echo 'export PATH="$HOME/.shomei-env/bin:$PATH"'
fi

# Test installation
echo "🧪 Testing installation..."
source ~/.shomei-env/bin/activate
if command -v shomei &> /dev/null; then
    echo ""
    echo "🎉 Installation successful!"
    echo ""
    echo "🎯 To use shomei:"
    echo "   shomei --help"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Restart your terminal or run: source $SHELL_PROFILE"
    echo "   2. Initialize configuration: shomei init"
    echo "   3. Start using: shomei analyze /path/to/repo"
    echo ""
    echo "🔗 For more info: https://github.com/petarran/shomei"
    echo ""
    echo "🤝 Want to contribute? Run: shomei contribute"
else
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi
