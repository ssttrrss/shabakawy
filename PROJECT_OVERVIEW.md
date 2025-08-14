# Shabakawy Project Overview

## Project Architecture

Shabakawy is a comprehensive cybersecurity monitoring and router control application built with a modular architecture designed for cross-platform compatibility and extensibility.

### Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Shabakawy Application                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │    GUI      │  │   Network   │  │   Router    │        │
│  │  (PyQt5)    │  │  Scanner    │  │ Controller  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│                    Utilities Layer                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Config    │  │   Logging   │  │   Platform  │        │
│  │ Management  │  │   System    │  │ Compatibility│        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│                    System Layer                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Python    │  │   Network   │  │   Security  │        │
│  │   Runtime   │  │   Stack     │  │   Tools     │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## Module Breakdown

### 1. GUI Module (`gui.py`)

**Purpose**: Provides the user interface for the application

**Key Components**:
- **Main Window**: Central application window with tabbed interface
- **Dashboard Tab**: Network overview and control panel
- **Threats Tab**: Security alerts and threat management
- **Router Control Tab**: Router administration and device management
- **Analysis Tab**: Advanced packet analysis and monitoring

**Features**:
- Modern PyQt5-based interface
- Real-time data updates
- Responsive design with dark/light themes
- Cross-platform compatibility

**Technical Implementation**:
- Uses QThread for background operations
- Signal-slot architecture for inter-tab communication
- Custom styling with CSS-like syntax
- Modular tab system for easy extension

### 2. Network Scanner Module (`network.py`)

**Purpose**: Handles network discovery, monitoring, and threat detection

**Key Components**:
- **NetworkScanner**: Main scanning engine
- **NetworkDevice**: Device representation and tracking
- **SecurityThreat**: Threat detection and classification
- **Packet Analysis**: Deep packet inspection capabilities

**Features**:
- Automatic device discovery
- Real-time threat detection
- DDoS, MITM, and spoofing detection
- Automatic countermeasures
- Port scanning and service detection

**Technical Implementation**:
- Multi-threaded scanning for performance
- Configurable detection thresholds
- Callback-based updates to GUI
- Cross-platform network commands

### 3. Router Controller Module (`router.py`)

**Purpose**: Automates router administration and device management

**Key Components**:
- **RouterController**: Main router management class
- **RouterDevice**: Connected device representation
- **RouterSettings**: Configuration management
- **Connection Methods**: HTTP and Selenium-based automation

**Features**:
- Automatic router model detection
- Multiple connection methods (HTTP/Selenium)
- Device blocking and unblocking
- Wi-Fi password management
- Speed limit configuration

**Technical Implementation**:
- Fallback connection methods
- Browser automation with Selenium
- HTTP API integration
- Cross-platform browser support

### 4. Utilities Module (`utils.py`)

**Purpose**: Provides cross-platform compatibility and helper functions

**Key Components**:
- **Platform Detection**: OS and distribution identification
- **Configuration Management**: INI-based configuration
- **Logging System**: Centralized logging with rotation
- **System Commands**: Cross-platform command execution

**Features**:
- Automatic platform detection
- Configuration file management
- Dependency checking
- Network interface enumeration
- System information gathering

**Technical Implementation**:
- Platform-specific code paths
- Configuration file validation
- Error handling and fallbacks
- Cross-platform file path handling

## Data Flow

### 1. Application Startup
```
run.py → utils.setup_logging() → utils.load_config() → GUI initialization
```

### 2. Network Scanning
```
GUI Start Button → NetworkScanner.start_scanning() → Background Thread → 
Device Discovery → Threat Detection → GUI Update via Signals
```

### 3. Threat Detection
```
Packet Capture → Analysis Engine → Threat Classification → 
Countermeasure Application → Alert Generation → GUI Update
```

### 4. Router Control
```
GUI Input → RouterController.connect() → Authentication → 
Device Management → Configuration Changes → Status Update
```

## Security Features

### 1. Threat Detection
- **DDoS Detection**: Connection rate monitoring with configurable thresholds
- **MITM Detection**: ARP table monitoring and anomaly detection
- **MAC Spoofing**: Duplicate MAC address detection
- **Network Anomalies**: Behavioral analysis and pattern recognition

### 2. Countermeasures
- **Automatic Blocking**: Device isolation based on threat level
- **Rate Limiting**: Traffic throttling for suspicious sources
- **Alert System**: Real-time notification of security events
- **Logging**: Comprehensive audit trail for incident response

### 3. Access Control
- **Router Integration**: Direct control over network access
- **Device Management**: Individual device blocking and monitoring
- **Speed Control**: Bandwidth management for specific devices
- **Guest Network**: Isolated network segment management

## Cross-Platform Compatibility

### Windows Support
- **Network Commands**: Uses `netsh`, `route`, `arp` commands
- **File Paths**: Windows-style path handling
- **Permissions**: Administrator privilege detection
- **Firewall**: Windows Firewall rule management

### Linux Support
- **Distribution Detection**: Automatic package manager identification
- **Network Commands**: Uses `ip`, `arp`, `ping` commands
- **Package Management**: apt, dnf, pacman support
- **System Services**: systemd integration

### Common Features
- **Python Runtime**: Consistent Python environment
- **Network Libraries**: Cross-platform network libraries
- **GUI Framework**: PyQt5 for consistent interface
- **Configuration**: Platform-appropriate config locations

## Installation and Deployment

### Automated Installation
- **Linux**: Bash script with distribution detection
- **Windows**: Batch script with administrator checks
- **Dependencies**: Automatic Python package installation
- **Configuration**: Default configuration file generation

### Manual Installation
- **Prerequisites**: Python, Git, system dependencies
- **Repository**: GitHub cloning and setup
- **Dependencies**: pip-based package installation
- **Configuration**: Manual configuration file setup

### Deployment Options
- **Desktop Application**: Standalone GUI application
- **System Service**: Background service (Linux)
- **Portable Mode**: USB drive deployment
- **Network Deployment**: Centralized management

## Performance Considerations

### 1. Memory Management
- **Device Tracking**: Configurable device limit
- **Threat History**: Automatic cleanup and rotation
- **Packet Buffers**: Limited buffer sizes for capture
- **Thread Management**: Controlled thread pool sizes

### 2. CPU Optimization
- **Scan Intervals**: Configurable scanning frequency
- **Analysis Algorithms**: Efficient threat detection
- **Background Processing**: Non-blocking operations
- **Resource Monitoring**: System resource awareness

### 3. Network Efficiency
- **Selective Scanning**: Focus on active devices
- **Packet Filtering**: Relevant traffic analysis only
- **Connection Pooling**: Reuse network connections
- **Timeout Management**: Configurable operation timeouts

## Extensibility

### 1. Plugin System
- **Detection Modules**: Custom threat detection algorithms
- **Router Support**: Additional router model support
- **Export Formats**: Custom data export capabilities
- **Integration APIs**: Third-party system integration

### 2. Configuration Extensions
- **Custom Rules**: User-defined security policies
- **Network Segments**: Multi-network support
- **Alert Actions**: Custom notification methods
- **Reporting**: Custom report generation

### 3. API Integration
- **REST API**: HTTP-based integration
- **WebSocket**: Real-time data streaming
- **Database**: Persistent data storage
- **SIEM Integration**: Security information management

## Testing and Quality Assurance

### 1. Unit Testing
- **Module Tests**: Individual component testing
- **Mock Objects**: Network and system simulation
- **Error Handling**: Exception and edge case testing
- **Performance**: Load and stress testing

### 2. Integration Testing
- **End-to-End**: Complete workflow testing
- **Cross-Platform**: Platform-specific testing
- **Network Simulation**: Virtual network testing
- **Router Testing**: Real router integration testing

### 3. Security Testing
- **Penetration Testing**: Vulnerability assessment
- **Threat Simulation**: Attack scenario testing
- **Performance Testing**: Load and stress testing
- **Compliance Testing**: Security standard validation

## Future Development

### 1. Planned Features
- **Machine Learning**: AI-powered threat detection
- **Cloud Integration**: Remote monitoring capabilities
- **Mobile App**: Smartphone monitoring application
- **API Gateway**: RESTful API for integration

### 2. Technology Updates
- **Python 3.12+**: Latest Python version support
- **PyQt6**: Modern Qt framework migration
- **Async Support**: Asynchronous operation support
- **Containerization**: Docker and Kubernetes support

### 3. Platform Expansion
- **macOS Support**: Native macOS application
- **ARM Support**: ARM64 architecture support
- **Embedded Systems**: IoT device monitoring
- **Cloud Platforms**: AWS, Azure, GCP integration

## Conclusion

Shabakawy represents a comprehensive approach to network security monitoring and management. Its modular architecture, cross-platform compatibility, and extensive feature set make it suitable for both personal and enterprise use.

The application successfully combines:
- **Security**: Advanced threat detection and response
- **Usability**: Intuitive interface for all skill levels
- **Reliability**: Robust error handling and recovery
- **Extensibility**: Easy customization and enhancement
- **Performance**: Efficient resource utilization

This foundation provides a solid base for continued development and expansion, ensuring Shabakawy remains a valuable tool in the cybersecurity landscape.
