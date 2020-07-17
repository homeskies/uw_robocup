import rospy


def execute(self, inputs, outputs, gvm):
    fetch = gvm.get_variable("robot")
    grasp_cli = gvm.get_variable("grasping_client")
    head = fetch[3]
    torso = fetch[4]
    # Assume we're in front of a surface to scan
    # Tilt head down
    head.pan_tilt(0, 1.0)
    self.logger.info("looked at object")
    self.logger.info("raising torso")
    torso.set_height(.4)

    self.logger.info("Selecting object...")
    grasp_cli.update_scene()
    coke, grasps = grasp_cli.get_graspable_cube()
    if coke is None:
        self.logger.warn("Perception failed.")
    else:
        outputs["objs"] = [coke, grasps]
        return "success"
    return "aborted"
