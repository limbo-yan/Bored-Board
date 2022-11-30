import serial
import time
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=0.1)

def send_val_to_arduino(ai_input):
    arduino.write(bytes(ai_input, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

def get_val_from_arduino():
    data = arduino.readline()
    while data == bytes('', 'utf-8'):
        data = arduino.readline()
    data = data.decode("utf-8")
    return data

# while True:
data = get_val_from_arduino()
print(data)

num = input("Move: ") # Taking input from user
value = send_val_to_arduino(num)
print(value) # printing the value
