# Serial Monitor v1.0.0

A lightweight, feature-rich serial port monitor for Windows.

## Features

### Core Functionality
- **Real-time Serial Monitoring** - Monitor any COM port with configurable baud rates (9600-921600)
- **Color-Coded Output** - Automatic syntax highlighting for ERROR, WARNING, INFO, SUCCESS, and DEBUG messages
- **Auto Port Detection** - Automatically detects when devices connect/disconnect with visual feedback
- **Timestamp Support** - Optional timestamps on every line

### User Interface
- **Dark Theme** - Easy on the eyes with a modern dark interface
- **Custom Icon** - Professional appearance with custom application icon
- **No Console Window** - Runs as a clean GUI application
- **Status Bar** - Real-time connection status and notifications

### Data Management
- **Save Logs** - Export logs to timestamped text files
- **Copy to Clipboard** - Copy all output with one click
- **Clear Display** - Quick clear button for fresh monitoring
- **Auto-scroll** - Automatically scrolls to show latest data

### Help System
- **Built-in Help** - Comprehensive help with color coding examples
- **Quick Start Guide** - Usage instructions right in the app
- **Troubleshooting** - Common issue solutions included

## Installation

### Option 1: Download EXE (Recommended)

Download `SerialMonitor.exe` - No Python installation required!

Just download and run. That's it!

### Option 2: Run from Source

Requires Python 3.6+

```bash
pip install pyserial
python serial_monitor.pyw
```

## What's New in v1.0.0

- Initial release
- Full-featured serial monitoring
- Custom icon support
- Standalone Windows executable
- Color-coded output with prefix detection
- Auto port detection and highlighting
- Built-in help system

## Color Coding

Lines starting with these prefixes are automatically colored:

- `[ERROR]` or `ERROR:` - Red
- `[WARN]`, `[WARNING]`, `WARN:`, `WARNING:` - Orange
- `[INFO]` or `INFO:` - Blue
- `[SUCCESS]` or `SUCCESS:` - Green
- `[DEBUG]` or `DEBUG:` - Gray

Matching is case-insensitive!

## System Requirements

- **OS**: Windows 10/11
- **RAM**: 50MB
- **Disk**: 15MB
- **Python**: Not required for EXE version

## Known Issues

- Windows locks COM ports exclusively (standard behavior)
- Requires Administrator privileges for some protected COM ports

## Building from Source

See `BUILD_INSTRUCTIONS.md` for details on building your own EXE.

## License

MIT License - See LICENSE file for details

## Links

- **GitHub**: https://github.com/LouisHitchcock/serialMonitor
- **Issues**: https://github.com/LouisHitchcock/serialMonitor/issues
