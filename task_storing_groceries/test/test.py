#!/usr/bin/env python
import sys
import unittest
from rafcon.core.start import open_state_machine, setup_configuration
import rospkg
import os

setup_configuration(None)
rospack = rospkg.RosPack()


def get_missing_states(sm):
    """
    Finds the IDs of any states that failed to load
    :param sm: the state machine to recursively search for missing states
    :return: a list of IDs of missing states
    """
    missing_list = []
    for id, state in sm.states.items():
        if state.name == "LIBRARY NOT FOUND DUMMY STATE":
            missing_list.append(id)
        else:
            missing_list += get_missing_states(state)
    return missing_list


class TestStateMachine(unittest.TestCase):

    def setUp(self):
        self.sm = open_state_machine(rospack.get_path('task_storing_groceries') + "/states/task_storing_groceries/task")

    def testLoads(self):
        self.assertTrue(self.sm)
        self.assertEqual(0, len(get_missing_states(self.sm.root_state)))


if __name__ == '__main__':
    import rosunit
    rosunit.unitrun("knowledge_representation", 'test_bare_bones', TestStateMachine)
