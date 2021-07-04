#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32

global buffer, buffer_size
buffer_size = rospy.get_param('/reader/buffer_len', 5)
buffer = []

def read_callback(msg):
	global buffer, buffer_size
	if len(buffer) == buffer_size:
		buffer.pop(0)
	buffer.append(msg.data)
	print(buffer)

rospy.init_node('reader')
sub = rospy.Subscriber('data_topic', Int32, read_callback)
rospy.spin()
