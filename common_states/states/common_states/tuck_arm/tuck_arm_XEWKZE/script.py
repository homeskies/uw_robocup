def execute(self, inputs, outputs, gvm):
    fetch = gvm.get_variable("robot")
    rospy = gvm.get_variable("rospy")
    grasp_cli = fetch[3]
    torso = fetch[5]
    grasp_cli.tuck()
    torso.set_height(0)
    return "success"
   