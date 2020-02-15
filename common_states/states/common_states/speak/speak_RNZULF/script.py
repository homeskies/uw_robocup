#! /usr/bin/env python

import rospy
from sound_play.libsoundplay import SoundClient

VOICE = 'voice_kal_diphone'


def execute(self, inputs, outputs, gvm):
    soundhandle = SoundClient(blocking=True)
    count = 0
    self._initialized = False
    while not rospy.is_shutdown() and not soundhandle.actionclient.wait_for_server(rospy.Duration(1.0)):
        rospy.logwarn('Waiting for sound play node...')
        count += 1
        if count > 10:
            rospy.logerr('Could not connect to sound play node!')
            return -1

    soundhandle.say(inputs["text"], VOICE)
    return 0
