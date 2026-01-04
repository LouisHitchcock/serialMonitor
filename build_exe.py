"""
Build script to create standalone EXE for Serial Monitor
Requirements: pip install pyinstaller pillow
"""

import os
import subprocess
import sys

def convert_icon():
    """Convert icon.png to icon.ico"""
    try:
        from PIL import Image
        
        if not os.path.exists('icon.png'):
            print("ERROR: icon.png not found!")
            print("Please add your icon.png file to this directory first.")
            return False
        
        print("Converting icon.png to icon.ico...")
        img = Image.open('icon.png')
        
        # Create multiple sizes for Windows
        icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        img.save('icon.ico', format='ICO', sizes=icon_sizes)
        
        print("✓ Icon converted successfully!")
        return True
        
    except ImportError:
        print("ERROR: Pillow not installed. Run: pip install pillow")
        return False
    except Exception as e:
        print(f"ERROR converting icon: {e}")
        return False

def build_exe():
    """Build the EXE using PyInstaller"""
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("ERROR: PyInstaller not installed. Run: pip install pyinstaller")
        return False
    
    print("\nBuilding EXE...")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                    # Single EXE file
        '--windowed',                   # No console window
        '--name=SerialMonitor',         # Output name
        '--icon=icon.ico',              # Icon file
        '--add-data=icon.ico;.',        # Include icon in bundle
        'serial_monitor.pyw'            # Main script
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        print("\n✓ Build successful!")
        print(f"\nYour EXE is located at: dist\\SerialMonitor.exe")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR building EXE: {e}")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("=" * 60)
    print("Serial Monitor - EXE Builder")
    print("=" * 60)
    print()
    
    # Step 1: Convert icon
    if not convert_icon():
        print("\nBuild aborted.")
        sys.exit(1)
    
    # Step 2: Build EXE
    if not build_exe():
        print("\nBuild aborted.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("BUILD COMPLETE!")
    print("=" * 60)
    print("\nTo distribute:")
    print("  1. Copy dist\\SerialMonitor.exe to any Windows PC")
    print("  2. No Python installation required!")
    print()

if __name__ == "__main__":
    main()
