#!/usr/bin/env python

import rospy
from local_tracker import LocalTracker as LT
from geometry.msg import PointStamped, TwistWithCovarianceStamped, Pose


tracker = LT()

gnss = rospy.Subscriber("/sensors/gnss/odom", PointStamped, GNSSHandler)
odom = rospy.Subscriber("/sensors/odom", TwistWithCovarianceStamped, ODOMHandler)
pub = rospy.Publisher("/estimate/pose", Pose, queue_size=10)

def GNSSHandler(data):
	
	# TODO get positional data from message, and add to LocalTracker object
	
	continue

def ODOMHandler(data):
	
	# TODO get positional data from message, and add to LocalTracker object
	
	# TODO get orientation and position data from LocalTracker and publish
	
	continue

rospy.init_node('local_tracker_node', anonymous=True)
rate = rospy.Rate(10) # 10hz
while not rospy.is_shutdown():
	hello_str = "hello world %s" % rospy.get_time()
	rospy.loginfo(hello_str)
	pub.publish(hello_str)
	rate.sleep()
	