# Building Serial Monitor as EXE

This guide explains how to build Serial Monitor as a standalone Windows executable.

## Prerequisites

```powershell
pip install pyinstaller pillow
```

## Steps

### 1. Add Your Icon

Place your icon file as `icon.png` in the SerialMonitor directory:
```
C:\Users\Louis\Desktop\Code\SerialMonitor\icon.png
```

The icon should be:
- Square (recommended 256x256 or larger)
- PNG format
- Will be automatically converted to .ico with multiple sizes

### 2. Run the Build Script

```powershell
python build_exe.py
```

The script will:
1. Convert `icon.png` to `icon.ico` (multiple sizes for Windows)
2. Build the EXE using PyInstaller
3. Create a single-file executable

### 3. Get Your EXE

Your executable will be located at:
```
dist\SerialMonitor.exe
```

## What Gets Built

- **Single EXE file** - No installation needed
- **No console window** - Runs as a GUI app
- **Custom icon** - Your icon.png on the taskbar and window
- **Standalone** - No Python required on target PC

## Distribution

Simply copy `dist\SerialMonitor.exe` to any Windows PC and run it!

## Troubleshooting

**"icon.png not found"**
- Make sure icon.png is in the same directory as build_exe.py

**"PyInstaller not installed"**
```powershell
pip install pyinstaller
```

**"Pillow not installed"**
```powershell
pip install pillow
```

**Build failed**
- Make sure `serialMonitor.pyw` exists
- Check that you have write permissions in the directory
- Close any running instances of Serial Monitor

## Clean Build

To start fresh:
```powershell
Remove-Item -Recurse -Force build, dist, *.spec
python build_exe.py
```

## Advanced: Manual Build

If you want to customize the build:
```powershell
pyinstaller --onefile --windowed --name=SerialMonitor --icon=icon.ico serialMonitor.pyw
```
