# ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# No module in this package, we just need this
# so roslint can actually attach to the catkin python hooks
setup_args = generate_distutils_setup(
    packages=[],
    package_dir={})

setup(**setup_args)
