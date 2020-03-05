import json
from geometry_msgs.msg import PoseStamped
from collections import namedtuple


def execute(self, inputs, outputs, gvm):
    fetch = gvm.get_variable("robot")
    base = fetch[0]
    pose_stamped = json2obj(inputs.get("robot"))
    try:
        base.move_to_pose(pose_stamped)
        return "success"
    except (Exception):
        return "aborted"


def _json_object_hook(d):
    return namedtuple(PoseStamped, d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)
