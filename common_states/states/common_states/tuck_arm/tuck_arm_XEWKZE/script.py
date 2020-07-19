def execute(self, inputs, outputs, gvm):
    fetch = gvm.get_variable("robot")
    arm = fetch[1]
    arm.tuck()
    return "success"
