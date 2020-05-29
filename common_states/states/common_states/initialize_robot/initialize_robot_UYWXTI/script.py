from fetch_api import Base, Arm, Gripper, GraspingClient, Torso, Head
import knowledge_representation
import rospy
import tf
import traceback


def execute(self, inputs, outputs, gvm):
    # check if the roscore is already running
    try:
        rospy.wait_for_service("/rosout/get_loggers", 5.0)
    except Exception as e:
        self.logger.error("Exception: " + str(e) + str(traceback.format_exc()))
        return -1
    if "node_name" in inputs:
        node_name = inputs["node_name"]
    else:
        # TODO(nickswalker): Pull this from the parent state machine's name...
        node_name = "task"
    if type(node_name).__name__ == "unicode":
        node_name = node_name.encode('ascii', 'ignore')
        # print node_name

    self.logger.info("Creating node: " + node_name)
    try:
        if not gvm.variable_exist("ros_node_initialized") or not gvm.get_variable("ros_node_initialized"):
            gvm.set_variable("ros_node_initialized", True)
            rospy.init_node(node_name, disable_signals=True)

            listener = tf.TransformListener()
            self.logger.info("Creating node: " + str(listener))
            gvm.set_variable("tf_listener", listener, per_reference=True)
            grasp_cli = GraspingClient()
            self.logger.info("tucking arm")
            grasp_cli.tuck()
            torso = Torso()
            self.logger.info("lowering torso")
            torso.set_height(0)

            fetch = (Base(), Arm(), Gripper(), grasp_cli, Head(), torso)

            gvm.set_variable("robot", fetch, per_reference=True)
            gvm.set_variable("rospy", rospy, per_reference = True)
            ltmc = knowledge_representation.get_default_ltmc()
            gvm.set_variable("knowledgebase", ltmc, per_reference=True)
    except Exception as e:
        self.logger.error("Unexpected error:" + str(e) + str(traceback.format_exc()))

    return 0
