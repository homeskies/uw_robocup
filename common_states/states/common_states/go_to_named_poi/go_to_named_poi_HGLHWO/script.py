import rospy


def execute(self, inputs, outputs, gvm):
    base, _ = gvm.get_variable("robot")
    ltmc = gvm.get_variable("knowledgebase")
    map = ltmc.get_map("arena")
    pose = map.get_pose(inputs["name"])
    base.navigate_to(pose)
    result = base.wait_for_navigation_result()
    self.loginfo(result)
    return "success"
