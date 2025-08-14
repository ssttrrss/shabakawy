#!/usr/bin/env python3
"""
Shabakawy Utilities Module
Helper functions for logging, configuration, and cross-platform compatibility
"""

import os
import sys
import json
import logging
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import configparser

# Global configuration
CONFIG_FILE = "shabakawy.conf"
LOG_FILE = "shabakawy.log"
DEFAULT_CONFIG = {
    "network": {
        "scan_interval": "30",
        "packet_capture_timeout": "60",
        "max_devices": "100"
    },
    "security": {
        "ddos_threshold": "1000",
        "mitm_detection": "true",
        "auto_block": "true"
    },
    "router": {
        "default_gateway": "192.168.1.1",
        "admin_port": "80",
        "timeout": "30"
    },
    "gui": {
        "theme": "dark",
        "auto_refresh": "true",
        "notifications": "true"
    }
}

def get_platform_info() -> Dict[str, str]:
    """Get detailed platform information"""
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version()
    }

def is_windows() -> bool:
    """Check if running on Windows"""
    return platform.system().lower() == "windows"

def is_linux() -> bool:
    """Check if running on Linux"""
    return platform.system().lower() == "linux"

def is_kali() -> bool:
    """Check if running on Kali Linux"""
    if not is_linux():
        return False
    try:
        with open("/etc/os-release", "r") as f:
            content = f.read().lower()
            return "kali" in content
    except:
        return False

def get_app_data_dir() -> Path:
    """Get application data directory for current platform"""
    if is_windows():
        base = Path(os.environ.get("APPDATA", ""))
        return base / "Shabakawy"
    else:
        base = Path.home()
        return base / ".shabakawy"

def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration"""
    # Create app data directory if it doesn't exist
    app_dir = get_app_data_dir()
    app_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = app_dir / LOG_FILE
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

def load_config() -> configparser.ConfigParser:
    """Load configuration from file or create default"""
    config = configparser.ConfigParser()
    
    # Try to load existing config
    config_file = get_app_data_dir() / CONFIG_FILE
    if config_file.exists():
        config.read(config_file)
    else:
        # Create default config
        for section, options in DEFAULT_CONFIG.items():
            config.add_section(section)
            for key, value in options.items():
                config.set(section, key, value)
        save_config(config)
    
    return config

def save_config(config: configparser.ConfigParser) -> None:
    """Save configuration to file"""
    config_file = get_app_data_dir() / CONFIG_FILE
    with open(config_file, 'w') as f:
        config.write(f)

def check_dependencies() -> bool:
    """Check if all required dependencies are installed"""
    required_packages = [
        "PyQt5",
        "scapy",
        "psutil",
        "requests",
        "selenium"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logging.error(f"Missing required packages: {', '.join(missing_packages)}")
        return False
    
    return True

def run_command(command: List[str], timeout: int = 30) -> Tuple[int, str, str]:
    """Run a system command with timeout"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout} seconds"
    except Exception as e:
        return -1, "", str(e)

def get_network_interfaces() -> List[Dict[str, str]]:
    """Get list of available network interfaces"""
    interfaces = []
    
    if is_windows():
        # Windows: use netsh
        try:
            result = subprocess.run(
                ["netsh", "interface", "show", "interface"],
                capture_output=True,
                text=True
            )
            lines = result.stdout.split('\n')
            for line in lines[3:]:  # Skip header lines
                if line.strip() and 'Loopback' not in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        interfaces.append({
                            "name": parts[3],
                            "status": parts[2],
                            "type": parts[1]
                        })
        except:
            pass
    else:
        # Linux: use ip command
        try:
            result = subprocess.run(
                ["ip", "link", "show"],
                capture_output=True,
                text=True
            )
            lines = result.stdout.split('\n')
            for line in lines:
                if ':' in line and 'lo:' not in line:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        name = parts[1].strip()
                        status = "UP" if "UP" in line else "DOWN"
                        interfaces.append({
                            "name": name,
                            "status": status,
                            "type": "Ethernet"
                        })
        except:
            pass
    
    return interfaces

def get_default_gateway() -> Optional[str]:
    """Get the default gateway IP address"""
    if is_windows():
        try:
            result = subprocess.run(
                ["route", "print", "0.0.0.0"],
                capture_output=True,
                text=True
            )
            lines = result.stdout.split('\n')
            for line in lines:
                if '0.0.0.0' in line and '0.0.0.0' in line.split():
                    parts = line.split()
                    if len(parts) >= 4:
                        return parts[3]
        except:
            pass
    else:
        try:
            result = subprocess.run(
                ["ip", "route", "show", "default"],
                capture_output=True,
                text=True
            )
            lines = result.stdout.split('\n')
            for line in lines:
                if 'default via' in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        return parts[2]
        except:
            pass
    
    return None

def format_bytes(bytes_value: int) -> str:
    """Format bytes into human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def validate_ip_address(ip: str) -> bool:
    """Validate IP address format"""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                return False
        return True
    except:
        return False

def validate_mac_address(mac: str) -> bool:
    """Validate MAC address format"""
    import re
    pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return bool(re.match(pattern, mac))

def get_system_info() -> Dict[str, str]:
    """Get comprehensive system information"""
    info = get_platform_info()
    
    # Add additional system info
    try:
        import psutil
        info.update({
            "cpu_count": str(psutil.cpu_count()),
            "memory_total": format_bytes(psutil.virtual_memory().total),
            "disk_total": format_bytes(psutil.disk_usage('/').total) if is_linux() else "N/A"
        })
    except:
        pass
    
    return info
