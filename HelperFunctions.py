import time
import subprocess

try:
    import serial
except ImportError:
    print("pyserial module not found. Installing...")
    subprocess.run(["pip", "install", "pyserial"])
    print("pyserial module installed. Please run the script again.")
    exit()

def open_serial_port():
    # Search for the first available ttyACM device
    for i in range(0, 10):  # You can adjust the range based on your needs
        port = f'/dev/ttyACM{i}'
        try:
            ser = serial.Serial(port, baudrate=115200, timeout=1)
            print(f"Opened serial port on {port} at 115200 bps")
            return ser
        except serial.SerialException:
            pass

    print("No ttyACM device found.")
    return None

