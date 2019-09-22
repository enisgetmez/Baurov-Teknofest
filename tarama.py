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
    set_rc_channel_pwm(3, 1600)
def don():
    set_rc_channel_pwm(4, 1400)

a = 0
git = 0
yon = 0
while(true):

	alcal()
	if(git == 0):
		if(100 > a):
			a += 1
			ileri()
		else:
			git = 1
    elif(git == 1):
    	if(10000  > yon):
    		sag()
    		yon +=1
    	elif(9999 < yon < 15000):
    		sol()
    		yon +=1
    	else:
    		yon = 0

