#! /usr/bin/env python

import rospy
import fetch_api
from geometry_msgs.msg import PoseStamped
from moveit_msgs.msg import OrientationConstraint
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

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

  # torso = fetch_api.Torso()
  
  fetch_gripper = fetch_api.Gripper()
  move_base_client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
  move_base_client.wait_for_server()
  rospy.sleep(0.5)
  print "Ready to move"

  ########## TODO: Uncomment this
  # shutdown handler
  # def shutdown():
  #   arm.cancel_all_goals()
  # rospy.on_shutdown(shutdown)


  # move base to the position near coke can
  goal = MoveBaseGoal()
  goal.target_pose.header.frame_id = "map"
  goal.target_pose.header.stamp = rospy.Time.now()
  goal.target_pose.pose.position.x = 4.50320185696
  goal.target_pose.pose.position.y = -4.2
  goal.target_pose.pose.orientation.z = -0.554336505677
  goal.target_pose.pose.orientation.w = 0.832292639926

  move_base_client.send_goal(goal)
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

  ##### TODO: write code for moving the arm to pick up the coke can
  pose = PoseStamped()
  pose.header.frame_id = 'base_link'
  pose.pose.position.x = 0.8
  pose.pose.position.y = 0
  pose.pose.position.z = 0.75
  pose.pose.orientation.w = 1
  # arm.move_to_pose(pose)
  # print "arm moved"

### MOVE ARM TO 
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
      print "Arm moved!"


  pose = PoseStamped()
  pose.header.frame_id = 'base_link'
  pose.pose.position.x = 0.5
  pose.pose.position.y = 0
  pose.pose.position.z = 0.4
  pose.pose.orientation.w = 1
  error = arm.move_to_pose(pose, **kwargs)
  if error is not None:
      rospy.logerr('Pose failed: {}'.format(error))
  else:
      rospy.loginfo('Pose succeeded')
      print "Arm moved!"

#TODO:uncomment
  # move base to the position near the shelf
  goal = MoveBaseGoal()
  goal.target_pose.header.frame_id = "map"
  goal.target_pose.header.stamp = rospy.Time.now()
  goal.target_pose.pose.position.x = 4.50320185696
  goal.target_pose.pose.position.y = -4.2
  goal.target_pose.pose.orientation.z = -0.554336505677
  goal.target_pose.pose.orientation.w = 0.832292639926

  move_base_client.send_goal(goal)
  wait = move_base_client.wait_for_result()
  if not wait:
      rospy.logerr("Action server not available!")
      rospy.signal_shutdown("Action server not available!")
  else:
      # move_base_client.get_result()
      print "Ready to place the coke can!"

  ##### TODO: write code for moving the arm to lace the coke can

  

if __name__ == "__main__":
  main()
