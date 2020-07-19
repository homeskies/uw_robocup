def execute(self, inputs, outputs, gvm):
    grasp_cli = gvm.get_variable("grasp_client")
    arm = gvm.get_variable("robot")[1]
    if "objs" not in inputs:
        self.logger.error("No objects provided")
        return "aborted"
    objs = inputs["objs"]
    coke = objs[0]
    grasps = objs[1]

    if grasp_cli.pick(coke, grasps):
        self.logger.info("grasp succeeded")
        return "success"
    else:
        self.logger.warn("grasp failed")
        arm.tuck()
        return "aborted"
