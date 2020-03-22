def execute(self, inputs, outputs, gvm):
    base, _ = gvm.get_variable("robot")
    ltmc = gvm.get_variable("knowledgebase")
    map = ltmc.get_map("arena")
    pose = map.get_pose(inputs["poi_name"])
    if not pose:
        self.logger.error("No pose named {}".format(inputs["poi_name"]))
        return "aborted"
    base.navigate_to(pose.x, pose.y, pose.theta)
    self.logger.info("Moving to {} {}".format(pose.x, pose.y))
    result = base.wait_for_navigation_result()
    self.logger.info(result)
    return "success"
