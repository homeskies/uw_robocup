cmake_minimum_required(VERSION 2.8.3)
project(common_states)

find_package(catkin REQUIRED
)


catkin_python_setup()


catkin_package(
)


catkin_add_env_hooks(${PROJECT_NAME} SHELLS sh DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/env-hooks)