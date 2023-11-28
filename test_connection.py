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
            ser.write(b"51,10,0,1000,1,100,100,100 \n") #Registers solid color event, starts at time 1000ms, at color Red: 100, Green: 100, Blue 100
            ser.write(b"51,10,0,2000,1,255,0,0 \n")     #Registers solid color event
            ser.write(b"51,10,0,3000,1,0,255,0 \n")     #Registers solid color event
            ser.write(b"51,10,0,4000,1,10,0,255 \n")    #Registers solid color event
            ser.write(b"51,10,0,5000,2,30,0,30,0,0,100,0,100,100 \n")    #Registers Orbs Pattern forward
            ser.write(b"51,10,0,10000,3,30,0,0,0,100,0,100,100 \n")    #Registers Playbar Pattern forward
            ser.write(b"51,10,0,15000,2,30,1,30,100,0,0,100,100,0 \n")    #Registers Orbs Pattern reverse
            ser.write(b"51,10,0,20000,3,30,1,100,0,0,100,100,0 \n")    #Registers Playbar Pattern forward
            ser.write(b"51,10,0,25000,4,1000,100,100,100,0,10,10 \n")
            ser.write(b"51,10,0,30000,5 \n")             #Rainbow Test Pattern
            ser.write(b"51,10,0,35000,1,0,0,0 \n")
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