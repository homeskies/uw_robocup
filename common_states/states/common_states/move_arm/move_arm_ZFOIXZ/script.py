def execute(self, inputs, outputs, gvm):
    fetch = gvm.get_variable("robot")
    rospy = gvm.get_variable("rospy")
    grasp_cli = fetch[3]
    objs = inputs["objs"]
    coke = objs[0]
    grasps = objs[1]

    if grasp_cli.pick(coke, grasps):
        self.logger.info("grasp succeeded")
        return "success"
    else:
        self.logger.warn("grasp failed")
        grasp_cli.tuck()
        return "aborted"
   