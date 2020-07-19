
def execute(self, inputs, outputs, gvm):
    gripper = gvm.get_variable("robot")[2]
    gripper_state = gripper.get_state()
    # Heuristic: if the grasp failed, we'll be pretty close to all the way closed
    if gripper_state < 0.01:
        return "aborted"
    return "success"
