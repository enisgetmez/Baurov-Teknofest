from pymavlink import mavutil

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


def ileri():
    set_rc_channel_pwm(5, 1650) # ileri git    
def geri():
    set_rc_channel_pwm(5, 1400) # geri git
def sol():
    set_rc_channel_pwm(6, 1400)
def sag():
    set_rc_channel_pwm(6, 1600)
def alcal():
    set_rc_channel_pwm(3, 1450)
def yuksel():
    set_rc_channel_pwm(3, 1510)
def don():
    set_rc_channel_pwm(4, 1400)

git = 0
while(True):
	if(4500 > git):
		yuksel()
		ileri()
		git +=1
		print(git)
	elif(4499 < git < 6000 ):
		sol()
		git +=1
		print(git)
    else:
    	alcal()


