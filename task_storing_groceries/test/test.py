#!/usr/bin/env python
import unittest
from rafcon.core.start import open_state_machine, setup_configuration
import rospkg

# A work around for missing libraries prompting user interaction
# https://github.com/DLR-RM/RAFCON/issues/838
import rafcon.core.interface
from rafcon.core.states.library_state import LibraryState

rafcon.core.interface.show_notice_func = lambda *args, **kwargs: None
rafcon.core.interface.open_folder_func = lambda *args, **kwargs: None

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
        elif isinstance(state, LibraryState):
            # This is a successfully loaded leaf state
            continue
        else:
            # Some other kind of container to recurse on
            missing_list += get_missing_states(state)
    return missing_list


class TestStateMachine(unittest.TestCase):

    def setUp(self):
        self.sm = open_state_machine(rospack.get_path('task_storing_groceries') + "/states/task_storing_groceries/task")

    def test_loads(self):
        self.assertTrue(self.sm)
        self.assertEqual([], get_missing_states(self.sm.root_state))


if __name__ == '__main__':
    import rosunit

    rosunit.unitrun("knowledge_representation", 'test_bare_bones', TestStateMachine)
