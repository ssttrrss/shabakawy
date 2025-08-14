#!/bin/bash

# Shabakawy Linux Installer
# This script installs Shabakawy on various Linux distributions

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to detect Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
        VERSION=$VERSION_ID
    elif [ -f /etc/redhat-release ]; then
        DISTRO="rhel"
        VERSION=$(cat /etc/redhat-release | sed 's/.*release \([0-9.]*\).*/\1/')
    elif [ -f /etc/debian_version ]; then
        DISTRO="debian"
        VERSION=$(cat /etc/debian_version)
    else
        DISTRO="unknown"
        VERSION="unknown"
    fi
    
    print_status "Detected distribution: $DISTRO $VERSION"
}

# Function to check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "This script must be run as root (use sudo)"
        exit 1
    fi
}

# Function to update package lists
update_packages() {
    print_status "Updating package lists..."
    
    case $DISTRO in
        "ubuntu"|"debian"|"kali"|"parrot")
            apt update
            ;;
        "fedora"|"rhel"|"centos"|"rocky"|"alma")
            dnf update -y || yum update -y
            ;;
        "arch"|"manjaro")
            pacman -Sy
            ;;
        *)
            print_warning "Unknown distribution, skipping package update"
            ;;
    esac
}

# Function to install Python
install_python() {
    print_status "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION is already installed"
        return 0
    fi
    
    print_status "Installing Python 3..."
    
    case $DISTRO in
        "ubuntu"|"debian"|"kali"|"parrot")
            apt install -y python3 python3-pip python3-venv
            ;;
        "fedora"|"rhel"|"centos"|"rocky"|"alma")
            dnf install -y python3 python3-pip || yum install -y python3 python3-pip
            ;;
        "arch"|"manjaro")
            pacman -S --noconfirm python python-pip
            ;;
        *)
            print_error "Unsupported distribution for Python installation"
            return 1
            ;;
    esac
    
    if command -v python3 &> /dev/null; then
        print_success "Python 3 installed successfully"
    else
        print_error "Failed to install Python 3"
        return 1
    fi
}

# Function to install system dependencies
install_system_deps() {
    print_status "Installing system dependencies..."
    
    case $DISTRO in
        "ubuntu"|"debian"|"kali"|"parrot")
            apt install -y \
                build-essential \
                python3-dev \
                libpcap-dev \
                libffi-dev \
                libssl-dev \
                libxml2-dev \
                libxslt1-dev \
                zlib1g-dev \
                git \
                curl \
                wget \
                chromium-browser \
                chromium-chromedriver
            ;;
        "fedora"|"rhel"|"centos"|"rocky"|"alma")
            dnf install -y \
                gcc \
                python3-devel \
                libpcap-devel \
                libffi-devel \
                openssl-devel \
                libxml2-devel \
                libxslt-devel \
                zlib-devel \
                git \
                curl \
                wget \
                chromium \
                chromium-headless-chromium
            ;;
        "arch"|"manjaro")
            pacman -S --noconfirm \
                base-devel \
                python \
                libpcap \
                libffi \
                openssl \
                libxml2 \
                libxslt \
                zlib \
                git \
                curl \
                wget \
                chromium
            ;;
        *)
            print_warning "Unknown distribution, skipping system dependencies"
            ;;
    esac
}

# Function to install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # Upgrade pip
    python3 -m pip install --upgrade pip
    
    # Install required packages
    python3 -m pip install \
        PyQt5 \
        scapy \
        psutil \
        requests \
        selenium \
        beautifulsoup4 \
        lxml \
        cryptography \
        paramiko \
        netifaces
    
    print_success "Python dependencies installed successfully"
}

# Function to clone repository
clone_repository() {
    print_status "Cloning Shabakawy repository..."
    
    if [ -d "shabakawy" ]; then
        print_warning "Shabakawy directory already exists, removing..."
        rm -rf shabakawy
    fi
    
    git clone https://github.com/ssttrrss/shabakawy.git
    
    if [ -d "shabakawy" ]; then
        print_success "Repository cloned successfully"
    else
        print_error "Failed to clone repository"
        return 1
    fi
}

# Function to create executable
create_executable() {
    print_status "Creating executable..."
    
    cd shabakawy
    
    # Create executable script
    cat > run << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 run.py "$@"
EOF
    
    chmod +x run
    
    # Create desktop entry
    cat > shabakawy.desktop << EOF
[Desktop Entry]
Name=Shabakawy
Comment=Network Security Monitor
Exec=$(pwd)/run
Icon=$(pwd)/icon.png
Terminal=false
Type=Application
Categories=Network;Security;System;
EOF
    
    # Install desktop entry
    if [ -d "/usr/share/applications" ]; then
        cp shabakawy.desktop /usr/share/applications/
        print_success "Desktop entry created"
    fi
    
    print_success "Executable created successfully"
}

# Function to setup firewall rules
setup_firewall() {
    print_status "Setting up firewall rules..."
    
    # Check if firewall is active
    if command -v ufw &> /dev/null && ufw status | grep -q "Status: active"; then
        print_status "UFW firewall detected, adding rules..."
        ufw allow out 53/tcp  # DNS
        ufw allow out 53/udp  # DNS
        ufw allow out 80/tcp  # HTTP
        ufw allow out 443/tcp # HTTPS
        print_success "Firewall rules configured"
    elif command -v firewall-cmd &> /dev/null; then
        print_status "Firewalld detected, adding rules..."
        firewall-cmd --permanent --add-service=dns
        firewall-cmd --permanent --add-service=http
        firewall-cmd --permanent --add-service=https
        firewall-cmd --reload
        print_success "Firewall rules configured"
    else
        print_warning "No supported firewall detected, skipping firewall configuration"
    fi
}

# Function to create configuration
create_config() {
    print_status "Creating configuration..."
    
    # Create config directory
    mkdir -p /etc/shabakawy
    
    # Create default configuration
    cat > /etc/shabakawy/shabakawy.conf << 'EOF'
[network]
scan_interval = 30
packet_capture_timeout = 60
max_devices = 100

[security]
ddos_threshold = 1000
mitm_detection = true
auto_block = true

[router]
default_gateway = 192.168.1.1
admin_port = 80
timeout = 30

[gui]
theme = light
auto_refresh = true
notifications = true
EOF
    
    chmod 644 /etc/shabakawy/shabakawy.conf
    print_success "Configuration created"
}

# Function to setup logging
setup_logging() {
    print_status "Setting up logging..."
    
    # Create log directory
    mkdir -p /var/log/shabakawy
    
    # Create logrotate configuration
    cat > /etc/logrotate.d/shabakawy << 'EOF'
/var/log/shabakawy/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 root root
}
EOF
    
    print_success "Logging configured"
}

# Function to create systemd service
create_service() {
    print_status "Creating systemd service..."
    
    cat > /etc/systemd/system/shabakawy.service << EOF
[Unit]
Description=Shabakawy Network Security Monitor
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/run
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
    
    # Reload systemd and enable service
    systemctl daemon-reload
    systemctl enable shabakawy.service
    
    print_success "Systemd service created and enabled"
}

# Function to check installation
check_installation() {
    print_status "Checking installation..."
    
    # Check if Python dependencies are available
    python3 -c "
import sys
try:
    import PyQt5
    import scapy
    import psutil
    import requests
    import selenium
    print('All Python dependencies are available')
except ImportError as e:
    print(f'Missing dependency: {e}')
    sys.exit(1)
"
    
    # Check if executable exists
    if [ -f "run" ] && [ -x "run" ]; then
        print_success "Executable file is ready"
    else
        print_error "Executable file not found or not executable"
        return 1
    fi
    
    print_success "Installation check completed successfully"
}

# Function to display completion message
show_completion() {
    echo
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}    Shabakawy Installation Complete!   ${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo
    echo -e "Installation completed successfully!"
    echo
    echo -e "To run Shabakawy:"
    echo -e "  ${BLUE}cd shabakawy${NC}"
    echo -e "  ${BLUE}./run${NC}"
    echo
    echo -e "Or use the desktop application launcher"
    echo
    echo -e "Configuration file: ${BLUE}/etc/shabakawy/shabakawy.conf${NC}"
    echo -e "Log files: ${BLUE}/var/log/shabakawy/${NC}"
    echo
    echo -e "For more information, see the README.md file"
    echo
}

# Main installation function
main() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}    Shabakawy Linux Installer v1.0    ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo
    
    # Check if running as root
    check_root
    
    # Detect distribution
    detect_distro
    
    # Update packages
    update_packages
    
    # Install Python
    install_python
    
    # Install system dependencies
    install_system_deps
    
    # Install Python dependencies
    install_python_deps
    
    # Clone repository
    clone_repository
    
    # Create executable
    create_executable
    
    # Setup firewall
    setup_firewall
    
    # Create configuration
    create_config
    
    # Setup logging
    setup_logging
    
    # Create systemd service
    create_service
    
    # Check installation
    check_installation
    
    # Show completion message
    show_completion
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --check        Check if Shabakawy is installed"
        echo "  --uninstall    Remove Shabakawy installation"
        echo
        echo "Examples:"
        echo "  sudo $0                    # Install Shabakawy"
        echo "  sudo $0 --check            # Check installation"
        echo "  sudo $0 --uninstall        # Remove Shabakawy"
        exit 0
        ;;
    --check)
        if [ -d "shabakawy" ]; then
            print_success "Shabakawy is installed"
            check_installation
        else
            print_warning "Shabakawy is not installed"
            exit 1
        fi
        exit 0
        ;;
    --uninstall)
        print_status "Uninstalling Shabakawy..."
        
        # Stop and disable service
        if systemctl is-active --quiet shabakawy.service; then
            systemctl stop shabakawy.service
        fi
        if systemctl is-enabled --quiet shabakawy.service; then
            systemctl disable shabakawy.service
        fi
        
        # Remove service file
        rm -f /etc/systemd/system/shabakawy.service
        systemctl daemon-reload
        
        # Remove application files
        rm -rf shabakawy
        
        # Remove configuration and logs
        rm -rf /etc/shabakawy
        rm -rf /var/log/shabakawy
        rm -f /etc/logrotate.d/shabakawy
        
        # Remove desktop entry
        rm -f /usr/share/applications/shabakawy.desktop
        
        print_success "Shabakawy uninstalled successfully"
        exit 0
        ;;
    "")
        # No arguments, run installation
        main
        ;;
    *)
        print_error "Unknown option: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac
