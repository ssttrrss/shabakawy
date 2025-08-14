# Shabakawy Installation and Usage Guide

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Installation](#quick-installation)
3. [Manual Installation](#manual-installation)
4. [Configuration](#configuration)
5. [Usage Guide](#usage-guide)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Configuration](#advanced-configuration)
8. [Security Considerations](#security-considerations)

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+ or Linux (Ubuntu 18.04+, Kali Linux, etc.)
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM
- **Storage**: 2GB free space
- **Network**: Active internet connection for initial setup

### Recommended Requirements
- **Operating System**: Windows 11 or Linux (Ubuntu 20.04+, Kali Linux 2023+)
- **Python**: 3.9 or higher
- **Memory**: 8GB RAM or more
- **Storage**: 5GB free space
- **Network**: Gigabit Ethernet or Wi-Fi 6
- **Graphics**: Support for OpenGL 3.3+

### Supported Platforms
- **Windows**: 10, 11 (x64)
- **Linux**: Ubuntu, Debian, Kali Linux, Parrot OS, Fedora, CentOS, Arch Linux
- **macOS**: Not officially supported (may work with modifications)

## Quick Installation

### Windows Users

1. **Download the installer**:
   - Right-click `install_and_setup_win.bat`
   - Select "Run as administrator"

2. **Follow the prompts**:
   - The installer will check for Python
   - Install required dependencies
   - Clone the repository
   - Create shortcuts and configuration

3. **Launch the application**:
   - Double-click the desktop shortcut
   - Or run `run.bat` from the installation directory

### Linux Users

1. **Make the installer executable**:
   ```bash
   chmod +x install_and_setup_linux.sh
   ```

2. **Run the installer**:
   ```bash
   sudo ./install_and_setup_linux.sh
   ```

3. **Launch the application**:
   ```bash
   cd shabakawy
   ./run
   ```

## Manual Installation

### Prerequisites Installation

#### Windows

1. **Install Python**:
   - Download from [python.org](https://www.python.org/downloads/)
   - Check "Add Python to PATH" during installation
   - Verify: `python --version`

2. **Install Git**:
   - Download from [git-scm.com](https://git-scm.com/download/win)
   - Use default settings

#### Linux (Ubuntu/Debian)

```bash
# Update package lists
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install system dependencies
sudo apt install build-essential python3-dev libpcap-dev libffi-dev libssl-dev

# Install Git
sudo apt install git

# Install browser for Selenium
sudo apt install chromium-browser chromium-chromedriver
```

#### Linux (Kali Linux)

```bash
# Update package lists
sudo apt update

# Install Python dependencies
sudo apt install python3-pip python3-venv

# Install system dependencies
sudo apt install build-essential python3-dev libpcap-dev libffi-dev libssl-dev

# Install Git
sudo apt install git

# Install browser for Selenium
sudo apt install chromium
```

#### Linux (Fedora/CentOS)

```bash
# Update package lists
sudo dnf update

# Install Python and dependencies
sudo dnf install python3 python3-pip python3-devel gcc libpcap-devel libffi-devel openssl-devel

# Install Git
sudo dnf install git

# Install browser for Selenium
sudo dnf install chromium
```

### Application Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ssttrrss/shabakawy.git
   cd shabakawy
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install PyQt5 scapy psutil requests selenium beautifulsoup4 lxml cryptography paramiko netifaces
   ```

3. **Create configuration**:
   ```bash
   mkdir -p ~/.shabakawy
   cp config/shabakawy.conf ~/.shabakawy/
   ```

4. **Make executable**:
   ```bash
   chmod +x run.py
   ```

## Configuration

### Configuration File Location

- **Windows**: `%APPDATA%\Shabakawy\shabakawy.conf`
- **Linux**: `~/.shabakawy/shabakawy.conf`

### Configuration Options

#### Network Settings
```ini
[network]
scan_interval = 30          # Network scan interval in seconds
packet_capture_timeout = 60 # Packet capture timeout
max_devices = 100          # Maximum devices to track
```

#### Security Settings
```ini
[security]
ddos_threshold = 1000      # DDoS detection threshold
mitm_detection = true       # Enable MITM detection
auto_block = true          # Auto-block malicious devices
```

#### Router Settings
```ini
[router]
default_gateway = 192.168.1.1  # Router IP address
admin_port = 80                # Router admin port
timeout = 30                   # Connection timeout
username = admin               # Router admin username
password =                     # Router admin password
```

#### GUI Settings
```ini
[gui]
theme = light                 # light or dark
auto_refresh = true          # Auto-refresh data
notifications = true         # Enable notifications
```

### Router Configuration

1. **Find your router's IP address**:
   - Windows: `ipconfig` (look for Default Gateway)
   - Linux: `ip route show default`

2. **Access router admin panel**:
   - Open browser and navigate to `http://[ROUTER_IP]`
   - Login with admin credentials

3. **Enable required features**:
   - Access Control Lists (ACL)
   - MAC Address Filtering
   - QoS/Bandwidth Control
   - Guest Network (optional)

## Usage Guide

### First Launch

1. **Start the application**:
   - Windows: Double-click desktop shortcut or run `run.bat`
   - Linux: Run `./run` from terminal

2. **Initial setup**:
   - The app will create configuration files
   - Check system requirements
   - Initialize logging

### Dashboard Tab

The Dashboard provides an overview of your network security status:

- **Network Status**: Shows device counts and threat levels
- **System Information**: Displays OS and hardware details
- **Control Buttons**: Start/stop network scanning

### Threats & Alerts Tab

Monitor and manage security threats:

- **Threats Table**: Lists all detected threats with details
- **Severity Levels**: Color-coded threat severity
- **Actions**: Clear threats, export data

### Router Control Tab

Manage your router and connected devices:

1. **Connect to Router**:
   - Enter router IP, username, and password
   - Choose connection method (HTTP or Selenium)
   - Click "Connect"

2. **Device Management**:
   - View connected devices
   - Block/unblock specific devices
   - Set speed limits

3. **Wi-Fi Settings**:
   - Change Wi-Fi password
   - Configure security settings

### Advanced Analysis Tab

Deep packet inspection and analysis:

1. **Packet Capture**:
   - Select network interface
   - Start/stop capture
   - Monitor statistics

2. **Analysis Options**:
   - Enable/disable detection types
   - View real-time analysis results

### Network Scanning

1. **Start Scanning**:
   - Click "Start Scanning" on Dashboard
   - App will discover network devices
   - Monitor for threats in real-time

2. **Scan Results**:
   - Device information (IP, MAC, hostname)
   - Connection status and threat levels
   - Port scanning results

### Threat Detection

The application detects various threats:

- **DDoS Attacks**: High connection rates from single sources
- **MITM Attacks**: Suspicious ARP behavior
- **MAC Spoofing**: Duplicate MAC addresses
- **Network Anomalies**: Unusual traffic patterns

## Troubleshooting

### Common Issues

#### Python Import Errors

**Error**: `ModuleNotFoundError: No module named 'PyQt5'`

**Solution**:
```bash
pip install PyQt5
```

**Error**: `ModuleNotFoundError: No module named 'scapy'`

**Solution**:
```bash
pip install scapy
```

#### Permission Errors

**Error**: `Permission denied` when running packet capture

**Solution**:
- **Windows**: Run as Administrator
- **Linux**: Use `sudo` or add user to appropriate groups

#### Router Connection Issues

**Error**: "Failed to connect to router"

**Solutions**:
1. Verify router IP address
2. Check if router admin panel is accessible
3. Verify username/password
4. Try different connection method

#### Network Interface Issues

**Error**: "No network interfaces found"

**Solutions**:
1. Check network adapter status
2. Verify network connection
3. Run as Administrator (Windows) or with sudo (Linux)

### Performance Issues

#### High CPU Usage

**Causes**:
- Large network with many devices
- Aggressive packet capture
- Complex threat detection rules

**Solutions**:
1. Increase scan interval in configuration
2. Reduce packet capture timeout
3. Limit number of tracked devices

#### Memory Issues

**Causes**:
- Long-running packet capture
- Large threat history
- Multiple analysis sessions

**Solutions**:
1. Clear threat history regularly
2. Restart application periodically
3. Increase system RAM

### Log Analysis

#### View Logs

- **Windows**: `%APPDATA%\Shabakawy\logs\`
- **Linux**: `~/.shabakawy/logs/`

#### Common Log Messages

```
[INFO] Starting network scanning...
[WARNING] DDoS threat detected from 192.168.1.100
[ERROR] Failed to connect to router: Connection timeout
[SUCCESS] Device 00:11:22:33:44:55 blocked successfully
```

### Getting Help

1. **Check the logs** for detailed error information
2. **Verify system requirements** are met
3. **Check network connectivity** and firewall settings
4. **Review configuration** for incorrect settings
5. **Search existing issues** on GitHub
6. **Create new issue** with detailed information

## Advanced Configuration

### Custom Threat Detection Rules

Create custom detection rules in configuration:

```ini
[security]
custom_rules = true
ddos_threshold = 500        # Lower threshold for sensitive networks
mitm_detection = true
arp_monitoring = true       # Enable ARP table monitoring
```

### Network Segmentation

Configure for multiple network segments:

```ini
[network]
segments = 192.168.1.0/24,192.168.2.0/24
scan_interval = 15          # Faster scanning for critical networks
max_devices = 200
```

### Integration with SIEM

Configure logging for SIEM integration:

```ini
[logging]
level = DEBUG
format = json
syslog = true
syslog_host = 192.168.1.10
syslog_port = 514
```

### Custom Router Integration

Add support for custom router models:

```ini
[router]
custom_model = true
login_url = /custom_login.asp
device_list_url = /custom_devices.asp
block_url = /custom_block.asp
```

## Security Considerations

### Application Security

1. **Run with minimal privileges**:
   - Use dedicated user account
   - Limit file system access
   - Restrict network access

2. **Secure configuration**:
   - Use strong passwords
   - Encrypt sensitive data
   - Regular security updates

3. **Network security**:
   - Use VPN for remote access
   - Implement network segmentation
   - Monitor for unauthorized access

### Privacy Considerations

1. **Data collection**:
   - Only collect necessary information
   - Anonymize sensitive data
   - Implement data retention policies

2. **User consent**:
   - Inform users about monitoring
   - Obtain explicit consent
   - Provide opt-out mechanisms

3. **Compliance**:
   - Follow local privacy laws
   - Implement GDPR requirements
   - Regular privacy audits

### Legal Considerations

1. **Authorized monitoring**:
   - Only monitor authorized networks
   - Obtain proper permissions
   - Follow company policies

2. **Data handling**:
   - Secure data storage
   - Proper data disposal
   - Audit trail maintenance

3. **Incident response**:
   - Document all incidents
   - Follow reporting procedures
   - Preserve evidence properly

## Support and Updates

### Getting Updates

1. **Check for updates**:
   ```bash
   cd shabakawy
   git pull origin main
   ```

2. **Reinstall dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

### Community Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check this guide and README
- **Discussions**: Join community forums

### Professional Support

For enterprise deployments and professional support:
- Contact the development team
- Request custom features
- Schedule training sessions

---

## Quick Reference

### Common Commands

```bash
# Start application
./run

# Check configuration
cat ~/.shabakawy/shabakawy.conf

# View logs
tail -f ~/.shabakawy/logs/shabakawy.log

# Update application
git pull origin main

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Configuration File Locations

- **Config**: `~/.shabakawy/shabakawy.conf`
- **Logs**: `~/.shabakawy/logs/`
- **Cache**: `~/.shabakawy/cache/`

### Default Ports

- **Router Admin**: 80 (HTTP), 443 (HTTPS)
- **DNS**: 53 (UDP/TCP)
- **Application**: No default port (local only)

### File Permissions

```bash
# Make executable
chmod +x run.py

# Set proper ownership
sudo chown -R $USER:$USER ~/.shabakawy

# Set proper permissions
chmod 600 ~/.shabakawy/shabakawy.conf
chmod 755 ~/.shabakawy/logs/
```

---

*This guide covers the essential information needed to install, configure, and use Shabakawy. For more detailed information, refer to the source code and GitHub repository.*
