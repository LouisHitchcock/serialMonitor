import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import serial
import serial.tools.list_ports
import threading
import time
from datetime import datetime
import re
import os
import sys


class SerialMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Monitor")
        self.root.geometry("900x600")
        
        # Set window icon
        self.set_icon()
        
        self.serial_port = None
        self.running = False
        self.show_timestamp = tk.BooleanVar(value=False)
        self.autoscroll = tk.BooleanVar(value=True)
        self.autoconnect = tk.BooleanVar(value=False)
        self.last_connected_port = None
        self.last_baud_rate = None
        
        # Color patterns - prefix: color
        # Lines starting with these prefixes will be colored
        self.color_patterns = [
            ('[ERROR]', 'red'),
            ('[WARN]', 'orange'),
            ('[WARNING]', 'orange'),
            ('[INFO]', 'blue'),
            ('[SUCCESS]', 'green'),
            ('[DEBUG]', 'gray'),
            ('ERROR:', 'red'),
            ('WARN:', 'orange'),
            ('WARNING:', 'orange'),
            ('INFO:', 'blue'),
            ('SUCCESS:', 'green'),
            ('DEBUG:', 'gray'),
        ]
        
        # Port monitoring
        self.known_ports = set()
        self.monitoring = True
        
        self.setup_ui()
        self.refresh_ports()
        
        # Start port monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_ports, daemon=True)
        self.monitor_thread.start()
    
    def set_icon(self):
        """Set window icon from icon.ico file"""
        try:
            # Try to find icon.ico in the same directory as the script
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                app_dir = sys._MEIPASS
            else:
                # Running as script
                app_dir = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(app_dir, 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            # If icon loading fails, continue without it
            pass
        
    def setup_ui(self):
        # Top control panel
        control_frame = ttk.Frame(self.root, padding="5")
        control_frame.pack(fill=tk.X)
        
        # COM Port selection
        ttk.Label(control_frame, text="COM Port:").pack(side=tk.LEFT, padx=5)
        self.port_combo = ttk.Combobox(control_frame, width=15, state='readonly')
        self.port_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Refresh", command=self.refresh_ports).pack(side=tk.LEFT, padx=2)
        
        # Baud rate
        ttk.Label(control_frame, text="Baud:").pack(side=tk.LEFT, padx=5)
        self.baud_combo = ttk.Combobox(control_frame, width=10, state='readonly')
        self.baud_combo['values'] = ('9600', '19200', '38400', '57600', '115200', '230400', '460800', '921600')
        self.baud_combo.current(4)  # Default to 115200
        self.baud_combo.pack(side=tk.LEFT, padx=5)
        
        # Connect/Disconnect button
        self.connect_btn = ttk.Button(control_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        
        # Autoconnect toggle
        ttk.Checkbutton(control_frame, text="Autoconnect", variable=self.autoconnect).pack(side=tk.LEFT, padx=5)
        
        # Clear button
        ttk.Button(control_frame, text="Clear", command=self.clear_output).pack(side=tk.LEFT, padx=5)
        
        # Copy button
        ttk.Button(control_frame, text="Copy", command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=5)
        
        # Save button
        ttk.Button(control_frame, text="Save", command=self.save_history).pack(side=tk.LEFT, padx=5)
        
        # Help button (right side)
        ttk.Button(control_frame, text="?", command=self.show_help, width=3).pack(side=tk.RIGHT, padx=5)
        
        # Text output area with scrollbar
        output_frame = ttk.Frame(self.root)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            width=100,
            height=30,
            font=('Consolas', 9),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='white'
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure color tags
        self.output_text.tag_config('red', foreground='#f44336')
        self.output_text.tag_config('orange', foreground='#ff9800')
        self.output_text.tag_config('blue', foreground='#2196f3')
        self.output_text.tag_config('green', foreground='#4caf50')
        self.output_text.tag_config('gray', foreground='#9e9e9e')
        self.output_text.tag_config('timestamp', foreground='#888888')
        
        # Status bar with toggles
        status_frame = ttk.Frame(self.root, relief=tk.SUNKEN)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)
        
        self.status_label = ttk.Label(status_frame, text="Disconnected", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Timestamp toggle (right side of footer)
        ttk.Checkbutton(status_frame, text="Timestamp", variable=self.show_timestamp).pack(side=tk.RIGHT, padx=5)
        
        # Autoscroll toggle (right side of footer)
        ttk.Checkbutton(status_frame, text="Autoscroll", variable=self.autoscroll).pack(side=tk.RIGHT, padx=5)
        
    def refresh_ports(self, highlight_new=None):
        """Refresh the list of available COM ports"""
        ports = serial.tools.list_ports.comports()
        port_list = [f"{port.device} - {port.description}" for port in ports]
        
        if port_list:
            self.port_combo['values'] = port_list
            
            # If a new port should be highlighted, select it
            if highlight_new:
                for idx, port_str in enumerate(port_list):
                    if highlight_new in port_str:
                        self.port_combo.current(idx)
                        return
            
            # Otherwise select first port if nothing is selected
            if not self.port_combo.get() or self.port_combo.get() == 'No ports available':
                if len(port_list) > 0:
                    self.port_combo.current(0)
        else:
            self.port_combo['values'] = ['No ports available']
            self.port_combo.current(0)
            
    def toggle_connection(self):
        """Connect or disconnect from the serial port"""
        if not self.running:
            self.connect()
        else:
            self.disconnect()
            
    def connect(self):
        """Connect to the selected serial port"""
        port_selection = self.port_combo.get()
        if not port_selection or port_selection == 'No ports available':
            messagebox.showerror("Error", "Please select a valid COM port")
            return
            
        # Extract port name (e.g., "COM3" from "COM3 - USB Serial Port")
        port_name = port_selection.split(' - ')[0]
        baud_rate = int(self.baud_combo.get())
        
        try:
            # Open port for monitoring
            self.serial_port = serial.Serial(
                port=port_name,
                baudrate=baud_rate,
                timeout=0.1
            )
            
            self.running = True
            self.connect_btn.config(text="Disconnect")
            self.status_label.config(text=f"Connected to {port_name} @ {baud_rate} baud")
            
            # Save last connected port and baud rate for autoconnect
            self.last_connected_port = port_name
            self.last_baud_rate = baud_rate
            
            # Start reading thread
            self.read_thread = threading.Thread(target=self.read_serial, daemon=True)
            self.read_thread.start()
            
        except serial.SerialException as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            self.status_label.config(text="Connection failed")
            
    def disconnect(self):
        """Disconnect from the serial port"""
        self.running = False
        
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            
        self.connect_btn.config(text="Connect")
        self.status_label.config(text="Disconnected")
        
    def read_serial(self):
        """Read data from serial port in a separate thread"""
        while self.running:
            try:
                if self.serial_port and self.serial_port.is_open and self.serial_port.in_waiting:
                    data = self.serial_port.readline().decode('utf-8', errors='replace').rstrip()
                    if data:
                        self.display_line(data)
                else:
                    time.sleep(0.01)  # Small delay to prevent CPU spinning
                    
            except serial.SerialException:
                self.root.after(0, self.disconnect)
                break
            except Exception as e:
                print(f"Error reading serial: {e}")
                
    def display_line(self, line):
        """Display a line of text with color coding and optional timestamp"""
        def update_ui():
            # Add timestamp if enabled
            if self.show_timestamp.get():
                timestamp = datetime.now().strftime("[%H:%M:%S.%f")[:-3] + "] "
                self.output_text.insert(tk.END, timestamp, 'timestamp')
            
            # Check for color patterns at start of line
            applied_color = None
            line_stripped = line.lstrip()  # Remove leading whitespace for checking
            
            for prefix, color in self.color_patterns:
                if line_stripped.upper().startswith(prefix.upper()):
                    applied_color = color
                    break
            
            # Insert the line with appropriate color
            if applied_color:
                self.output_text.insert(tk.END, line + '\n', applied_color)
            else:
                self.output_text.insert(tk.END, line + '\n')
            
            # Auto-scroll to bottom if enabled
            if self.autoscroll.get():
                self.output_text.see(tk.END)
        
        self.root.after(0, update_ui)
        
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
    
    def copy_to_clipboard(self):
        """Copy all console output to clipboard"""
        content = self.output_text.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.root.update()  # Keep the clipboard content after window closes
        
        # Brief visual feedback
        original_text = self.status_label.cget('text')
        self.status_label.config(text="Copied to clipboard!")
        self.root.after(1500, lambda: self.status_label.config(text=original_text))
        
    def save_history(self):
        """Save the current output to a text file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"serial_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    content = self.output_text.get(1.0, tk.END)
                    f.write(content)
                messagebox.showinfo("Success", f"Log saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def monitor_ports(self):
        """Monitor for COM port connections and disconnections"""
        while self.monitoring:
            try:
                # Get current ports
                current_ports = {port.device for port in serial.tools.list_ports.comports()}
                
                # Check for newly connected ports
                new_ports = current_ports - self.known_ports
                if new_ports:
                    # Get the newest port (assuming it's the last one alphabetically)
                    newest_port = sorted(new_ports)[-1]
                    self.root.after(0, self.on_port_connected, newest_port)
                
                # Check for disconnected ports
                removed_ports = self.known_ports - current_ports
                if removed_ports:
                    for port in removed_ports:
                        self.root.after(0, self.on_port_disconnected, port)
                
                # Update known ports
                self.known_ports = current_ports
                
                # Check every second
                time.sleep(1)
                
            except Exception as e:
                print(f"Error monitoring ports: {e}")
                time.sleep(1)
    
    def on_port_connected(self, port_name):
        """Handle new port connection"""
        # Refresh and highlight the new port
        self.refresh_ports(highlight_new=port_name)
        
        # Check if autoconnect is enabled and this is the last connected port
        if self.autoconnect.get() and self.last_connected_port == port_name and not self.running:
            # Restore the baud rate if saved
            if self.last_baud_rate:
                baud_values = self.baud_combo['values']
                if str(self.last_baud_rate) in baud_values:
                    self.baud_combo.set(str(self.last_baud_rate))
            
            # Auto-connect to the device
            self.connect()
            self.status_label.config(text=f"Auto-connected to {port_name}")
        else:
            # Update status to show connection
            self.status_label.config(text=f"New device connected: {port_name}")
            
            # Flash the combobox briefly to draw attention
            original_bg = self.port_combo.cget('background')
            self.port_combo.configure(background='#4caf50')  # Green highlight
            self.root.after(500, lambda: self.port_combo.configure(background=original_bg))
    
    def on_port_disconnected(self, port_name):
        """Handle port disconnection"""
        # Refresh port list
        self.refresh_ports()
        
        # If we were connected to this port, disconnect
        if self.serial_port and self.serial_port.is_open:
            if self.serial_port.port == port_name:
                self.disconnect()
                self.status_label.config(text=f"({port_name}) Device Disconnected")
    
    def show_help(self):
        """Show help dialog with color settings and info"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help & Settings")
        help_window.geometry("600x500")
        help_window.transient(self.root)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(help_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Color Settings
        color_frame = ttk.Frame(notebook, padding="10")
        notebook.add(color_frame, text="Color Settings")
        
        ttk.Label(color_frame, text="Color-Coded Output", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        ttk.Label(color_frame, text="Lines starting with these prefixes are automatically colored:", 
                 wraplength=550, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 10))
        
        # Color pattern display
        color_text = tk.Text(color_frame, height=15, width=70, wrap=tk.WORD, font=('Consolas', 9))
        color_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure the same color tags
        color_text.tag_config('red', foreground='#f44336')
        color_text.tag_config('orange', foreground='#ff9800')
        color_text.tag_config('blue', foreground='#2196f3')
        color_text.tag_config('green', foreground='#4caf50')
        color_text.tag_config('gray', foreground='#9e9e9e')
        color_text.tag_config('bold', font=('Consolas', 9, 'bold'))
        
        # Add examples
        color_text.insert(tk.END, "Red (Errors):\n", 'bold')
        color_text.insert(tk.END, "  [ERROR] Message\n", 'red')
        color_text.insert(tk.END, "  ERROR: Message\n\n", 'red')
        
        color_text.insert(tk.END, "Orange (Warnings):\n", 'bold')
        color_text.insert(tk.END, "  [WARN] Message\n", 'orange')
        color_text.insert(tk.END, "  [WARNING] Message\n", 'orange')
        color_text.insert(tk.END, "  WARN: Message\n", 'orange')
        color_text.insert(tk.END, "  WARNING: Message\n\n", 'orange')
        
        color_text.insert(tk.END, "Blue (Info):\n", 'bold')
        color_text.insert(tk.END, "  [INFO] Message\n", 'blue')
        color_text.insert(tk.END, "  INFO: Message\n\n", 'blue')
        
        color_text.insert(tk.END, "Green (Success):\n", 'bold')
        color_text.insert(tk.END, "  [SUCCESS] Message\n", 'green')
        color_text.insert(tk.END, "  SUCCESS: Message\n\n", 'green')
        
        color_text.insert(tk.END, "Gray (Debug):\n", 'bold')
        color_text.insert(tk.END, "  [DEBUG] Message\n", 'gray')
        color_text.insert(tk.END, "  DEBUG: Message\n\n", 'gray')
        
        color_text.insert(tk.END, "Note: Matching is case-insensitive and ignores leading whitespace.")
        color_text.config(state='disabled')
        
        # Tab 2: Usage
        usage_frame = ttk.Frame(notebook, padding="10")
        notebook.add(usage_frame, text="Usage")
        
        usage_text = tk.Text(usage_frame, wrap=tk.WORD, font=('Arial', 9))
        usage_text.pack(fill=tk.BOTH, expand=True)
        
        usage_content = """Serial Monitor - Quick Start Guide

1. SELECT PORT
   Choose your COM port from the dropdown menu.
   The app automatically detects new device connections.

2. SET BAUD RATE
   Select the appropriate baud rate (default: 115200).
   Common rates: 9600, 19200, 38400, 57600, 115200

3. CONNECT
   Click "Connect" to start monitoring.
   The button changes to "Disconnect" when active.

4. FEATURES
   • Timestamp: Add timestamps to each line
   • Clear: Clear the output window
   • Copy: Copy all output to clipboard
   • Save: Export log to a timestamped text file

5. AUTO PORT DETECTION
   When a new device connects:
   - The port list automatically refreshes
   - New port is highlighted in green
   - Status bar shows the connection

6. TROUBLESHOOTING
   Permission Error:
   - Close other apps using the COM port
   - Run as Administrator if needed
   - Check Device Manager for port conflicts
"""
        
        usage_text.insert('1.0', usage_content)
        usage_text.config(state='disabled')
        
        # Tab 3: About
        about_frame = ttk.Frame(notebook, padding="10")
        notebook.add(about_frame, text="About")
        
        ttk.Label(about_frame, text="Serial Monitor", font=('Arial', 16, 'bold')).pack(pady=(10, 5))
        ttk.Label(about_frame, text="v1.1.0", font=('Arial', 10)).pack(pady=(0, 20))
        
        about_text = """A lightweight serial port monitor with:
        
• Real-time serial data monitoring
• Automatic color-coded output
• COM port auto-detection
• Timestamp support
• Export to text files
• Copy to clipboard
• Dark theme interface

Built with Python, tkinter, and pyserial.
"""
        ttk.Label(about_frame, text=about_text, justify=tk.LEFT, wraplength=550).pack(pady=10)
        
        # Close button
        ttk.Button(help_window, text="Close", command=help_window.destroy).pack(pady=10)


def main():
    root = tk.Tk()
    app = SerialMonitor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
