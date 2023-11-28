import time
import subprocess
from HelperFunctions import open_serial_port

# --- Solid Color Command
# Example ser.write(b"51,10,0,1000,1,100,100,100 \n")
# 51 : Start of command
# 10 : Configure Event
# 0  : LED Strip 0
# 1000 : Start time in milliseconds
# 1 : Solid Color Animation ID
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
# Example ser.write(b"51,10,0,15000,3,30,0,0,0,100,0,100,100 \n")
# 51 : Start of command
# 10 : Configure Event
# 0  : LED Strip 0
# 15000 : Start time in milliseconds
# 3 : Playbar Pattern Animation ID
# 30 : Rate of movement (1-50, higher number faster)
# 0 : Direction of moment (0 outwards, 1 inwards)
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
            ser.write(b"51,10,0,1000,1,100,100,100 \n")                 #Solid color event, starts at time 1000ms, at color Red: 100, Green: 100, Blue 100
            ser.write(b"51,10,0,2000,1,255,0,0 \n")                     #Solid color event
            ser.write(b"51,10,0,3000,1,0,255,0 \n")                     #Solid color event
            ser.write(b"51,10,0,4000,1,10,0,255 \n")                    #Solid color event
            ser.write(b"51,10,0,5000,2,30,0,30,0,0,250,0,100,100 \n")     #Orbs Pattern forward
            ser.write(b"51,10,0,10000,2,30,1,30,240,40,0,0,200,40 \n")  #Orbs Pattern reverse
            ser.write(b"51,10,0,15000,3,30,0,0,0,250,0,100,100 \n")     #Playbar Pattern forward
            ser.write(b"51,10,0,23000,3,30,1,240,40,0,0,100,20 \n")     #Playbar Pattern forward
            ser.write(b"51,10,0,30000,4,1000,100,100,100,0,10,10 \n")   #Alternating Color Pattern
            ser.write(b"51,10,0,35000,5 \n")                            #Rainbow Test Pattern
            ser.write(b"51,10,0,40000,1,0,0,0 \n")                      #Blank
            ser.write(b"51,10,1,43000,3,30,0,0,0,250,0,100,100 \n")
            ser.write(b"51,10,1,47000,1,0,0,0 \n")
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