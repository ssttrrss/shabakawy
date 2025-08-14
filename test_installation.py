#!/usr/bin/env python3
"""
Shabakawy Installation Test Script
This script tests if all dependencies and modules are working correctly
"""

import sys
import importlib
from pathlib import Path

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        if package_name:
            importlib.import_module(module_name, package_name)
        else:
            importlib.import_module(module_name)
        print(f"✓ {module_name} - OK")
        return True
    except ImportError as e:
        print(f"✗ {module_name} - FAILED: {e}")
        return False
    except Exception as e:
        print(f"✗ {module_name} - ERROR: {e}")
        return False

def test_local_modules():
    """Test if local modules can be imported"""
    print("\n--- Testing Local Modules ---")
    
    # Add src directory to path
    src_path = Path(__file__).parent / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))
        
        modules = ["utils", "network", "router", "gui"]
        success_count = 0
        
        for module in modules:
            if test_import(module):
                success_count += 1
        
        print(f"\nLocal modules: {success_count}/{len(modules)} passed")
        return success_count == len(modules)
    else:
        print("✗ src directory not found")
        return False

def test_dependencies():
    """Test if all required dependencies can be imported"""
    print("\n--- Testing Dependencies ---")
    
    dependencies = [
        "PyQt5",
        "scapy",
        "psutil",
        "requests",
        "selenium",
        "bs4",  # beautifulsoup4
        "lxml",
        "cryptography",
        "paramiko",
        "netifaces"
    ]
    
    success_count = 0
    for dep in dependencies:
        if test_import(dep):
            success_count += 1
    
    print(f"\nDependencies: {success_count}/{len(dependencies)} passed")
    return success_count == len(dependencies)

def test_system_info():
    """Test system information gathering"""
    print("\n--- Testing System Information ---")
    
    try:
        import platform
        print(f"✓ Platform: {platform.system()} {platform.release()}")
        print(f"✓ Python: {platform.python_version()}")
        print(f"✓ Architecture: {platform.machine()}")
        
        # Test utils module if available
        try:
            from utils import get_system_info, get_platform_info
            sys_info = get_system_info()
            platform_info = get_platform_info()
            print(f"✓ System info module working")
            print(f"  - OS: {platform_info.get('system', 'Unknown')}")
            print(f"  - Release: {platform_info.get('release', 'Unknown')}")
        except ImportError:
            print("✗ Utils module not available")
        
        return True
    except Exception as e:
        print(f"✗ System info test failed: {e}")
        return False

def test_network_capabilities():
    """Test network-related capabilities"""
    print("\n--- Testing Network Capabilities ---")
    
    try:
        # Test basic network operations
        import socket
        print("✓ Socket module - OK")
        
        # Test if we can get local IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            print(f"✓ Local IP detection: {local_ip}")
        except Exception as e:
            print(f"✗ Local IP detection failed: {e}")
        
        # Test if we can resolve DNS
        try:
            ip = socket.gethostbyname("google.com")
            print(f"✓ DNS resolution: google.com -> {ip}")
        except Exception as e:
            print(f"✗ DNS resolution failed: {e}")
        
        return True
    except Exception as e:
        print(f"✗ Network capabilities test failed: {e}")
        return False

def test_gui_capabilities():
    """Test GUI capabilities"""
    print("\n--- Testing GUI Capabilities ---")
    
    try:
        # Test PyQt5
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        
        print("✓ PyQt5 core modules - OK")
        
        # Test if we can create a basic application
        try:
            app = QApplication.instance()
            if app is None:
                app = QApplication([])
            print("✓ QApplication creation - OK")
            
            # Clean up
            if app.parent() is None:
                app.quit()
                
        except Exception as e:
            print(f"✗ QApplication test failed: {e}")
        
        return True
    except Exception as e:
        print(f"✗ GUI capabilities test failed: {e}")
        return False

def main():
    """Main test function"""
    print("Shabakawy Installation Test")
    print("=" * 40)
    
    # Test dependencies
    deps_ok = test_dependencies()
    
    # Test local modules
    modules_ok = test_local_modules()
    
    # Test system info
    sys_ok = test_system_info()
    
    # Test network capabilities
    net_ok = test_network_capabilities()
    
    # Test GUI capabilities
    gui_ok = test_gui_capabilities()
    
    # Summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    
    tests = [
        ("Dependencies", deps_ok),
        ("Local Modules", modules_ok),
        ("System Info", sys_ok),
        ("Network Capabilities", net_ok),
        ("GUI Capabilities", gui_ok)
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:20} : {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Shabakawy is ready to use.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
