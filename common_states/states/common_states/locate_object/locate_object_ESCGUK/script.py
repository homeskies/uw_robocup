
def execute(self, inputs, outputs, gvm):
    fetch = gvm.get_variable("robot")
    rospy = gvm.get_variable("rospy")
    head = fetch[4]
    grasp_cli = fetch[3]
    torso = fetch[5]
    look = inputs["look"]
    head.look_at("map", look["x"], look["y"], look["w"])
    self.logger.info("looked at object")
    self.logger.info("raising torso")
    torso.set_height(.4)
    while not rospy.is_shutdown():
        self.logger.info("Picking object...")
        grasp_cli.updateScene()
        coke, grasps = grasp_cli.getGraspableCube()
        if coke == None:
            self.logger.warn("Perception failed.")
            continue
        else:
            outputs["objs"] = [coke, grasps]
            return "success"
    return "aborted"