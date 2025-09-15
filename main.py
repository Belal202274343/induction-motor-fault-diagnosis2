#!/usr/bin/env python3
"""
Induction Motor Fault Diagnosis - Main Script
This script serves as the entry point for the motor fault diagnosis system.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent))

def main():
    """Main function to run the motor fault diagnosis system."""
    print("Induction Motor Fault Diagnosis System")
    print("======================================")
    print("System initialized. Ready for data input and analysis.")

if __name__ == "__main__":
    main()
