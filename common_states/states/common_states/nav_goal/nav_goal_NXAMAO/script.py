import json
from geometry_msgs.msg import PoseStamped
from collections import namedtuple
from rospy_message_converter import json_message_converter

def execute(self, inputs, outputs, gvm):
    fetch = gvm.get_variable("robot")
    base = fetch[0]
    pose_stamped = inputs["pose"]
    self.logger.info(pose_stamped)
    pose_stamped = json_message_converter.convert_json_to_ros_message("geometry_msgs/PoseStamped", pose_stamped)
    try:
        base.navigate_to(pose_stamped.pose.position.x, pose_stamped.pose.position.y, pose_stamped.pose.orientation.w)
        result = base.wait_for_navigation_result()
        self.logger.info(result)
        self.logger.info("Moved to pose " + str(pose_stamped.pose.position) + " successfully")
        return "success"
    except Exception as e:
        self.logger.error(e)
        return "aborted"

if __name__ == "__main__":
    inputs = {"pose": '{\
        "header": {\
            "frame_id": "base_link"\
        },\
        "pose": {\
            "position": {\
                "x": 0.5,\
                "y": 0,\
                "z": 0.4\
            },\
            "orientation": {\
                "w": 1\
            }\
        }\
    }'}
    # import json
    print(json.loads(inputs["pose"]))

    # json.loads('"\\"foo\\bar"')

    #     from io import StringIO
    #     io = StringIO('["streaming API"]')
    #     json.load(io)

    execute(None, inputs, None, None)


