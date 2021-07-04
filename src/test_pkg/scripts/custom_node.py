#!/usr/bin/env python3
import rospy
import random
from test_pkg.msg import CustomMessage

rospy.init_node('pub_node')
pub = rospy.Publisher('custom_topic',CustomMessage)
rate = rospy.Rate(0.5)
count = 0
while not rospy.is_shutdown():
	msg = CustomMessage()
	msg.name = 'CustomMessage_'+str(count)
	msg.value = random.random()
	pub.publish(msg)
	count += 1
	rate.sleep()
