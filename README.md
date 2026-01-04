# Serial Monitor

A lightweight serial monitor with color-coded output and non-exclusive port access.

## Features

- **COM Port Selection**: Dropdown list of available COM ports with auto-detection
- **Configurable Baud Rate**: Support for common baud rates (9600 to 921600)
- **Timestamp Toggle**: Optional timestamps for each received line
- **Color-Coded Output**: Automatic color highlighting for:
  - `ERROR` - Red
  - `WARNING` - Orange
  - `INFO` - Blue
  - `SUCCESS` - Green
  - `DEBUG` - Gray
- **Save History**: Export logs to timestamped text files
- **Clear Display**: Clear the output window
- **Copy to Clipboard**: Copy all console output with one click

## Installation

1. Install Python 3.6 or higher
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the serial monitor:
```
python serial_monitor.py
```

### Controls

1. **Select COM Port**: Choose from the dropdown (click Refresh to update the list)
2. **Set Baud Rate**: Select the appropriate baud rate for your device
3. **Connect**: Click to start monitoring
4. **Timestamp**: Check to enable timestamps on each line
5. **Clear**: Clear the output display
6. **Copy**: Copy all output to clipboard
7. **Save**: Save current output to a text file
8. **Disconnect**: Stop monitoring (button changes when connected)

## Customizing Colors

You can modify the color patterns in the `SerialMonitor.__init__()` method:

```python
self.color_patterns = [
    (r'\berror\b', 'red'),
    (r'\bwarning\b', 'orange'),
    (r'\binfo\b', 'blue'),
    (r'\bsuccess\b', 'green'),
    (r'\bdebug\b', 'gray'),
]
```

Add your own regex patterns and colors to match your specific needs.

## Notes

- Automatic port detection with visual highlighting when new devices connect
- Dark theme with monospace font for better readability
- Auto-scrolls to show latest messages
- Handles UTF-8 decoding with error replacement for robustness
- Port is locked exclusively while monitoring (standard Windows behavior)
