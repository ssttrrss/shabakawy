#!/usr/bin/env python3
"""
Shabakawy GUI Module
Main user interface built with PyQt5
"""

import sys
import time
import threading
from typing import Dict, List, Optional
from datetime import datetime
import logging

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QLineEdit,
        QComboBox, QSpinBox, QProgressBar, QGroupBox, QGridLayout, QMessageBox,
        QCheckBox, QSlider, QSplitter, QFrame, QScrollArea, QSizePolicy
    )
    from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize
    from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPixmap
    PYQT5_AVAILABLE = True
except ImportError:
    PYQT5_AVAILABLE = False
    logging.error("PyQt5 not available. GUI will not work.")

from utils import load_config, get_system_info, get_network_interfaces
from network import NetworkScanner, NetworkDevice, SecurityThreat
from router import RouterController

class NetworkScannerThread(QThread):
    """Thread for running network scanner in background"""
    devices_updated = pyqtSignal(dict)
    threats_updated = pyqtSignal(list)
    status_updated = pyqtSignal(dict)
    
    def __init__(self, scanner: NetworkScanner):
        super().__init__()
        self.scanner = scanner
        self.running = False
    
    def run(self):
        """Main thread loop"""
        self.running = True
        
        def update_callback(devices, threats):
            if self.running:
                self.devices_updated.emit(devices)
                self.threats_updated.emit(threats)
                self.status_updated.emit(self.scanner.get_network_summary())
        
        self.scanner.start_scanning(update_callback)
    
    def stop(self):
        """Stop the scanner thread"""
        self.running = False
        self.scanner.stop_scanning()

class DashboardTab(QWidget):
    """Dashboard tab showing network overview and status"""
    
    def __init__(self, scanner: NetworkScanner):
        super().__init__()
        self.scanner = scanner
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dashboard UI"""
        layout = QVBoxLayout()
        
        # Network Status Section
        status_group = QGroupBox("Network Status")
        status_layout = QGridLayout()
        
        self.status_labels = {}
        status_items = [
            ("Total Devices", "0"),
            ("Online Devices", "0"),
            ("Offline Devices", "0"),
            ("Blocked Devices", "0"),
            ("Active Threats", "0"),
            ("Total Threats", "0"),
            ("Scan Status", "Inactive"),
            ("Packet Capture", "Inactive")
        ]
        
        for i, (label, value) in enumerate(status_items):
            row = i // 2
            col = i % 2 * 2
            
            status_layout.addWidget(QLabel(f"{label}:"), row, col)
            value_label = QLabel(value)
            value_label.setStyleSheet("font-weight: bold; color: #2E86AB;")
            self.status_labels[label] = value_label
            status_layout.addWidget(value_label, row, col + 1)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # System Information Section
        sys_group = QGroupBox("System Information")
        sys_layout = QGridLayout()
        
        self.sys_labels = {}
        sys_info = get_system_info()
        sys_items = [
            ("Operating System", sys_info.get("system", "Unknown")),
            ("OS Version", sys_info.get("release", "Unknown")),
            ("Architecture", sys_info.get("machine", "Unknown")),
            ("Python Version", sys_info.get("python_version", "Unknown"))
        ]
        
        for i, (label, value) in enumerate(sys_items):
            sys_layout.addWidget(QLabel(f"{label}:"), i, 0)
            value_label = QLabel(value)
            value_label.setStyleSheet("color: #2E86AB;")
            self.sys_labels[label] = value_label
            sys_layout.addWidget(value_label, i, 1)
        
        sys_group.setLayout(sys_layout)
        layout.addWidget(sys_group)
        
        # Control Buttons
        button_layout = QHBoxLayout()
        
        self.start_scan_btn = QPushButton("Start Scanning")
        self.start_scan_btn.clicked.connect(self.start_scanning)
        self.start_scan_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        self.stop_scan_btn = QPushButton("Stop Scanning")
        self.stop_scan_btn.clicked.connect(self.stop_scanning)
        self.stop_scan_btn.setEnabled(False)
        self.stop_scan_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        
        button_layout.addWidget(self.start_scan_btn)
        button_layout.addWidget(self.stop_scan_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def update_status(self, status: Dict):
        """Update status display"""
        for label, value in status.items():
            if label in self.status_labels:
                self.status_labels[label].setText(str(value))
    
    def start_scanning(self):
        """Start network scanning"""
        self.start_scan_btn.setEnabled(False)
        self.stop_scan_btn.setEnabled(True)
        self.status_labels["Scan Status"].setText("Active")
        self.status_labels["Scan Status"].setStyleSheet("color: #28a745; font-weight: bold;")
    
    def stop_scanning(self):
        """Stop network scanning"""
        self.start_scan_btn.setEnabled(True)
        self.stop_scan_btn.setEnabled(False)
        self.status_labels["Scan Status"].setText("Inactive")
        self.status_labels["Scan Status"].setStyleSheet("color: #dc3545; font-weight: bold;")

class ThreatsTab(QWidget):
    """Threats and alerts tab"""
    
    def __init__(self, scanner: NetworkScanner):
        super().__init__()
        self.scanner = scanner
        self.init_ui()
    
    def init_ui(self):
        """Initialize the threats UI"""
        layout = QVBoxLayout()
        
        # Threats Table
        self.threats_table = QTableWidget()
        self.threats_table.setColumnCount(6)
        self.threats_table.setHorizontalHeaderLabels([
            "Time", "Type", "Severity", "Source IP", "Source MAC", "Description"
        ])
        
        # Set table properties
        self.threats_table.setAlternatingRowColors(True)
        self.threats_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.threats_table.setSortingEnabled(True)
        
        # Style the table
        self.threats_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #ddd;
                background-color: white;
                alternate-background-color: #f9f9f9;
            }
            QHeaderView::section {
                background-color: #2E86AB;
                color: white;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.threats_table)
        
        # Control Buttons
        button_layout = QHBoxLayout()
        
        self.clear_btn = QPushButton("Clear All Threats")
        self.clear_btn.clicked.connect(self.clear_threats)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        
        self.export_btn = QPushButton("Export Threats")
        self.export_btn.clicked.connect(self.export_threats)
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def update_threats(self, threats: List[SecurityThreat]):
        """Update threats table"""
        self.threats_table.setRowCount(len(threats))
        
        for row, threat in enumerate(threats):
            # Time
            time_item = QTableWidgetItem(threat.timestamp.strftime("%H:%M:%S"))
            self.threats_table.setItem(row, 0, time_item)
            
            # Type
            type_item = QTableWidgetItem(threat.threat_type.upper())
            self.threats_table.setItem(row, 1, type_item)
            
            # Severity
            severity_item = QTableWidgetItem(threat.severity.upper())
            severity_item.setBackground(self.get_severity_color(threat.severity))
            self.threats_table.setItem(row, 2, severity_item)
            
            # Source IP
            ip_item = QTableWidgetItem(threat.source_ip)
            self.threats_table.setItem(row, 3, ip_item)
            
            # Source MAC
            mac_item = QTableWidgetItem(threat.source_mac)
            self.threats_table.setItem(row, 4, mac_item)
            
            # Description
            desc_item = QTableWidgetItem(threat.description)
            self.threats_table.setItem(row, 5, desc_item)
        
        # Auto-resize columns
        self.threats_table.resizeColumnsToContents()
    
    def get_severity_color(self, severity: str) -> QColor:
        """Get color for threat severity"""
        colors = {
            "low": QColor(255, 255, 0, 100),      # Yellow
            "medium": QColor(255, 165, 0, 100),   # Orange
            "high": QColor(255, 69, 0, 100),      # Red-Orange
            "critical": QColor(255, 0, 0, 100)    # Red
        }
        return colors.get(severity.lower(), QColor(255, 255, 255))
    
    def clear_threats(self):
        """Clear all threats"""
        reply = QMessageBox.question(
            self, "Clear Threats", 
            "Are you sure you want to clear all threats?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.scanner.clear_threats()
            self.threats_table.setRowCount(0)
    
    def export_threats(self):
        """Export threats to file"""
        # Implementation for exporting threats
        QMessageBox.information(self, "Export", "Export functionality coming soon!")

class RouterControlTab(QWidget):
    """Router control and management tab"""
    
    def __init__(self, router: RouterController):
        super().__init__()
        self.router = router
        self.init_ui()
    
    def init_ui(self):
        """Initialize the router control UI"""
        layout = QVBoxLayout()
        
        # Connection Section
        conn_group = QGroupBox("Router Connection")
        conn_layout = QGridLayout()
        
        # Router IP
        conn_layout.addWidget(QLabel("Router IP:"), 0, 0)
        self.router_ip_input = QLineEdit("192.168.1.1")
        conn_layout.addWidget(self.router_ip_input, 0, 1)
        
        # Username
        conn_layout.addWidget(QLabel("Username:"), 1, 0)
        self.username_input = QLineEdit("admin")
        conn_layout.addWidget(self.username_input, 1, 1)
        
        # Password
        conn_layout.addWidget(QLabel("Password:"), 2, 0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        conn_layout.addWidget(self.password_input, 2, 1)
        
        # Connection Method
        conn_layout.addWidget(QLabel("Method:"), 3, 0)
        self.method_combo = QComboBox()
        self.method_combo.addItems(["HTTP", "Selenium (Chrome)", "Selenium (Firefox)"])
        conn_layout.addWidget(self.method_combo, 3, 1)
        
        # Connect Button
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_to_router)
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        conn_layout.addWidget(self.connect_btn, 4, 0, 1, 2)
        
        conn_group.setLayout(conn_layout)
        layout.addWidget(conn_group)
        
        # Device Management Section
        device_group = QGroupBox("Device Management")
        device_layout = QVBoxLayout()
        
        # Devices Table
        self.devices_table = QTableWidget()
        self.devices_table.setColumnCount(5)
        self.devices_table.setHorizontalHeaderLabels([
            "Hostname", "IP Address", "MAC Address", "Status", "Actions"
        ])
        device_layout.addWidget(self.devices_table)
        
        # Device Control Buttons
        device_btn_layout = QHBoxLayout()
        
        self.refresh_devices_btn = QPushButton("Refresh Devices")
        self.refresh_devices_btn.clicked.connect(self.refresh_devices)
        
        self.block_device_btn = QPushButton("Block Selected")
        self.block_device_btn.clicked.connect(self.block_selected_device)
        
        self.unblock_device_btn = QPushButton("Unblock Selected")
        self.unblock_device_btn.clicked.connect(self.unblock_selected_device)
        
        device_btn_layout.addWidget(self.refresh_devices_btn)
        device_btn_layout.addWidget(self.block_device_btn)
        device_btn_layout.addWidget(self.unblock_device_btn)
        device_btn_layout.addStretch()
        
        device_layout.addLayout(device_btn_layout)
        device_group.setLayout(device_layout)
        layout.addWidget(device_group)
        
        # Wi-Fi Settings Section
        wifi_group = QGroupBox("Wi-Fi Settings")
        wifi_layout = QGridLayout()
        
        wifi_layout.addWidget(QLabel("New Password:"), 0, 0)
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        wifi_layout.addWidget(self.new_password_input, 0, 1)
        
        self.change_password_btn = QPushButton("Change Password")
        self.change_password_btn.clicked.connect(self.change_wifi_password)
        wifi_layout.addWidget(self.change_password_btn, 1, 0, 1, 2)
        
        wifi_group.setLayout(wifi_layout)
        layout.addWidget(wifi_group)
        
        # Speed Control Section
        speed_group = QGroupBox("Speed Control")
        speed_layout = QGridLayout()
        
        speed_layout.addWidget(QLabel("Device MAC:"), 0, 0)
        self.speed_mac_input = QLineEdit()
        speed_layout.addWidget(self.speed_mac_input, 0, 1)
        
        speed_layout.addWidget(QLabel("Speed Limit (Mbps):"), 1, 0)
        self.speed_limit_input = QSpinBox()
        self.speed_limit_input.setRange(1, 1000)
        self.speed_limit_input.setValue(100)
        speed_layout.addWidget(self.speed_limit_input, 1, 1)
        
        self.set_speed_btn = QPushButton("Set Speed Limit")
        self.set_speed_btn.clicked.connect(self.set_speed_limit)
        speed_layout.addWidget(self.set_speed_btn, 2, 0, 1, 2)
        
        speed_group.setLayout(speed_layout)
        layout.addWidget(speed_group)
        
        self.setLayout(layout)
    
    def connect_to_router(self):
        """Connect to router"""
        try:
            router_ip = self.router_ip_input.text()
            username = self.username_input.text()
            password = self.password_input.text()
            method = self.method_combo.currentText()
            
            if not all([router_ip, username, password]):
                QMessageBox.warning(self, "Error", "Please fill in all fields")
                return
            
            # Update router configuration
            self.router.router_ip = router_ip
            self.router.username = username
            self.router.password = password
            
            # Connect based on method
            if method == "HTTP":
                success = self.router.connect_http()
            elif "Chrome" in method:
                success = self.router.connect_selenium("chrome")
            elif "Firefox" in method:
                success = self.router.connect_selenium("firefox")
            else:
                success = False
            
            if success:
                # Try to login
                if self.router.login():
                    QMessageBox.information(self, "Success", "Connected to router successfully!")
                    self.connect_btn.setText("Connected")
                    self.connect_btn.setEnabled(False)
                    self.refresh_devices()
                else:
                    QMessageBox.warning(self, "Error", "Connected but login failed")
            else:
                QMessageBox.critical(self, "Error", "Failed to connect to router")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection error: {str(e)}")
    
    def refresh_devices(self):
        """Refresh connected devices list"""
        try:
            devices = self.router.get_connected_devices()
            self.update_devices_table(devices)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to refresh devices: {str(e)}")
    
    def update_devices_table(self, devices):
        """Update devices table"""
        self.devices_table.setRowCount(len(devices))
        
        for row, device in enumerate(devices):
            self.devices_table.setItem(row, 0, QTableWidgetItem(device.hostname))
            self.devices_table.setItem(row, 1, QTableWidgetItem(device.ip))
            self.devices_table.setItem(row, 2, QTableWidgetItem(device.mac))
            self.devices_table.setItem(row, 3, QTableWidgetItem(device.status))
            
            # Actions button
            actions_btn = QPushButton("Actions")
            actions_btn.clicked.connect(lambda checked, d=device: self.show_device_actions(d))
            self.devices_table.setCellWidget(row, 4, actions_btn)
    
    def show_device_actions(self, device):
        """Show actions for a specific device"""
        # Implementation for device-specific actions
        pass
    
    def block_selected_device(self):
        """Block selected device"""
        current_row = self.devices_table.currentRow()
        if current_row >= 0:
            mac = self.devices_table.item(current_row, 2).text()
            if self.router.block_device(mac):
                QMessageBox.information(self, "Success", f"Device {mac} blocked successfully")
                self.refresh_devices()
            else:
                QMessageBox.warning(self, "Error", f"Failed to block device {mac}")
        else:
            QMessageBox.warning(self, "Error", "Please select a device to block")
    
    def unblock_selected_device(self):
        """Unblock selected device"""
        current_row = self.devices_table.currentRow()
        if current_row >= 0:
            mac = self.devices_table.item(current_row, 2).text()
            if self.router.unblock_device(mac):
                QMessageBox.information(self, "Success", f"Device {mac} unblocked successfully")
                self.refresh_devices()
            else:
                QMessageBox.warning(self, "Error", f"Failed to unblock device {mac}")
        else:
            QMessageBox.warning(self, "Error", "Please select a device to unblock")
    
    def change_wifi_password(self):
        """Change Wi-Fi password"""
        new_password = self.new_password_input.text()
        if not new_password:
            QMessageBox.warning(self, "Error", "Please enter a new password")
            return
        
        if self.router.change_wifi_password(new_password):
            QMessageBox.information(self, "Success", "Wi-Fi password changed successfully!")
            self.new_password_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Failed to change Wi-Fi password")
    
    def set_speed_limit(self):
        """Set speed limit for device"""
        mac = self.speed_mac_input.text()
        speed = self.speed_limit_input.value()
        
        if not mac:
            QMessageBox.warning(self, "Error", "Please enter device MAC address")
            return
        
        if self.router.set_speed_limit(mac, speed):
            QMessageBox.information(self, "Success", f"Speed limit set to {speed} Mbps for {mac}")
        else:
            QMessageBox.warning(self, "Error", f"Failed to set speed limit for {mac}")

class AnalysisTab(QWidget):
    """Advanced analysis and packet inspection tab"""
    
    def __init__(self, scanner: NetworkScanner):
        super().__init__()
        self.scanner = scanner
        self.init_ui()
    
    def init_ui(self):
        """Initialize the analysis UI"""
        layout = QVBoxLayout()
        
        # Packet Capture Section
        capture_group = QGroupBox("Packet Capture")
        capture_layout = QVBoxLayout()
        
        # Interface Selection
        interface_layout = QHBoxLayout()
        interface_layout.addWidget(QLabel("Network Interface:"))
        self.interface_combo = QComboBox()
        self.interface_combo.addItem("Default")
        
        # Get available interfaces
        interfaces = get_network_interfaces()
        for interface in interfaces:
            self.interface_combo.addItem(interface["name"])
        
        interface_layout.addWidget(self.interface_combo)
        interface_layout.addStretch()
        
        capture_layout.addLayout(interface_layout)
        
        # Capture Controls
        capture_btn_layout = QHBoxLayout()
        
        self.start_capture_btn = QPushButton("Start Capture")
        self.start_capture_btn.clicked.connect(self.start_capture)
        self.start_capture_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        self.stop_capture_btn = QPushButton("Stop Capture")
        self.stop_capture_btn.clicked.connect(self.stop_capture)
        self.stop_capture_btn.setEnabled(False)
        self.stop_capture_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        
        capture_btn_layout.addWidget(self.start_capture_btn)
        capture_btn_layout.addWidget(self.stop_capture_btn)
        capture_btn_layout.addStretch()
        
        capture_layout.addLayout(capture_btn_layout)
        
        # Capture Statistics
        stats_layout = QHBoxLayout()
        
        self.packets_label = QLabel("Packets Captured: 0")
        self.packets_label.setStyleSheet("font-weight: bold; color: #2E86AB;")
        
        self.threats_label = QLabel("Threats Detected: 0")
        self.threats_label.setStyleSheet("font-weight: bold; color: #dc3545;")
        
        stats_layout.addWidget(self.packets_label)
        stats_layout.addWidget(self.threats_label)
        stats_layout.addStretch()
        
        capture_layout.addLayout(stats_layout)
        capture_group.setLayout(capture_layout)
        layout.addWidget(capture_group)
        
        # Packet Analysis Section
        analysis_group = QGroupBox("Packet Analysis")
        analysis_layout = QVBoxLayout()
        
        # Analysis Options
        options_layout = QHBoxLayout()
        
        self.ddos_check = QCheckBox("DDoS Detection")
        self.ddos_check.setChecked(True)
        
        self.mitm_check = QCheckBox("MITM Detection")
        self.mitm_check.setChecked(True)
        
        self.spoofing_check = QCheckBox("MAC Spoofing Detection")
        self.spoofing_check.setChecked(True)
        
        self.anomaly_check = QCheckBox("Anomaly Detection")
        self.anomaly_check.setChecked(True)
        
        options_layout.addWidget(self.ddos_check)
        options_layout.addWidget(self.mitm_check)
        options_layout.addWidget(self.spoofing_check)
        options_layout.addWidget(self.anomaly_check)
        options_layout.addStretch()
        
        analysis_layout.addLayout(options_layout)
        
        # Analysis Results
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }
        """)
        analysis_layout.addWidget(self.analysis_text)
        
        analysis_group.setLayout(analysis_layout)
        layout.addWidget(analysis_group)
        
        self.setLayout(layout)
    
    def start_capture(self):
        """Start packet capture"""
        interface = self.interface_combo.currentText()
        if interface == "Default":
            interface = None
        
        if self.scanner.start_packet_capture(interface):
            self.start_capture_btn.setEnabled(False)
            self.stop_capture_btn.setEnabled(True)
            self.analysis_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] Started packet capture on {interface or 'default'} interface")
        else:
            QMessageBox.warning(self, "Error", "Failed to start packet capture")
    
    def stop_capture(self):
        """Stop packet capture"""
        self.scanner.stop_packet_capture()
        self.start_capture_btn.setEnabled(True)
        self.stop_capture_btn.setEnabled(False)
        self.analysis_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] Stopped packet capture")
    
    def update_capture_stats(self, status: Dict):
        """Update capture statistics"""
        self.packets_label.setText(f"Packets Captured: {status.get('packets_captured', 0)}")
        self.threats_label.setText(f"Threats Detected: {status.get('threats_detected', 0)}")

class ShabakawyGUI(QMainWindow):
    """Main Shabakawy application window"""
    
    def __init__(self):
        super().__init__()
        
        if not PYQT5_AVAILABLE:
            QMessageBox.critical(None, "Error", "PyQt5 is required but not available!")
            sys.exit(1)
        
        # Load configuration
        self.config = load_config()
        
        # Initialize components
        self.scanner = NetworkScanner(self.config["security"])
        self.router = RouterController(self.config["router"])
        
        # Initialize UI
        self.init_ui()
        
        # Setup scanner thread
        self.scanner_thread = NetworkScannerThread(self.scanner)
        self.scanner_thread.devices_updated.connect(self.update_devices)
        self.scanner_thread.threats_updated.connect(self.update_threats)
        self.scanner_thread.status_updated.connect(self.update_status)
        
        # Setup update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.periodic_update)
        self.update_timer.start(5000)  # Update every 5 seconds
    
    def init_ui(self):
        """Initialize the main UI"""
        self.setWindowTitle("Shabakawy - Network Security Monitor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set application icon (placeholder)
        # self.setWindowIcon(QIcon("icon.png"))
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.dashboard_tab = DashboardTab(self.scanner)
        self.threats_tab = ThreatsTab(self.scanner)
        self.router_tab = RouterControlTab(self.router)
        self.analysis_tab = AnalysisTab(self.scanner)
        
        # Add tabs to widget
        self.tab_widget.addTab(self.dashboard_tab, "Dashboard")
        self.tab_widget.addTab(self.threats_tab, "Threats & Alerts")
        self.tab_widget.addTab(self.router_tab, "Router Control")
        self.tab_widget.addTab(self.analysis_tab, "Advanced Analysis")
        
        # Style the tab widget
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f8f9fa;
                padding: 8px 16px;
                margin-right: 2px;
                border: 1px solid #ddd;
                border-bottom: none;
                border-radius: 4px 4px 0 0;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
            QTabBar::tab:hover {
                background-color: #e9ecef;
            }
        """)
        
        # Set main layout
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        central_widget.setLayout(layout)
        
        # Apply dark theme if configured
        if self.config["gui"]["theme"] == "dark":
            self.apply_dark_theme()
    
    def apply_dark_theme(self):
        """Apply dark theme to the application"""
        dark_palette = QPalette()
        
        # Set dark colors
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        self.setPalette(dark_palette)
    
    def update_devices(self, devices: Dict):
        """Update devices across all tabs"""
        # This would update device displays in relevant tabs
        pass
    
    def update_threats(self, threats: List[SecurityThreat]):
        """Update threats across all tabs"""
        self.threats_tab.update_threats(threats)
    
    def update_status(self, status: Dict):
        """Update status across all tabs"""
        self.dashboard_tab.update_status(status)
        self.analysis_tab.update_capture_stats(status)
    
    def periodic_update(self):
        """Periodic update function"""
        # Update system information and other periodic tasks
        pass
    
    def start_scanning(self):
        """Start network scanning"""
        self.scanner_thread.start()
        self.dashboard_tab.start_scanning()
    
    def stop_scanning(self):
        """Stop network scanning"""
        self.scanner_thread.stop()
        self.dashboard_tab.stop_scanning()
    
    def run(self):
        """Run the application"""
        self.show()
        
        # Start scanning automatically if configured
        if self.config["gui"]["auto_refresh"] == "true":
            self.start_scanning()
    
    def closeEvent(self, event):
        """Handle application close event"""
        try:
            # Stop scanning and cleanup
            if hasattr(self, 'scanner_thread'):
                self.scanner_thread.stop()
                self.scanner_thread.wait()
            
            if hasattr(self, 'router'):
                self.router.disconnect()
            
            event.accept()
        except Exception as e:
            logging.error(f"Error during shutdown: {e}")
            event.accept()

def main():
    """Main entry point for GUI"""
    if not PYQT5_AVAILABLE:
        print("Error: PyQt5 is required but not available!")
        print("Please install PyQt5: pip install PyQt5")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Shabakawy")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Shabakawy Security")
    
    # Create and show main window
    window = ShabakawyGUI()
    window.run()
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
