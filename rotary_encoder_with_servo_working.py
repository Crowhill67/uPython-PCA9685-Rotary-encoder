# also see file 'Rotary encoder and servo.jpg'

# this program is dependent on the rotary encoder, pc9685 and servo libraries
# You can use the program to move a servo with 10 μs increments
 

# import all libraries
from machine import I2C, Pin
import sys
import servo
import time
from rotary_irq_esp import RotaryIRQ
print('Libraries have been imported')

# create the objects needed
r = RotaryIRQ(pin_num_clk=14, pin_num_dt=13, min_val=51, max_val=230, reverse=False, range_mode=RotaryIRQ.RANGE_WRAP)
i2c = I2C(sda=Pin(21),scl=Pin(22))
srv1=servo.Servos(i2c,address=0x40,freq=50, min_us=510, max_us=2300, degrees=180) #This object is the actual pca9685board, not the servo on the board
"""
In this case you are accessing servo(0) on board srv1. By rights it would be handier to name this object pca1, pca2 etc., then access the servos wiyh
pca1.position(0, us = 'value here')
pca1.position(1, us = 'value here')
Then for a second board:
create an object for the board:
pca2=servo.Servos(i2c,address=0x41,freq=50, min_us=510, max_us=2300, degrees=180)
and access it's servos by:
pca2.position(0, us = 'value here')
pca2.position(1, us = 'value here')

There must be a cool way of mapping the servo's to the boars, so you can access them directly. Maybe look at Mitri's documentation on the hexapod.
"""

print('All objects have been created')

try:
    val_old = r.value()
    while True:
        val_new = r.value()
        
        if val_old != val_new:
            val_old = val_new
            print('result =', val_new*10)
            srv1.position(0,us=val_new*10)
        time.sleep_ms(50)

except KeyboardInterrupt:
    print('KeyboardInterrupt detected.')
    print('Ending programme, Bye Bye..')
    srv1.release(0)
    sys.exit()


