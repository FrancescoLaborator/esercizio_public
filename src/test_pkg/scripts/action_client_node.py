#!/usr/bin/env python3
import rospy
import time
import actionlib
from test_pkg.msg import TimerAction, TimerGoal, TimerResult, TimerFeedback

def feedback_callback(feedback):
	print('Time elapsed: '+str(round(feedback.partial_time_elapsed,2)))
	if feedback.partial_time_elapsed>=5:
		client.cancel_all_goals()

rospy.init_node('timer_action_client_node')
client = actionlib.SimpleActionClient('timer', TimerAction)
client.wait_for_server()
goal = TimerGoal()
goal.duration_time = 10.0
client.send_goal(goal, feedback_cb=feedback_callback)
client.wait_for_result()
print('Time elapsed: '+str(client.get_result()))
