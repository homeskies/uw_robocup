#!/usr/bin/env python
import rospy
from std_msgs.msg import Header, ColorRGBA
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import PoseStamped, Pose, Vector3, PoseWithCovarianceStamped

class Teleport():
    def __init__(self):
        self.set_rviz = rospy.Publisher("initialpose", PoseWithCovarianceStamped, queue_size=10)
        rospy.wait_for_service("/gazebo/set_model_state")
        try:
            self.set_gazebo = rospy.ServiceProxy("/gazebo/set_model_state", SetModelState)
        except:
            print("Service call failed")

    def move_to_pose(self, pose):
    pose_w = PoseWithCovarianceStamped()
    pose_w.pose.pose = pose
    pose_w.pose.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853892326654787]
    pose_w.header = Header(stamp=rospy.Time.now(), frame_id="map")
    self.set_rviz.publish(pose_w)
    model = ModelState()
    model.model_name = "fetch"
    model.pose = pose
    self.set_gazebo(model)