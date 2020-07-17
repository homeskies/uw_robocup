import rospy


def execute(self, inputs, outputs, gvm):
    base = gvm.get_variable("robot")[0]
    simulated = gvm.get_variable("simulation")
    self.logger.info(simulated)
    map = gvm.get_variable("map")
    pose = map.get_pose(inputs["pose_name"])
    if not pose:
        self.logger.error("No pose named {}".format(inputs["pose_name"]))
        return "aborted"
    if simulated:
        from gazebo_msgs.srv import SetModelState, SetModelStateRequest
        from tf.transformations import quaternion_from_euler
        set_model_state = rospy.ServiceProxy("/gazebo/set_model_state", SetModelState)
        data = SetModelStateRequest()
        data.model_state.model_name = "fetch"
        data.model_state.pose.position.x = pose.x
        data.model_state.pose.position.y = pose.y
        data.model_state.pose.position.y = pose.y
        quat = quaternion_from_euler(0, 0, pose.theta)
        data.model_state.pose.orientation.x = quat[0]
        data.model_state.pose.orientation.y = quat[1]
        data.model_state.pose.orientation.z = quat[2]
        data.model_state.pose.orientation.w = quat[3]
        set_model_state.call(data)
        # TODO(nickswalker): Send updated pose to /initialpose so AMCL is corrected
        return "success"
    else:
        base.navigate_to(pose.x, pose.y, pose.theta)
        self.logger.info("Moving to x={} y={} t={}".format(pose.x, pose.y, pose.theta))
        result = base.wait_for_navigation_result()
        self.logger.info(result)
    # TODO(nickswalker): report failure if failed to reach goal
    return "success"
