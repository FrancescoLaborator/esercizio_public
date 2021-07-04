#!/usr/bin/env python3
import rospy
import random
from std_msgs.msg import Int32

rospy.init_node('writer')
pub = rospy.Publisher('data_topic', Int32)
freq = rospy.get_param('/writer/freq', 1)
min_value = rospy.get_param('/writer/min', 1)
max_value = rospy.get_param('/writer/max', 10)
rate = rospy.Rate(freq)
while not rospy.is_shutdown():
	pub.publish(random.randint(min_value, max_value))
	rate.sleep()
