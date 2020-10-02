import pyvjoy
import time
import socket
import sys
from serial import Serial

# Define constants
SERIAL_BUFF_SIZE = 98
ANALOG_ON = "1"
JOY_CENT_OUT = int(32768/2)

# Setup virtual joystick device using pyvjoy
j = pyvjoy.VJoyDevice(1) # dev no. 1

# Establish tcp socket for comms
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.2.239', 5557)
sock.bind(server_address)
sock.listen(1)
print("waiting for joystick connection...")
connection, client_address = sock.accept()
print("found joystick at ", client_address, "!")

def analogMap(value, outMax, inMax):
    if value >= inMax:
        outval = outMax
    else:
        outval = (outMax/inMax) * value

    return int(outval)

while True:
    # Recieve buffer from joystick box and echo back
    data = connection.recv(SERIAL_BUFF_SIZE)
    if data:
        connection.sendall(data)
    else:
        pass

    # ======================================================================
    # DESERIALIZE DATA
    # ======================================================================
    data = data.decode()

    # ++++++++++++++++++++++++++++++++++++++++++++++++++
    # Joy 1
    # ++++++++++++++++++++++++++++++++++++++++++++++++++
    # ------------------------------
    # X1
    # ------------------------------
    if data[4] == ANALOG_ON:
        j1XLeft = int(data[1:4])
    else:
        j1XLeft = 0

    if data[8] == ANALOG_ON:
        j1XRight = int(data[5:8])
    else:
        j1XRight = 0

    # ------------------------------
    # Y1
    # ------------------------------
    if data[12] == ANALOG_ON:
        j1YDown = int(data[9:12])
    else:
        j1YDown = 0

    if data[16] == ANALOG_ON:
        j1YUp = int(data[13:16])
    else:
        j1YUp = 0

    # ------------------------------
    # Z1
    # ------------------------------
    if data[20] == ANALOG_ON:
        j1ZLeft = int(data[17:20])
    else:
        j1ZLeft = 0

    if data[24] == ANALOG_ON:
        j1ZRight = int(data[21:24])
    else:
        j1ZRight = 0
        
    # ++++++++++++++++++++++++++++++++++++++++++++++++++
    # Joy 2
    # ++++++++++++++++++++++++++++++++++++++++++++++++++
    # ------------------------------
    # X2
    # ------------------------------
    if data[28] == ANALOG_ON:
        j2XLeft = int(data[25:28])
    else:
        j2XLeft = 0

    if data[32] == ANALOG_ON:
        j2XRight = int(data[29:32])
    else:
        j2XRight = 0

    # ------------------------------
    # Y2
    # ------------------------------
    if data[36] == ANALOG_ON:
        j2YDown = int(data[33:36])
    else:
        j2YDown = 0

    if data[40] == ANALOG_ON:
        j2YUp = int(data[37:40])
    else:
        j2YUp = 0

    # ------------------------------
    # Z2
    # ------------------------------
    if data[44] == ANALOG_ON:
        j2ZLeft = int(data[41:44])
    else:
        j2ZLeft = 0

    if data[48] == ANALOG_ON:
        j2ZRight = int(data[45:48])
    else:
        j2ZRight = 0

    # ======================================================================
    # OUTPUT JOY COMMANDS
    # ======================================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++
    # Joy 1
    # ++++++++++++++++++++++++++++++++++++++++++++++++++
    # ------------------------------
    # X1
    # ------------------------------
    if j1XLeft > 0:
        j.set_axis(pyvjoy.HID_USAGE_X, JOY_CENT_OUT - analogMap(j1XLeft,JOY_CENT_OUT,550))
    elif j1XRight > 0:
        j.set_axis(pyvjoy.HID_USAGE_X, JOY_CENT_OUT + analogMap(j1XRight,JOY_CENT_OUT,550))
    else:
        j.set_axis(pyvjoy.HID_USAGE_X, JOY_CENT_OUT)

    # ------------------------------
    # Y1
    # ------------------------------
    if j1YDown > 0:
        j.set_axis(pyvjoy.HID_USAGE_Y, JOY_CENT_OUT - analogMap(j1YDown,JOY_CENT_OUT,550))
    elif j1YUp > 0:
        j.set_axis(pyvjoy.HID_USAGE_Y, JOY_CENT_OUT + analogMap(j1YUp,JOY_CENT_OUT,550))
    else:
        j.set_axis(pyvjoy.HID_USAGE_Y, JOY_CENT_OUT)

    # ------------------------------
    # Z1
    # ------------------------------
    if j1ZLeft > 0:
        j.set_axis(pyvjoy.HID_USAGE_Z, JOY_CENT_OUT - analogMap(j1ZLeft,JOY_CENT_OUT,550))
    elif j1ZRight > 0:
        j.set_axis(pyvjoy.HID_USAGE_Z, JOY_CENT_OUT + analogMap(j1ZRight,JOY_CENT_OUT,550))
    else:
        j.set_axis(pyvjoy.HID_USAGE_Z, JOY_CENT_OUT)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++
    # Joy 2
    # ++++++++++++++++++++++++++++++++++++++++++++++++++
    # ------------------------------
    # X2
    # ------------------------------
    if j2XLeft > 0:
        j.set_axis(pyvjoy.HID_USAGE_RX, JOY_CENT_OUT - analogMap(j2XLeft,JOY_CENT_OUT,550))
    elif j2XRight > 0:
        j.set_axis(pyvjoy.HID_USAGE_RX, JOY_CENT_OUT + analogMap(j2XRight,JOY_CENT_OUT,550))
    else:
        j.set_axis(pyvjoy.HID_USAGE_RX, JOY_CENT_OUT)

    # ------------------------------
    # Y2
    # ------------------------------
    if j2YDown > 0:
        j.set_axis(pyvjoy.HID_USAGE_RY, JOY_CENT_OUT - analogMap(j2YDown,JOY_CENT_OUT,550))
    elif j2YUp > 0:
        j.set_axis(pyvjoy.HID_USAGE_RY, JOY_CENT_OUT + analogMap(j2YUp,JOY_CENT_OUT,550))
    else:
        j.set_axis(pyvjoy.HID_USAGE_RY, JOY_CENT_OUT)

    # ------------------------------
    # Z2
    # ------------------------------
    if j2ZLeft > 0:
        j.set_axis(pyvjoy.HID_USAGE_RZ, JOY_CENT_OUT - analogMap(j2ZLeft,JOY_CENT_OUT,550))
    elif j2ZRight > 0:
        j.set_axis(pyvjoy.HID_USAGE_RZ, JOY_CENT_OUT + analogMap(j2ZRight,JOY_CENT_OUT,550))
    else:
        j.set_axis(pyvjoy.HID_USAGE_RZ, JOY_CENT_OUT)



