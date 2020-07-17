from fetch_api import Base, Arm, Gripper, Torso, Head
import knowledge_representation
import rospy
import tf
import traceback


def load_robot_objects(logger, inputs, gvm):
    # We can reload all of the robot API objects though
    listener = tf.TransformListener()
    gvm.set_variable("tf_listener", listener, per_reference=True)
    arm = Arm()
    logger.info("tucking arm")
    arm.tuck()
    torso = Torso()
    logger.info("lowering torso")
    torso.set_height(0)
    logger.info("done")
    if inputs["use_manipulation"]:
        from uw_manipulation import GraspingClient
        grasping_client = GraspingClient()
    else:
        grasping_client = None
    fetch = (Base(), arm, Gripper(), Head(), torso)
    gvm.set_variable("robot", fetch, per_reference=True)
    gvm.set_variable("grasp_client", grasping_client, per_reference=True)
    ltmc = knowledge_representation.get_default_ltmc()
    gvm.set_variable("knowledgebase", ltmc, per_reference=True)
    map = ltmc.get_map(inputs["map_name"])
    if map is None:
        raise RuntimeError("Couldn't load map {}".format(inputs["map_name"]))
    # TODO(nickswalker): Expose this as a parameter
    gvm.set_variable("map", ltmc.get_map("map"), per_reference=True)

    # For now, this single switch serves to signal any special Gazebo-specific hacks
    # or accelerations across other states.
    in_simulation = rospy.get_param("use_sim_time")
    gvm.set_variable("simulation", in_simulation)
    if in_simulation:
        logger.info("Running with simulation flag")


def execute(self, inputs, outputs, gvm):
    if rospy.is_shutdown():
        # Reinitializing a ROS node isn't allowed. If the node gets shutdown and you're
        # running this state machine within the RAFCON GUI, you'll need to restart the GUI
        self.logger.error("rospy is shutdown")
        return -1

    # check if the roscore is already running
    try:
        rospy.wait_for_service("/rosout/get_loggers", 5.0)
    except Exception as e:
        self.logger.error("Exception: " + str(e) + str(traceback.format_exc()))
        return -1
    if "node_name" in inputs and inputs["node_name"]:
        self.logger.info(list(inputs.keys))
        node_name = inputs["node_name"]
    else:
        # TODO(nickswalker): Pull this from the parent state machine's name...
        node_name = "task"
    if type(node_name).__name__ == "unicode":
        node_name = node_name.encode('ascii', 'ignore')
        # print node_name

    self.logger.info("Creating node: " + node_name)
    try:
        # This is a once per process thing. If you need a fresh node, the process has to relaunch
        if not gvm.variable_exist("ros_node_initialized") or not gvm.get_variable("ros_node_initialized"):
            gvm.set_variable("ros_node_initialized", True)
            rospy.init_node(node_name, disable_signals=True)

        load_robot_objects(self.logger, inputs, gvm)
    except Exception as e:
        self.logger.error("Unexpected error:" + str(e) + str(traceback.format_exc()))

    return 0
