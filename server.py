import socket
import time
from pymavlink import mavutil

TCP_IP = 
TCP_PORT = 21
BUFFER_SIZE = 20 # Normally 1024, but I want fast response


master = mavutil.mavlink_connection( # aracin baglantisi
            '/dev/ttyACM0',
            baud=115200)

#master = "mavutil.mavlink_connection('udpin:192.168.2.2:14550')" #eğer bilgisayardan konttrol edilecekse
def set_rc_channel_pwm(id, pwm=1500):

    if id < 1:
        print("Channel does not exist.")
        return


    if id < 9: # ardusubla iletisim
        rc_channel_values = [65535 for _ in range(8)]
        rc_channel_values[id - 1] = pwm
        master.mav.rc_channels_override_send(
            master.target_system,
            master.target_component,
            *rc_channel_values)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

def ileri():
    set_rc_channel_pwm(5, 1650) # ileri git
def geri():
    set_rc_channel_pwm(5, 1400) # geri git
def sol():
    set_rc_channel_pwm(6, 1400)
def sag():
    set_rc_channel_pwm(6, 1600)
def don():
    set_rc_channel_pwm(4, 1400)

conn, addr = s.accept()
print ('Connection address:', addr)
while (True):
    data = conn.recv(BUFFER_SIZE)
    print ("received data:", data)
    conn.send(data)  # echo
    if (data == "ileri"):
    	ileri()
    elif(data =="sag"):
    	sag()
    elif(data == "sol"):
    	sol()
    elif(data == "geri"):
    	geri()
    elif(data == "don"):
    	don()
    else:
    	time.sleep(0.1)
    data = ""
conn.close()
