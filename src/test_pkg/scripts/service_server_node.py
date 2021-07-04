#!/usr/bin/env python3
import rospy
from test_pkg.srv import WordCount,WordCountResponse

def count_callback(request):
	return WordCountResponse(len(request.words.split()))

rospy.init_node('service_server_node')
rospy.Service('word_count',WordCount,count_callback)
rospy.spin()
