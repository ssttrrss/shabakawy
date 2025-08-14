#!/usr/bin/env python3
"""
Shabakawy Router Control Module
Router automation, device management, and network configuration
"""

import time
import logging
import threading
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import json
import re

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logging.warning("Requests not available. HTTP-based router control will be limited.")

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logging.warning("Selenium not available. Browser-based router control will be limited.")

from utils import (
    is_windows, is_linux, get_default_gateway, validate_ip_address,
    validate_mac_address, run_command
)

@dataclass
class RouterDevice:
    """Represents a device managed by the router"""
    mac: str
    ip: str
    hostname: str
    status: str  # "connected", "disconnected", "blocked"
    connection_time: datetime
    data_usage: int
    speed_limit: Optional[int] = None  # in Mbps
    blocked_until: Optional[datetime] = None

@dataclass
class RouterSettings:
    """Router configuration settings"""
    ssid: str
    password: str
    encryption: str  # "WPA2", "WPA3", "WEP"
    channel: int
    bandwidth: str  # "20MHz", "40MHz", "80MHz"
    guest_network_enabled: bool
    parental_controls_enabled: bool
    firewall_enabled: bool

class RouterController:
    """Main router controller class"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.router_ip = config.get("default_gateway", "192.168.1.1")
        self.admin_port = int(config.get("admin_port", 80))
        self.timeout = int(config.get("timeout", 30))
        self.username = config.get("username", "admin")
        self.password = config.get("password", "")
        
        # Router state
        self.connected = False
        self.session = None
        self.driver = None
        self.devices: Dict[str, RouterDevice] = {}
        self.settings: Optional[RouterSettings] = None
        
        # Supported router models
        self.supported_models = {
            "tp-link": "TP-Link",
            "netgear": "Netgear",
            "asus": "ASUS",
            "linksys": "Linksys",
            "d-link": "D-Link",
            "belkin": "Belkin",
            "tenda": "Tenda",
            "huawei": "Huawei"
        }
        
        self.logger = logging.getLogger(__name__)
    
    def detect_router_model(self) -> Optional[str]:
        """Detect router model automatically"""
        try:
            # Try to access router admin page
            if not REQUESTS_AVAILABLE:
                return None
            
            response = requests.get(
                f"http://{self.router_ip}:{self.admin_port}",
                timeout=self.timeout,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for router model indicators
                for model, name in self.supported_models.items():
                    if model in content or name.lower() in content:
                        self.logger.info(f"Detected router model: {name}")
                        return model
            
            # Try common router URLs
            common_urls = [
                "/login.asp", "/login.html", "/admin/", "/setup/",
                "/index.asp", "/index.html", "/router/", "/config/"
            ]
            
            for url in common_urls:
                try:
                    response = requests.get(
                        f"http://{self.router_ip}:{self.admin_port}{url}",
                        timeout=5
                    )
                    if response.status_code == 200:
                        content = response.text.lower()
                        for model, name in self.supported_models.items():
                            if model in content or name.lower() in content:
                                self.logger.info(f"Detected router model: {name}")
                                return model
                except:
                    continue
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error detecting router model: {e}")
            return None
    
    def connect_http(self) -> bool:
        """Connect to router using HTTP requests"""
        if not REQUESTS_AVAILABLE:
            self.logger.error("Requests library not available")
            return False
        
        try:
            # Create session
            self.session = requests.Session()
            
            # Try to get login page
            response = self.session.get(
                f"http://{self.router_ip}:{self.admin_port}",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                self.logger.info("Successfully connected to router via HTTP")
                self.connected = True
                return True
            else:
                self.logger.error(f"Failed to connect to router: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error connecting to router via HTTP: {e}")
            return False
    
    def connect_selenium(self, browser: str = "chrome") -> bool:
        """Connect to router using Selenium browser automation"""
        if not SELENIUM_AVAILABLE:
            self.logger.error("Selenium not available")
            return False
        
        try:
            if browser.lower() == "chrome":
                options = Options()
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                
                if is_windows():
                    self.driver = webdriver.Chrome(options=options)
                else:
                    self.driver = webdriver.Chrome(options=options)
                    
            elif browser.lower() == "firefox":
                options = FirefoxOptions()
                options.add_argument("--headless")
                
                if is_windows():
                    self.driver = webdriver.Firefox(options=options)
                else:
                    self.driver = webdriver.Firefox(options=options)
            else:
                self.logger.error(f"Unsupported browser: {browser}")
                return False
            
            # Navigate to router
            self.driver.get(f"http://{self.router_ip}:{self.admin_port}")
            
            # Wait for page to load
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            self.logger.info(f"Successfully connected to router via {browser}")
            self.connected = True
            return True
            
        except Exception as e:
            self.logger.error(f"Error connecting to router via Selenium: {e}")
            if self.driver:
                self.driver.quit()
                self.driver = None
            return False
    
    def login(self, username: str = None, password: str = None) -> bool:
        """Login to router admin panel"""
        if not self.connected:
            self.logger.error("Not connected to router")
            return False
        
        username = username or self.username
        password = password or self.password
        
        if not username or not password:
            self.logger.error("Username and password required for login")
            return False
        
        try:
            if self.session:  # HTTP method
                return self._login_http(username, password)
            elif self.driver:  # Selenium method
                return self._login_selenium(username, password)
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Error during login: {e}")
            return False
    
    def _login_http(self, username: str, password: str) -> bool:
        """Login using HTTP POST"""
        try:
            # Common login endpoints
            login_endpoints = [
                "/login.asp", "/login.html", "/admin/login.asp",
                "/admin/login.html", "/login.cgi", "/auth.cgi"
            ]
            
            login_data = {
                "username": username,
                "password": password,
                "submit": "Login",
                "login": "Login"
            }
            
            for endpoint in login_endpoints:
                try:
                    response = self.session.post(
                        f"http://{self.router_ip}:{self.admin_port}{endpoint}",
                        data=login_data,
                        timeout=self.timeout
                    )
                    
                    if response.status_code == 200:
                        # Check if login was successful
                        if "logout" in response.text.lower() or "admin" in response.text.lower():
                            self.logger.info("Successfully logged in via HTTP")
                            return True
                except:
                    continue
            
            self.logger.error("Failed to login via HTTP")
            return False
            
        except Exception as e:
            self.logger.error(f"Error during HTTP login: {e}")
            return False
    
    def _login_selenium(self, username: str, password: str) -> bool:
        """Login using Selenium"""
        try:
            # Common username/password field selectors
            username_selectors = [
                "input[name='username']", "input[name='user']", "input[name='login']",
                "input[id='username']", "input[id='user']", "input[id='login']",
                "input[type='text']"
            ]
            
            password_selectors = [
                "input[name='password']", "input[name='pass']", "input[name='pwd']",
                "input[id='password']", "input[id='pass']", "input[id='pwd']",
                "input[type='password']"
            ]
            
            submit_selectors = [
                "input[type='submit']", "button[type='submit']", "input[value*='Login']",
                "button:contains('Login')", "input[value*='Submit']"
            ]
            
            # Find and fill username field
            username_field = None
            for selector in username_selectors:
                try:
                    username_field = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not username_field:
                self.logger.error("Could not find username field")
                return False
            
            # Find and fill password field
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not password_field:
                self.logger.error("Could not find password field")
                return False
            
            # Fill in credentials
            username_field.clear()
            username_field.send_keys(username)
            
            password_field.clear()
            password_field.send_keys(password)
            
            # Find and click submit button
            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not submit_button:
                self.logger.error("Could not find submit button")
                return False
            
            submit_button.click()
            
            # Wait for login to complete
            time.sleep(3)
            
            # Check if login was successful
            if "logout" in self.driver.page_source.lower() or "admin" in self.driver.page_source.lower():
                self.logger.info("Successfully logged in via Selenium")
                return True
            else:
                self.logger.error("Login failed - check credentials")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during Selenium login: {e}")
            return False
    
    def get_connected_devices(self) -> List[RouterDevice]:
        """Get list of devices connected to the router"""
        if not self.connected:
            self.logger.error("Not connected to router")
            return []
        
        try:
            if self.session:
                return self._get_devices_http()
            elif self.driver:
                return self._get_devices_selenium()
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Error getting connected devices: {e}")
            return []
    
    def _get_devices_http(self) -> List[RouterDevice]:
        """Get devices using HTTP requests"""
        devices = []
        
        try:
            # Common device list endpoints
            device_endpoints = [
                "/admin/connected_devices.asp", "/admin/devices.asp",
                "/admin/attached_devices.asp", "/admin/device_list.asp",
                "/devices.asp", "/attached_devices.asp"
            ]
            
            for endpoint in device_endpoints:
                try:
                    response = self.session.get(
                        f"http://{self.router_ip}:{self.admin_port}{endpoint}",
                        timeout=self.timeout
                    )
                    
                    if response.status_code == 200:
                        # Parse device information from HTML
                        devices = self._parse_devices_html(response.text)
                        if devices:
                            break
                except:
                    continue
            
            return devices
            
        except Exception as e:
            self.logger.error(f"Error getting devices via HTTP: {e}")
            return []
    
    def _get_devices_selenium(self) -> List[RouterDevice]:
        """Get devices using Selenium"""
        devices = []
        
        try:
            # Navigate to device list page
            device_urls = [
                f"http://{self.router_ip}:{self.admin_port}/admin/connected_devices.asp",
                f"http://{self.router_ip}:{self.admin_port}/admin/devices.asp",
                f"http://{self.router_ip}:{self.admin_port}/admin/attached_devices.asp"
            ]
            
            for url in device_urls:
                try:
                    self.driver.get(url)
                    time.sleep(2)
                    
                    # Parse devices from current page
                    devices = self._parse_devices_selenium()
                    if devices:
                        break
                except:
                    continue
            
            return devices
            
        except Exception as e:
            self.logger.error(f"Error getting devices via Selenium: {e}")
            return []
    
    def _parse_devices_html(self, html: str) -> List[RouterDevice]:
        """Parse device information from HTML"""
        devices = []
        
        try:
            # This is a simplified parser - in production you'd use BeautifulSoup
            # Look for common patterns in router admin pages
            
            # Extract MAC addresses
            mac_pattern = r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})'
            macs = re.findall(mac_pattern, html)
            
            # Extract IP addresses
            ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            ips = re.findall(ip_pattern, html)
            
            # Extract hostnames
            hostname_pattern = r'<td[^>]*>([^<]+)</td>'
            hostnames = re.findall(hostname_pattern, html)
            
            # Create device objects
            for i, mac in enumerate(macs):
                if i < len(ips) and i < len(hostnames):
                    device = RouterDevice(
                        mac=mac[0] + mac[1],
                        ip=ips[i],
                        hostname=hostnames[i].strip(),
                        status="connected",
                        connection_time=datetime.now(),
                        data_usage=0
                    )
                    devices.append(device)
            
            return devices
            
        except Exception as e:
            self.logger.error(f"Error parsing devices HTML: {e}")
            return []
    
    def _parse_devices_selenium(self) -> List[RouterDevice]:
        """Parse device information using Selenium"""
        devices = []
        
        try:
            # Look for device table rows
            device_rows = self.driver.find_elements(By.CSS_SELECTOR, "tr")
            
            for row in device_rows:
                try:
                    cells = row.find_elements(By.CSS_SELECTOR, "td")
                    if len(cells) >= 3:
                        # Extract device information from table cells
                        hostname = cells[0].text.strip() if len(cells) > 0 else "Unknown"
                        ip = cells[1].text.strip() if len(cells) > 1 else ""
                        mac = cells[2].text.strip() if len(cells) > 2 else ""
                        
                        if mac and validate_mac_address(mac):
                            device = RouterDevice(
                                mac=mac,
                                ip=ip,
                                hostname=hostname,
                                status="connected",
                                connection_time=datetime.now(),
                                data_usage=0
                            )
                            devices.append(device)
                except:
                    continue
            
            return devices
            
        except Exception as e:
            self.logger.error(f"Error parsing devices via Selenium: {e}")
            return []
    
    def block_device(self, mac: str, duration_hours: int = 24) -> bool:
        """Block a device from the network"""
        if not self.connected:
            self.logger.error("Not connected to router")
            return False
        
        try:
            if self.session:
                return self._block_device_http(mac, duration_hours)
            elif self.driver:
                return self._block_device_selenium(mac, duration_hours)
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Error blocking device {mac}: {e}")
            return False
    
    def _block_device_http(self, mac: str, duration_hours: int) -> bool:
        """Block device using HTTP requests"""
        try:
            # Common block device endpoints
            block_endpoints = [
                "/admin/block_device.asp", "/admin/block.asp",
                "/admin/access_control.asp", "/admin/firewall.asp"
            ]
            
            block_data = {
                "mac": mac,
                "action": "block",
                "duration": str(duration_hours),
                "submit": "Block Device"
            }
            
            for endpoint in block_endpoints:
                try:
                    response = self.session.post(
                        f"http://{self.router_ip}:{self.admin_port}{endpoint}",
                        data=block_data,
                        timeout=self.timeout
                    )
                    
                    if response.status_code == 200:
                        self.logger.info(f"Successfully blocked device {mac}")
                        return True
                except:
                    continue
            
            self.logger.error(f"Failed to block device {mac} via HTTP")
            return False
            
        except Exception as e:
            self.logger.error(f"Error blocking device via HTTP: {e}")
            return False
    
    def _block_device_selenium(self, mac: str, duration_hours: int) -> bool:
        """Block device using Selenium"""
        try:
            # Navigate to access control page
            control_urls = [
                f"http://{self.router_ip}:{self.admin_port}/admin/access_control.asp",
                f"http://{self.router_ip}:{self.admin_port}/admin/firewall.asp",
                f"http://{self.router_ip}:{self.admin_port}/admin/block_device.asp"
            ]
            
            for url in control_urls:
                try:
                    self.driver.get(url)
                    time.sleep(2)
                    
                    # Look for block device form
                    mac_field = None
                    for selector in ["input[name='mac']", "input[id='mac']", "input[placeholder*='MAC']"]:
                        try:
                            mac_field = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                            )
                            break
                        except:
                            continue
                    
                    if mac_field:
                        # Fill in MAC address
                        mac_field.clear()
                        mac_field.send_keys(mac)
                        
                        # Find and click block button
                        block_button = None
                        for selector in ["input[value*='Block']", "button:contains('Block')", "input[type='submit']"]:
                            try:
                                block_button = WebDriverWait(self.driver, 5).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                                )
                                break
                            except:
                                continue
                        
                        if block_button:
                            block_button.click()
                            time.sleep(2)
                            
                            self.logger.info(f"Successfully blocked device {mac}")
                            return True
                except:
                    continue
            
            self.logger.error(f"Failed to block device {mac} via Selenium")
            return False
            
        except Exception as e:
            self.logger.error(f"Error blocking device via Selenium: {e}")
            return False
    
    def unblock_device(self, mac: str) -> bool:
        """Unblock a device from the network"""
        if not self.connected:
            self.logger.error("Not connected to router")
            return False
        
        try:
            if self.session:
                return self._unblock_device_http(mac)
            elif self.driver:
                return self._unblock_device_selenium(mac)
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Error unblocking device {mac}: {e}")
            return False
    
    def _unblock_device_http(self, mac: str) -> bool:
        """Unblock device using HTTP requests"""
        try:
            # Similar to block but with action="unblock"
            unblock_data = {
                "mac": mac,
                "action": "unblock",
                "submit": "Unblock Device"
            }
            
            # Try common endpoints
            unblock_endpoints = [
                "/admin/block_device.asp", "/admin/access_control.asp"
            ]
            
            for endpoint in unblock_endpoints:
                try:
                    response = self.session.post(
                        f"http://{self.router_ip}:{self.admin_port}{endpoint}",
                        data=unblock_data,
                        timeout=self.timeout
                    )
                    
                    if response.status_code == 200:
                        self.logger.info(f"Successfully unblocked device {mac}")
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error unblocking device via HTTP: {e}")
            return False
    
    def _unblock_device_selenium(self, mac: str) -> bool:
        """Unblock device using Selenium"""
        # Similar to block but look for unblock button
        try:
            # Navigate to blocked devices list
            self.driver.get(f"http://{self.router_ip}:{self.admin_port}/admin/blocked_devices.asp")
            time.sleep(2)
            
            # Look for unblock button for this MAC
            unblock_buttons = self.driver.find_elements(By.CSS_SELECTOR, "input[value*='Unblock'], button:contains('Unblock')")
            
            for button in unblock_buttons:
                try:
                    # Check if this button is for our MAC
                    row = button.find_element(By.XPATH, "./ancestor::tr")
                    if mac in row.text:
                        button.click()
                        time.sleep(2)
                        
                        self.logger.info(f"Successfully unblocked device {mac}")
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error unblocking device via Selenium: {e}")
            return False
    
    def change_wifi_password(self, new_password: str) -> bool:
        """Change Wi-Fi password"""
        if not self.connected:
            self.logger.error("Not connected to router")
            return False
        
        try:
            if self.session:
                return self._change_password_http(new_password)
            elif self.driver:
                return self._change_password_selenium(new_password)
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Error changing Wi-Fi password: {e}")
            return False
    
    def _change_password_http(self, new_password: str) -> bool:
        """Change password using HTTP requests"""
        try:
            # Common password change endpoints
            password_endpoints = [
                "/admin/wireless.asp", "/admin/wifi.asp",
                "/admin/security.asp", "/admin/password.asp"
            ]
            
            password_data = {
                "password": new_password,
                "confirm_password": new_password,
                "submit": "Save Changes",
                "action": "update"
            }
            
            for endpoint in password_endpoints:
                try:
                    response = self.session.post(
                        f"http://{self.router_ip}:{self.admin_port}{endpoint}",
                        data=password_data,
                        timeout=self.timeout
                    )
                    
                    if response.status_code == 200:
                        self.logger.info("Successfully changed Wi-Fi password")
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error changing password via HTTP: {e}")
            return False
    
    def _change_password_selenium(self, new_password: str) -> bool:
        """Change password using Selenium"""
        try:
            # Navigate to wireless settings
            wireless_urls = [
                f"http://{self.router_ip}:{self.admin_port}/admin/wireless.asp",
                f"http://{self.router_ip}:{self.admin_port}/admin/wifi.asp"
            ]
            
            for url in wireless_urls:
                try:
                    self.driver.get(url)
                    time.sleep(2)
                    
                    # Find password field
                    password_field = None
                    for selector in ["input[name='password']", "input[name='wpa_psk']", "input[id='password']"]:
                        try:
                            password_field = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                            )
                            break
                        except:
                            continue
                    
                    if password_field:
                        # Fill in new password
                        password_field.clear()
                        password_field.send_keys(new_password)
                        
                        # Find and click save button
                        save_button = None
                        for selector in ["input[value*='Save']", "button:contains('Save')", "input[type='submit']"]:
                            try:
                                save_button = WebDriverWait(self.driver, 5).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                                )
                                break
                            except:
                                continue
                        
                        if save_button:
                            save_button.click()
                            time.sleep(3)
                            
                            self.logger.info("Successfully changed Wi-Fi password")
                            return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error changing password via Selenium: {e}")
            return False
    
    def set_speed_limit(self, mac: str, speed_mbps: int) -> bool:
        """Set speed limit for a specific device"""
        if not self.connected:
            self.logger.error("Not connected to router")
            return False
        
        try:
            if self.session:
                return self._set_speed_limit_http(mac, speed_mbps)
            elif self.driver:
                return self._set_speed_limit_selenium(mac, speed_mbps)
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Error setting speed limit for {mac}: {e}")
            return False
    
    def _set_speed_limit_http(self, mac: str, speed_mbps: int) -> bool:
        """Set speed limit using HTTP requests"""
        try:
            # Common QoS/bandwidth control endpoints
            qos_endpoints = [
                "/admin/qos.asp", "/admin/bandwidth.asp",
                "/admin/traffic_control.asp", "/admin/priority.asp"
            ]
            
            qos_data = {
                "mac": mac,
                "speed_limit": str(speed_mbps),
                "action": "set_limit",
                "submit": "Apply"
            }
            
            for endpoint in qos_endpoints:
                try:
                    response = self.session.post(
                        f"http://{self.router_ip}:{self.admin_port}{endpoint}",
                        data=qos_data,
                        timeout=self.timeout
                    )
                    
                    if response.status_code == 200:
                        self.logger.info(f"Successfully set speed limit for {mac}")
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error setting speed limit via HTTP: {e}")
            return False
    
    def _set_speed_limit_selenium(self, mac: str, speed_mbps: int) -> bool:
        """Set speed limit using Selenium"""
        try:
            # Navigate to QoS settings
            qos_urls = [
                f"http://{self.router_ip}:{self.admin_port}/admin/qos.asp",
                f"http://{self.router_ip}:{self.admin_port}/admin/bandwidth.asp"
            ]
            
            for url in qos_urls:
                try:
                    self.driver.get(url)
                    time.sleep(2)
                    
                    # Find device selection
                    device_select = None
                    for selector in ["select[name='device']", "select[id='device']", "input[name='mac']"]:
                        try:
                            device_select = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                            )
                            break
                        except:
                            continue
                    
                    if device_select:
                        # Select device and set speed limit
                        if device_select.tag_name == "select":
                            # Dropdown selection
                            for option in device_select.find_elements(By.TAG_NAME, "option"):
                                if mac in option.text:
                                    option.click()
                                    break
                        else:
                            # Text input
                            device_select.clear()
                            device_select.send_keys(mac)
                        
                        # Find speed limit field
                        speed_field = None
                        for selector in ["input[name='speed']", "input[name='limit']", "input[id='speed']"]:
                            try:
                                speed_field = WebDriverWait(self.driver, 5).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                )
                                break
                            except:
                                continue
                        
                        if speed_field:
                            speed_field.clear()
                            speed_field.send_keys(str(speed_mbps))
                            
                            # Find and click apply button
                            apply_button = None
                            for selector in ["input[value*='Apply']", "button:contains('Apply')", "input[type='submit']"]:
                                try:
                                    apply_button = WebDriverWait(self.driver, 5).until(
                                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                                    )
                                    break
                                except:
                                    continue
                            
                            if apply_button:
                                apply_button.click()
                                time.sleep(2)
                                
                                self.logger.info(f"Successfully set speed limit for {mac}")
                                return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error setting speed limit via Selenium: {e}")
            return False
    
    def get_router_settings(self) -> Optional[RouterSettings]:
        """Get current router settings"""
        if not self.connected:
            self.logger.error("Not connected to router")
            return None
        
        try:
            if self.session:
                return self._get_settings_http()
            elif self.driver:
                return self._get_settings_selenium()
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting router settings: {e}")
            return None
    
    def _get_settings_http(self) -> Optional[RouterSettings]:
        """Get settings using HTTP requests"""
        # Implementation would parse router configuration pages
        # This is a placeholder for the actual implementation
        return None
    
    def _get_settings_selenium(self) -> Optional[RouterSettings]:
        """Get settings using Selenium"""
        # Implementation would navigate to settings pages and extract information
        # This is a placeholder for the actual implementation
        return None
    
    def disconnect(self) -> None:
        """Disconnect from router"""
        try:
            if self.session:
                self.session.close()
                self.session = None
            
            if self.driver:
                self.driver.quit()
                self.driver = None
            
            self.connected = False
            self.logger.info("Disconnected from router")
            
        except Exception as e:
            self.logger.error(f"Error disconnecting from router: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get router connection status"""
        return {
            "connected": self.connected,
            "router_ip": self.router_ip,
            "admin_port": self.admin_port,
            "connection_method": "HTTP" if self.session else "Selenium" if self.driver else "None",
            "devices_count": len(self.devices),
            "last_scan": datetime.now().isoformat() if self.connected else None
        }
