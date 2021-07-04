#!/usr/bin/env python3
import rospy
import time
import actionlib
from test_pkg.msg import TimerAction, TimerGoal, TimerResult, TimerFeedback

def timer_callback(goal):
	start_time = time.time()
	result = TimerResult()
	curr_time = time.time()
	while(curr_time - start_time) < goal.duration_time:
		if server.is_preempt_requested():
			# Cancel goal request received
			result.total_time_elapsed = curr_time - start_time
			server.set_preempted(result,'Timer PREEMPTED')
			return
		feedback = TimerFeedback()
		feedback.partial_time_elapsed = curr_time - start_time
		server.publish_feedback(feedback)
		time.sleep(1)
		curr_time = time.time()

	result.total_time_elapsed = curr_time - start_time
	server.set_succeeded(result,'Timer SUCCEFULLY COMPLETED')

rospy.init_node('timer_action_server_node')
server = actionlib.SimpleActionServer('timer', TimerAction, timer_callback, False)
server.start()
rospy.spin()
