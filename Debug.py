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


# Solid Color Command
# Example ser.write(b"51,10,0,1000,1,100,100,100 \n")
# 51 : Start of command
# 10 : Configure Event
# 0  : LED Strip 0
# 1000 : Start time in milliseconds
# 1 : Solid Color Animation ID
# 100 : Color Red
# 100 : Color Green
# 100 : Color Blue

def send_and_receive(ser):
    if ser is not None:
        try:
            ser.write(b"51,1 \n") #stops anything actively running
            ser.write(b"51,12 \n") #clears event buffer
            
            # ------------- Registering Events ---------------

            ser.write(b"51,10,0,1000,2,30,1,30,240,40,0,0,240,40 \n") 

            # ------------ End of Event Registry -------------
            
            ser.write(b"51,2 \n") #Runs strip

            # Wait for a moment to receive the response
            time.sleep(0.1)

            # Read and print the response
            response = ser.read_all().decode('utf-8')
            print(f"Received response: {response}")
        except serial.SerialException as e:
            print(f"Error: {e}")
        finally:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    serial_port = open_serial_port()
    send_and_receive(serial_port)