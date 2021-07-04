#!/usr/bin/env python3
import rospy
from test_pkg.srv import WordCount,WordCountRequest

rospy.init_node('service_client_node')
rospy.wait_for_service('word_count')
word_counter_proxy = rospy.ServiceProxy('word_count', WordCount)
req = WordCountRequest()
req.words = 'two three'
res = word_counter_proxy(req)
print('The number of words are '+str(res.count))
