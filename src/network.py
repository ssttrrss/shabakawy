#!/usr/bin/env python3
"""
Shabakawy Network Security Module
Network scanning, packet inspection, threat detection, and countermeasures
"""

import time
import logging
import threading
from typing import Dict, List, Optional, Callable, Tuple
from dataclasses import dataclass
from datetime import datetime
import ipaddress
import queue

try:
    from scapy.all import *
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    logging.warning("Scapy not available. Packet capture features will be limited.")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logging.warning("psutil not available. Some network features will be limited.")

from utils import (
    get_platform_info, is_windows, is_linux, run_command,
    get_default_gateway, validate_ip_address, validate_mac_address
)

@dataclass
class NetworkDevice:
    """Represents a device on the network"""
    ip: str
    mac: str
    hostname: str
    vendor: str
    first_seen: datetime
    last_seen: datetime
    status: str  # "online", "offline", "suspicious"
    threat_level: int  # 0-10, where 10 is highest threat
    connection_count: int
    data_transferred: int
    ports_open: List[int]

@dataclass
class SecurityThreat:
    """Represents a detected security threat"""
    threat_type: str  # "ddos", "mitm", "spoofing", "anomaly"
    severity: str  # "low", "medium", "high", "critical"
    description: str
    timestamp: datetime
    source_ip: str
    source_mac: str
    evidence: Dict
    mitigated: bool = False

class NetworkScanner:
    """Network scanner for discovering devices and monitoring activity"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.devices: Dict[str, NetworkDevice] = {}
        self.threats: List[SecurityThreat] = []
        self.scanning = False
        self.packet_capture_active = False
        self.callback_queue = queue.Queue()
        
        # Threat detection thresholds
        self.ddos_threshold = int(config.get("ddos_threshold", 1000))
        self.mitm_detection = config.get("mitm_detection", "true").lower() == "true"
        self.auto_block = config.get("auto_block", "true").lower() == "true"
        
        # Statistics
        self.packets_captured = 0
        self.threats_detected = 0
        self.devices_blocked = 0
        
        self.logger = logging.getLogger(__name__)
    
    def start_scanning(self, callback: Optional[Callable] = None) -> bool:
        """Start continuous network scanning"""
        if self.scanning:
            return False
        
        self.scanning = True
        self.logger.info("Starting network scanning...")
        
        # Start scanning thread
        scan_thread = threading.Thread(
            target=self._scan_loop,
            args=(callback,),
            daemon=True
        )
        scan_thread.start()
        
        return True
    
    def stop_scanning(self) -> None:
        """Stop network scanning"""
        self.scanning = False
        self.logger.info("Stopping network scanning...")
    
    def _scan_loop(self, callback: Optional[Callable]) -> None:
        """Main scanning loop"""
        while self.scanning:
            try:
                # Perform network scan
                new_devices = self._perform_network_scan()
                
                # Update device list
                self._update_devices(new_devices)
                
                # Check for threats
                self._check_for_threats()
                
                # Call callback if provided
                if callback:
                    callback(self.devices, self.threats)
                
                # Wait before next scan
                time.sleep(int(self.config.get("scan_interval", 30)))
                
            except Exception as e:
                self.logger.error(f"Error in scan loop: {e}")
                time.sleep(5)
    
    def _perform_network_scan(self) -> List[NetworkDevice]:
        """Perform a network scan to discover devices"""
        devices = []
        
        try:
            # Get network range
            gateway = get_default_gateway()
            if not gateway:
                self.logger.error("Could not determine default gateway")
                return devices
            
            # Determine network range (assuming /24 for now)
            network = ipaddress.IPv4Network(f"{gateway}/24", strict=False)
            
            # Scan common ports
            common_ports = [22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
            
            for ip in network.hosts():
                ip_str = str(ip)
                
                # Skip gateway and broadcast
                if ip_str == gateway or ip_str.endswith('.255'):
                    continue
                
                # Check if device is online
                if self._ping_device(ip_str):
                    device = self._get_device_info(ip_str, common_ports)
                    if device:
                        devices.append(device)
        
        except Exception as e:
            self.logger.error(f"Error during network scan: {e}")
        
        return devices
    
    def _ping_device(self, ip: str) -> bool:
        """Ping a device to check if it's online"""
        try:
            if is_windows():
                cmd = ["ping", "-n", "1", "-w", "1000", ip]
            else:
                cmd = ["ping", "-c", "1", "-W", "1", ip]
            
            returncode, _, _ = run_command(cmd, timeout=2)
            return returncode == 0
            
        except Exception:
            return False
    
    def _get_device_info(self, ip: str, ports: List[int]) -> Optional[NetworkDevice]:
        """Get detailed information about a device"""
        try:
            # Get MAC address
            mac = self._get_mac_address(ip)
            if not mac:
                return None
            
            # Get hostname
            hostname = self._get_hostname(ip)
            
            # Get vendor from MAC
            vendor = self._get_vendor_from_mac(mac)
            
            # Check open ports
            open_ports = self._scan_ports(ip, ports)
            
            # Check if device already exists
            if mac in self.devices:
                device = self.devices[mac]
                device.last_seen = datetime.now()
                device.status = "online"
                device.ports_open = open_ports
                return device
            
            # Create new device
            device = NetworkDevice(
                ip=ip,
                mac=mac,
                hostname=hostname or "Unknown",
                vendor=vendor or "Unknown",
                first_seen=datetime.now(),
                last_seen=datetime.now(),
                status="online",
                threat_level=0,
                connection_count=0,
                data_transferred=0,
                ports_open=open_ports
            )
            
            return device
            
        except Exception as e:
            self.logger.error(f"Error getting device info for {ip}: {e}")
            return None
    
    def _get_mac_address(self, ip: str) -> Optional[str]:
        """Get MAC address for an IP address"""
        try:
            if is_windows():
                # Windows: use arp -a
                cmd = ["arp", "-a", ip]
            else:
                # Linux: use arp -n
                cmd = ["arp", "-n", ip]
            
            returncode, stdout, _ = run_command(cmd, timeout=5)
            if returncode == 0:
                lines = stdout.split('\n')
                for line in lines:
                    if ip in line:
                        parts = line.split()
                        for part in parts:
                            if validate_mac_address(part):
                                return part
        except Exception:
            pass
        
        return None
    
    def _get_hostname(self, ip: str) -> Optional[str]:
        """Get hostname for an IP address"""
        try:
            if is_windows():
                cmd = ["nbtstat", "-A", ip]
            else:
                cmd = ["nslookup", ip]
            
            returncode, stdout, _ = run_command(cmd, timeout=5)
            if returncode == 0:
                # Simple parsing - could be improved
                lines = stdout.split('\n')
                for line in lines:
                    if 'Name:' in line or 'name =' in line:
                        parts = line.split()
                        for part in parts:
                            if '.' in part and not validate_ip_address(part):
                                return part.split('.')[0]
        except Exception:
            pass
        
        return None
    
    def _get_vendor_from_mac(self, mac: str) -> Optional[str]:
        """Get vendor information from MAC address OUI"""
        # This is a simplified version - in production you'd use a proper OUI database
        try:
            # Extract OUI (first 6 characters)
            oui = mac.replace(':', '').replace('-', '')[:6].upper()
            
            # Common vendor OUIs (this is just a small sample)
            vendors = {
                '000C29': 'VMware',
                '001A11': 'Google',
                '002272': 'American Micro-Fuel Device Corp',
                '00AABB': 'Cisco',
                '00E018': 'Arris',
                '080027': 'PCS Systemtechnik GmbH',
                '080020': 'Sun Microsystems',
                '080010': 'Omron Tateisi Electronics Co',
                '080009': 'Hewlett-Packard',
                '080006': 'Xerox'
            }
            
            return vendors.get(oui, "Unknown")
            
        except Exception:
            return "Unknown"
    
    def _scan_ports(self, ip: str, ports: List[int]) -> List[int]:
        """Scan for open ports on a device"""
        open_ports = []
        
        try:
            for port in ports:
                if self._is_port_open(ip, port):
                    open_ports.append(port)
        except Exception as e:
            self.logger.error(f"Error scanning ports for {ip}: {e}")
        
        return open_ports
    
    def _is_port_open(self, ip: str, port: int) -> bool:
        """Check if a specific port is open"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def _update_devices(self, new_devices: List[NetworkDevice]) -> None:
        """Update the device list with new scan results"""
        current_macs = set()
        
        # Update existing devices and add new ones
        for device in new_devices:
            current_macs.add(device.mac)
            self.devices[device.mac] = device
        
        # Mark offline devices
        for mac, device in self.devices.items():
            if mac not in current_macs:
                device.status = "offline"
                device.last_seen = datetime.now()
    
    def _check_for_threats(self) -> None:
        """Check for various security threats"""
        self._check_ddos_attacks()
        self._check_mitm_attacks()
        self._check_mac_spoofing()
        self._check_anomalies()
    
    def _check_ddos_attacks(self) -> None:
        """Check for DDoS attacks based on connection patterns"""
        try:
            for mac, device in self.devices.items():
                if device.status == "online":
                    # Simple DDoS detection based on connection count
                    if device.connection_count > self.ddos_threshold:
                        threat = SecurityThreat(
                            threat_type="ddos",
                            severity="high" if device.connection_count > self.ddos_threshold * 2 else "medium",
                            description=f"Potential DDoS attack from {device.ip} ({device.hostname})",
                            timestamp=datetime.now(),
                            source_ip=device.ip,
                            source_mac=device.mac,
                            evidence={
                                "connection_count": device.connection_count,
                                "threshold": self.ddos_threshold,
                                "device_info": {
                                    "hostname": device.hostname,
                                    "vendor": device.vendor
                                }
                            }
                        )
                        
                        self.threats.append(threat)
                        self.threats_detected += 1
                        
                        # Auto-block if enabled
                        if self.auto_block:
                            self._block_device(mac)
                        
                        self.logger.warning(f"DDoS threat detected: {threat.description}")
        
        except Exception as e:
            self.logger.error(f"Error checking for DDoS attacks: {e}")
    
    def _check_mitm_attacks(self) -> None:
        """Check for Man-in-the-Middle attacks"""
        if not self.mitm_detection:
            return
        
        try:
            # This is a simplified MITM detection
            # In production, you'd implement more sophisticated detection
            for mac, device in self.devices.items():
                if device.status == "online":
                    # Check for suspicious ARP behavior
                    if self._check_suspicious_arp(device):
                        threat = SecurityThreat(
                            threat_type="mitm",
                            severity="critical",
                            description=f"Potential MITM attack from {device.ip} ({device.hostname})",
                            timestamp=datetime.now(),
                            source_ip=device.ip,
                            source_mac=device.mac,
                            evidence={
                                "arp_anomaly": True,
                                "device_info": {
                                    "hostname": device.hostname,
                                    "vendor": device.vendor
                                }
                            }
                        )
                        
                        self.threats.append(threat)
                        self.threats_detected += 1
                        
                        if self.auto_block:
                            self._block_device(mac)
                        
                        self.logger.warning(f"MITM threat detected: {threat.description}")
        
        except Exception as e:
            self.logger.error(f"Error checking for MITM attacks: {e}")
    
    def _check_suspicious_arp(self, device: NetworkDevice) -> bool:
        """Check for suspicious ARP behavior"""
        # This is a placeholder - implement actual ARP monitoring
        # In production, you'd monitor ARP tables for inconsistencies
        return False
    
    def _check_mac_spoofing(self) -> None:
        """Check for MAC address spoofing"""
        try:
            # Check for duplicate MAC addresses
            mac_count = {}
            for mac, device in self.devices.items():
                if device.status == "online":
                    mac_count[mac] = mac_count.get(mac, 0) + 1
            
            for mac, count in mac_count.items():
                if count > 1:
                    threat = SecurityThreat(
                        threat_type="spoofing",
                        severity="high",
                        description=f"MAC address spoofing detected: {mac} appears {count} times",
                        timestamp=datetime.now(),
                        source_ip="Multiple",
                        source_mac=mac,
                        evidence={
                            "duplicate_count": count,
                            "affected_devices": [
                                d.ip for d in self.devices.values() 
                                if d.mac == mac and d.status == "online"
                            ]
                        }
                    )
                    
                    self.threats.append(threat)
                    self.threats_detected += 1
                    
                    self.logger.warning(f"MAC spoofing detected: {threat.description}")
        
        except Exception as e:
            self.logger.error(f"Error checking for MAC spoofing: {e}")
    
    def _check_anomalies(self) -> None:
        """Check for general network anomalies"""
        try:
            # Check for devices with unusual behavior
            for mac, device in self.devices.items():
                if device.status == "online":
                    # Check for devices with many open ports (potential scanning)
                    if len(device.ports_open) > 10:
                        threat = SecurityThreat(
                            threat_type="anomaly",
                            severity="medium",
                            description=f"Device {device.ip} has {len(device.ports_open)} open ports",
                            timestamp=datetime.now(),
                            source_ip=device.ip,
                            source_mac=device.mac,
                            evidence={
                                "open_ports": device.ports_open,
                                "port_count": len(device.ports_open),
                                "device_info": {
                                    "hostname": device.hostname,
                                    "vendor": device.vendor
                                }
                            }
                        )
                        
                        self.threats.append(threat)
                        self.threats_detected += 1
                        
                        self.logger.warning(f"Anomaly detected: {threat.description}")
        
        except Exception as e:
            self.logger.error(f"Error checking for anomalies: {e}")
    
    def _block_device(self, mac: str) -> bool:
        """Block a device from the network"""
        try:
            # This is a placeholder - implement actual blocking
            # In production, you'd integrate with router APIs or firewall rules
            
            if mac in self.devices:
                self.devices[mac].status = "blocked"
                self.devices_blocked += 1
                self.logger.info(f"Device {mac} has been blocked")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error blocking device {mac}: {e}")
            return False
    
    def start_packet_capture(self, interface: str = None) -> bool:
        """Start packet capture for deep inspection"""
        if not SCAPY_AVAILABLE:
            self.logger.error("Scapy not available for packet capture")
            return False
        
        if self.packet_capture_active:
            return False
        
        try:
            self.packet_capture_active = True
            
            # Start packet capture in separate thread
            capture_thread = threading.Thread(
                target=self._packet_capture_loop,
                args=(interface,),
                daemon=True
            )
            capture_thread.start()
            
            self.logger.info(f"Started packet capture on interface: {interface or 'default'}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting packet capture: {e}")
            self.packet_capture_active = False
            return False
    
    def stop_packet_capture(self) -> None:
        """Stop packet capture"""
        self.packet_capture_active = False
        self.logger.info("Stopped packet capture")
    
    def _packet_capture_loop(self, interface: str = None) -> None:
        """Main packet capture loop"""
        try:
            # Use Scapy to capture packets
            sniff(
                iface=interface,
                prn=self._process_packet,
                store=0,
                stop_filter=lambda x: not self.packet_capture_active
            )
        except Exception as e:
            self.logger.error(f"Error in packet capture loop: {e}")
    
    def _process_packet(self, packet) -> None:
        """Process a captured packet"""
        try:
            self.packets_captured += 1
            
            # Analyze packet for threats
            if self._analyze_packet_threats(packet):
                self.logger.debug(f"Threat detected in packet {self.packets_captured}")
            
            # Update device statistics
            self._update_device_stats(packet)
            
        except Exception as e:
            self.logger.error(f"Error processing packet: {e}")
    
    def _analyze_packet_threats(self, packet) -> bool:
        """Analyze packet for security threats"""
        try:
            # Check for suspicious patterns
            if packet.haslayer(IP):
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                
                # Check for port scanning
                if packet.haslayer(TCP):
                    flags = packet[TCP].flags
                    if flags == 2:  # SYN flag only (port scan indicator)
                        self._detect_port_scan(src_ip)
                
                # Check for suspicious payloads
                if packet.haslayer(Raw):
                    payload = str(packet[Raw].load)
                    if any(suspicious in payload.lower() for suspicious in ['exploit', 'shell', 'root']):
                        self._detect_suspicious_payload(src_ip, payload)
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error analyzing packet threats: {e}")
            return False
    
    def _detect_port_scan(self, src_ip: str) -> None:
        """Detect port scanning activity"""
        # Update device statistics
        for device in self.devices.values():
            if device.ip == src_ip:
                device.threat_level = min(device.threat_level + 1, 10)
                break
    
    def _detect_suspicious_payload(self, src_ip: str, payload: str) -> None:
        """Detect suspicious payload content"""
        threat = SecurityThreat(
            threat_type="anomaly",
            severity="medium",
            description=f"Suspicious payload detected from {src_ip}",
            timestamp=datetime.now(),
            source_ip=src_ip,
            source_mac="Unknown",
            evidence={
                "payload_preview": payload[:100],
                "payload_length": len(payload)
            }
        )
        
        self.threats.append(threat)
        self.threats_detected += 1
    
    def _update_device_stats(self, packet) -> None:
        """Update device statistics from packet"""
        try:
            if packet.haslayer(IP):
                src_ip = packet[IP].src
                
                # Find device and update stats
                for device in self.devices.values():
                    if device.ip == src_ip:
                        device.connection_count += 1
                        if packet.haslayer(Raw):
                            device.data_transferred += len(packet[Raw].load)
                        break
                        
        except Exception as e:
            self.logger.error(f"Error updating device stats: {e}")
    
    def get_network_summary(self) -> Dict:
        """Get a summary of network status"""
        online_devices = sum(1 for d in self.devices.values() if d.status == "online")
        offline_devices = sum(1 for d in self.devices.values() if d.status == "offline")
        blocked_devices = sum(1 for d in self.devices.values() if d.status == "blocked")
        
        active_threats = sum(1 for t in self.threats if not t.mitigated)
        
        return {
            "total_devices": len(self.devices),
            "online_devices": online_devices,
            "offline_devices": offline_devices,
            "blocked_devices": blocked_devices,
            "active_threats": active_threats,
            "total_threats": len(self.threats),
            "packets_captured": self.packets_captured,
            "devices_blocked": self.devices_blocked,
            "scan_status": "active" if self.scanning else "inactive",
            "capture_status": "active" if self.packet_capture_active else "inactive"
        }
    
    def get_device_list(self) -> List[NetworkDevice]:
        """Get list of all devices"""
        return list(self.devices.values())
    
    def get_threats(self) -> List[SecurityThreat]:
        """Get list of all threats"""
        return self.threats.copy()
    
    def clear_threats(self) -> None:
        """Clear all threats"""
        self.threats.clear()
        self.threats_detected = 0
        self.logger.info("All threats cleared")
