def execute(self, inputs, outputs, gvm):
    grasp_cli = gvm.get_variable("grasp_client")
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
