import time
import subprocess
try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("pyserial module not found. Installing...")
    subprocess.run(["pip", "install", "pyserial"])
    print("pyserial module installed. Please run the script again.")
    exit()


# --- Solid Color Command
# Example ser.write(b"51,10,0,1000,1,20,100,100,100 \n")
# 51 : Start of command
# 10 : Configure Event
# 0  : LED Strip 0
# 1000 : Start time in milliseconds
# 1 : Solid Color Animation ID
# 20 : Fade Speed
# 100 : Color Red
# 100 : Color Green
# 100 : Color Blue

# --- Registers Orbs Pattern
# Example ser.write(b"51,10,0,5000,2,30,0,30,0,0,100,0,50,50 \n")
# 51 : Start of command
# 10 : Configure Event
# 0  : LED Strip 0
# 5000 : Start time in milliseconds
# 2 : Orb Pattern Animation ID
# 30 : Rate of movement (1-50, higher number faster)
# 0 : Direction of moment (0 outwards, 1 inwards)
# 30 : Spacing of orbs (10 - 90 number of pixels between orbs)
# 0 : Orb Color Red
# 0 : Orb Color Green
# 100 : Orb Color Blue
# 0 : Tail Color Red
# 50 : Tail Color Green
# 50 : Tail Color Blue

# --- Playbar Pattern
# Example ser.write(b"51,10,0,15000,3,30,0,0,180,0,0,100,0,100,100 \n")
# 51 : Start of command
# 10 : Configure Event
# 0  : LED Strip 0
# 15000 : Start time in milliseconds
# 3 : Playbar Pattern Animation ID
# 30 : Rate of movement (1-50, higher number faster)
# 0 : Direction of moment (0 outwards, 1 inwards)
# 0 : Start Pixel
# 180 : End Pixel
# 0 : Orb Color Red
# 0 : Orb Color Green
# 100 : Orb Color Blue
# 0 : Tail Color Red
# 50 : Tail Color Green
# 50 : Tail Color Blue

# --- Alternating Pattern
# Example ser.write(b"51,10,0,30000,4,1000,100,100,100,0,10,10 \n")
# 51 : Start of command
# 10 : Configure Event
# 0  : LED Strip 0
# 30000 : Start time in milliseconds
# 4 : Playbar Pattern Animation ID
# 1000 : Rate of movement (1-50, higher number faster)
# 100 : Color 1 Red
# 100 : Color 1 Green
# 100 : Color 1 Blue
# 0 : Color 2 Red
# 10 : Color 2 Green
# 10 : Color 2 Blue

def send_and_receive(ser):
    if ser is not None:
        try:
            ser.write(b"51,1 \n") #stops anything actively running
            ser.write(b"51,12 \n") #clears event buffer
            
            # ------------- Registering Events ---------------
            
            ser.write(b"51,10,0,1000,1,20,100,100,100 \n")                   #Solid color event, starts at time 1000ms, at color Red: 100, Green: 100, Blue 100
            ser.write(b"51,10,0,2000,1,20,255,0,0 \n")                       #Solid color event
            ser.write(b"51,10,0,3000,1,20,0,255,0 \n")                       #Solid color event
            ser.write(b"51,10,0,4000,1,20,0,0,255 \n")                       #Solid color event
            ser.write(b"51,10,0,5000,2,30,0,30,0,0,250,0,100,100 \n")        #Orbs Pattern forward
            ser.write(b"51,10,0,10000,2,30,1,30,240,40,0,0,200,40 \n")       #Orbs Pattern reverse
            ser.write(b"51,10,0,15000,3,30,0,0,180,0,0,250,0,100,100 \n")    #Playbar Pattern forward
            ser.write(b"51,10,0,23000,3,30,1,180,0,240,40,0,0,100,20 \n")    #Playbar Pattern forward
            ser.write(b"51,10,0,30000,4,1000,100,100,100,0,10,10 \n")        #Alternating Color Pattern
            ser.write(b"51,10,0,35000,5 \n")                                 #Rainbow Test Pattern
            ser.write(b"51,10,0,40000,1,20,0,0,0 \n")                        #Blank            

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



def check_serial_port(port):
    try:
        ser = serial.Serial(port, baudrate=115200, timeout=0.005)
        ser.write(b"51,0\r\n")
        time.sleep(0.001)
        response = ser.readline().decode().strip()
        ser.close()
        if response == "2":
            return ser
        else:
            return False
    except serial.SerialException:
        return False

def find_serial_ports():
    ports = [port.device for port in serial.tools.list_ports.comports()]
    return ports

def main():
    serial_ports = find_serial_ports()

    if not serial_ports:
        print("No serial ports found.")
        return

    for port in serial_ports:
        print(f"Checking port {port}...")
        serial_port = check_serial_port(port)
        if check_serial_port(port) != False:
            serial_port.open()
            send_and_receive(serial_port)
            break
        else:
            print(f"No response from {port}.")

if __name__ == "__main__":
    main()