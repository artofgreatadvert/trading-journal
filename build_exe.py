#!/usr/bin/env python3
"""
Build script to create standalone executable using PyInstaller
"""

import PyInstaller.__main__
import os
import sys

def build_executable():
    """Build the executable"""
    print("Building Trading Journal executable...")
    print("This may take a few minutes...\n")
    
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--windowed',
        '--name=Trading Journal',
        '--icon=NONE',
        '--add-data=config:config',
        '--add-data=database:database',
        '--add-data=gui:gui',
        '--hidden-import=PyQt6',
        '--hidden-import=sqlalchemy',
        '--hidden-import=pandas',
        '--hidden-import=matplotlib',
        '--collect-all=PyQt6',
        '--distpath=dist',
        '--buildpath=build',
        '--specpath=.',
    ])
    
    print("\n" + "="*50)
    print("BUILD COMPLETE!")
    print("="*50)
    print("\nYour executable is ready:")
    if sys.platform == 'win32':
        print("  dist/Trading Journal.exe")
    else:
        print("  dist/Trading Journal")
    print("\nYou can now run the application!")

if __name__ == '__main__':
    build_executable()
