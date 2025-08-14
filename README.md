# Shabakawy 🔒

**Shabakawy** is a comprehensive cybersecurity monitoring and router control application designed to protect your home network from various cyber threats.

## 🚀 Features

### Network Security Monitoring
- **Real-time Network Scanning**: Discover all connected devices on your network
- **Packet Inspection**: Monitor network traffic for suspicious activity
- **Threat Detection**: Automatically detect DDoS attacks, MITM attempts, and MAC spoofing
- **Intelligent Countermeasures**: Block malicious devices and alert users to threats

### Router Control & Management
- **Automated Router Access**: Secure login to router admin panels
- **Device Management**: Block/unblock specific devices from your network
- **Wi-Fi Security**: Change passwords and manage access controls
- **Bandwidth Control**: Set speed limits for individual devices

### User-Friendly Interface
- **Cross-Platform**: Works on Windows and Linux (Kali, Ubuntu, etc.)
- **Modern GUI**: Built with PyQt5 for a professional, intuitive experience
- **Real-time Dashboard**: Monitor network health and security status
- **Threat Alerts**: Get notified immediately when threats are detected

## 🛡️ Security Features

- **DDoS Protection**: Detect and mitigate distributed denial-of-service attacks
- **MITM Detection**: Identify man-in-the-middle attacks in real-time
- **MAC Spoofing Prevention**: Detect and block devices with spoofed MAC addresses
- **Network Anomaly Detection**: Machine learning-based threat identification

## 🖥️ System Requirements

- **Operating System**: Windows 10+ or Linux (Ubuntu 18.04+, Kali Linux)
- **Python**: 3.8 or higher
- **Memory**: Minimum 4GB RAM
- **Network**: Active internet connection for initial setup

## 🚀 Quick Start

### Windows Users
1. Run `install_and_setup_win.bat` as Administrator
2. Follow the installation prompts
3. Launch the application with `run.bat`

### Linux Users
1. Make the installer executable: `chmod +x install_and_setup_linux.sh`
2. Run the installer: `sudo ./install_and_setup_linux.sh`
3. Launch the application: `./run`

## 📁 Project Structure

```
shabakawy/
├── src/                    # Source code
│   ├── gui.py            # Main GUI interface
│   ├── network.py        # Network scanning and security
│   ├── router.py         # Router automation and control
│   └── utils.py          # Helper functions and utilities
├── installers/            # Platform-specific installers
├── docs/                  # Documentation and guides
├── run.py                 # Application entry point
└── README.md             # This file
```

## 🔧 Installation

For detailed installation instructions, see the [Installation Guide](docs/guide.md).

## ⚠️ Disclaimer

This application is designed for educational and personal network security purposes. Users are responsible for ensuring compliance with local laws and regulations when using this software. The developers are not liable for any misuse or damage caused by this application.

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests for any improvements.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or need help:
1. Check the [troubleshooting section](docs/guide.md#troubleshooting) in the guide
2. Open an issue on GitHub
3. Contact the development team

---

**Shabakawy** - Your Network's Guardian 🛡️
