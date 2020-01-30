#! /usr/bin/env python

import rospy
import fetch_api
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import PoseStamped, Pose, Vector3, PoseWithCovarianceStamped
from moveit_msgs.msg import OrientationConstraint
import actionlib
from std_msgs.msg import Header, ColorRGBA
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionGoal
from visualization_msgs.msg import Marker


def teleport(rviz, gazebo, pose):
  pose_w = PoseWithCovarianceStamped()
  pose_w.pose.pose = pose
  pose_w.pose.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853892326654787]
  pose_w.header = Header(stamp=rospy.Time.now(), frame_id="map")
  rviz.publish(pose_w)
  model = ModelState()
  model.model_name = "fetch"
  model.pose = pose
  gazebo(model)


def wait_for_time():
  """
    Wait for simulated time to begin.
  """
  while rospy.Time().now().to_sec() == 0:
    pass


def main():
  rospy.init_node('coke_can_node')
  wait_for_time()

  # controls of Fetch
  ##### TODO: Uncomment these if nessecary
  head = fetch_api.Head()
  arm_joints = fetch_api.ArmJoints()
  arm = fetch_api.Arm()
  gripper = fetch_api.Gripper()
  # torso = fetch_api.Torso()
  
  set_rviz = rospy.Publisher("initialpose", PoseWithCovarianceStamped, queue_size=10)
  rospy.wait_for_service("/gazebo/set_model_state")
  try:
    set_gazebo = rospy.ServiceProxy("/gazebo/set_model_state", SetModelState)
  except:
    print("Service call failed")



  fetch_gripper = fetch_api.Gripper()
  move_base_client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
  move_base_client.wait_for_server()
  # move_arm_client = actionlib.SimpleActionClient("/play_motion", PlayMotionAction)
  # move_arm_client.wait_for_server()
  move_base_pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
  marker_pub = rospy.Publisher('visualization/msg', Marker, queue_size=10)
  rospy.sleep(0.5)
  print "Ready to move"

  ########## TODO: Uncomment this
  # shutdown handler
  # def shutdown():
  #   arm.cancel_all_goals()
  # rospy.on_shutdown(shutdown)

  # move base to the position near coke can
  pose = Pose()
  pose.position.x = 1.51860149414
  pose.position.y = -4.3
  pose.orientation.z = -0.713937033753
  pose.orientation.w = 0.700209905554
  

  goal = MoveBaseGoal()
  goal.target_pose.header.frame_id = "map"
  goal.target_pose.header.stamp = rospy.Time.now()
  goal.target_pose.pose = pose

  #pose 2 move to shelf
  pose2 = PoseStamped()
  pose2.header.frame_id = 'map'
  pose2.pose.position.x = 3.99776721001
  pose2.pose.position.y = -4.2840180397

  pose2.pose.position.z = 0.0
  pose2.pose.orientation.z = -0.713937033753
  pose2.pose.orientation.w = 0.700209905554

  marker = Marker(header=Header(stamp=rospy.Time.now(),
                                frame_id="map"),
                        pose=pose2.pose,
                        type=0,
                        scale=Vector3(x=2,y=.3,z=.3),
                        id=0,
                        color=ColorRGBA(r=1,a=1))
  marker_pub.publish(marker)

  move_base_client.send_goal(goal)
  teleport(set_rviz, set_gazebo, pose)

  wait = move_base_client.wait_for_result()
  if not wait:
      rospy.logerr("Action server not available!")
      rospy.signal_shutdown("Action server not available!")
  else:
      # move_base_client.get_result()
      print "Ready to pick up the coke can!"

  # move head
  head.pan_tilt(0, 0.7)
  print "Head moved!"

# ### MOVE ARM TO can
  pose = PoseStamped()
  pose.header.frame_id = 'base_link'
  pose.pose.position.x = 0.8
  pose.pose.position.y = 0
  pose.pose.position.z = 0.75
  pose.pose.orientation.w = 1
  arm.move_to_pose(pose)

  kwargs = {
      'allowed_planning_time': 20,
      'execution_timeout': 20,
      'num_planning_attempts': 1,
      'replan_attempts': 5,
      'replan': True,
      'orientation_constraint': None
  }

  error = arm.move_to_pose(pose, **kwargs)
  if error is not None:
      rospy.logerr('Pose failed: {}'.format(error))
  else:
      rospy.loginfo('Pose succeeded')
      print "Arm moved out!"

  gripper.close()

  # goal = PlayMotionGoal()
  # goal.motion_name = 'home'
  # goal.skip_planning = True
  # move_arm_client.send_goal(goal)
  # move_arm_client.wait_for_result(rospy.Duration(10.0))
  pose = [1.32, 1.40, -0.2, 1.72, 0.0, 1.66, 0.0]
  arm.move_to_joints(arm_joints.from_list(pose))

  print "Arm moved in!"
# # Move arm back to body
#   pose = PoseStamped()
#   pose.header.frame_id = 'base_link'
#   pose.pose.position.x = 0.5
#   pose.pose.position.y = 0
#   pose.pose.position.z = 0.4
#   pose.pose.orientation.w = 1
#   error = arm.move_to_pose(pose, **kwargs)
#   if error is not None:
#       rospy.logerr('Pose failed: {}'.format(error))
#   else:
#       rospy.loginfo('Pose succeeded')
#       print "Arm moved in!"


## Move to Shelf

  move_base_pub.publish(pose2)
  teleport(set_rviz, set_gazebo, pose2.pose)

  gripper.open()

  ##### TODO: write code for moving the arm to lace the coke can

  

if __name__ == "__main__":
  main()
