"""
Configure joints so the robot can safely navigate.
"""


def execute(self, inputs, outputs, gvm):
    fetch = gvm.get_variable("robot")
    arm = fetch[1]
    torso = fetch[4]
    arm.tuck()
    torso.set_height(0)
    return "success"
