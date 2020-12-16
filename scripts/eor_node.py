#!/usr/bin/env python

import RPi.GPIO as GPIO
import rospy
from std_msgs.msg import Int32



but_pin = rospy.get_param('~pin')
rospy.loginfo('Parameter %s has value %s', rospy.resolve_name('~pin'), value)
rate_hz = rospy.get_param('~rate', 10)
rospy.loginfo('Parameter %s has value %s', rospy.resolve_name('~rate'), value)
side = rospy.get_param('~side')
rospy.loginfo('Parameter %s has value %s', rospy.resolve_name('~side'), value)

GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
GPIO.setup(but_pin, GPIO.IN)  # button pin set as input
pub = rospy.Publisher('eor_' + lado, Int32, queue_size=10)
rospy.init_node('eor_pub', anonymous=True)
rate = rospy.Rate(rate_hz) # 10hz

def eor_pub():
    while not rospy.is_shutdown():
        if GPIO.input(but_pin) == GPIO.HIGH:
                GPIO.wait_for_edge(but_pin, GPIO.FALLING)
                rospy.loginfo('EOR %s Soltado', side)
                pub.publish(0)
        elif GPIO.input(but_pin) == GPIO.LOW:
                GPIO.wait_for_edge(but_pin, GPIO.RISING)
                rospy.loginfo('EOR %s Apretado', side)
                pub.publish(1)
        rate.sleep()

if __name__ == '__main__':
    try:
        eor_pub()
    except rospy.ROSInterruptException:
        GPIO.cleanup()  # cleanup all GPIOs
        pass
