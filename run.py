#!/usr/bin/env python3
"""
Shabakawy - Cybersecurity Monitoring and Router Control Application
Main entry point for the application
"""

import sys
import os
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui import ShabakawyGUI
from utils import setup_logging, check_dependencies

def main():
    """Main entry point for Shabakawy application"""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting Shabakawy application...")
        
        # Check dependencies
        if not check_dependencies():
            logger.error("Missing required dependencies. Please run the installer first.")
            sys.exit(1)
        
        # Launch GUI
        app = ShabakawyGUI()
        app.run()
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
