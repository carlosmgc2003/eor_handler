#!/usr/bin/env python

import RPi.GPIO as GPIO
import rospy
from std_msgs.msg import Int32



but_pin = 37
rate_hz = 10
side = "right"

GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
GPIO.setup(but_pin, GPIO.IN)  # button pin set as input
pub = rospy.Publisher(side + '_eor', Int32, queue_size=10)
rospy.init_node('eor_pub', anonymous=True)
rate = rospy.Rate(rate_hz) # 10hz

def eor_pub():
    while not rospy.is_shutdown():
        if GPIO.input(but_pin) == GPIO.LOW:
                #GPIO.wait_for_edge(but_pin, GPIO.RISING)
                rospy.loginfo('EOR %s Soltado', side)
                pub.publish(0)
        elif GPIO.input(but_pin) == GPIO.HIGH:
                #GPIO.wait_for_edge(but_pin, GPIO.FALLING)
                rospy.loginfo('EOR %s Apretado', side)
                pub.publish(1)
        rate.sleep()

if __name__ == '__main__':
    try:
        eor_pub()
    except rospy.ROSInterruptException:
        GPIO.cleanup()  # cleanup all GPIOs
        pass
