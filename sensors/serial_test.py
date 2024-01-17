import serial

# Configure the serial port
ser = serial.Serial("/dev/ttyUSB0", 9600)

while True:
    if ser.in_waiting > 0:
        received_line = ser.readline()
        print(received_line)
