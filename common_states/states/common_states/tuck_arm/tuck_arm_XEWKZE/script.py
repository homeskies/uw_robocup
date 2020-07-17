def execute(self, inputs, outputs, gvm):
    fetch = gvm.get_variable("robot")
    arm = fetch[1]
    torso = fetch[5]
    arm.tuck()
    torso.set_height(0)
    return "success"
