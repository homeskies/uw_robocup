cmake_minimum_required(VERSION 2.8.3)
project(task_storing_groceries)

find_package(catkin REQUIRED COMPONENTS
roslint
)

catkin_package(
)

catkin_python_setup()

catkin_add_env_hooks(${PROJECT_NAME} SHELLS sh DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/env-hooks)

# Lint Python modules for PEP8 compatibility
set(ROSLINT_PYTHON_OPTS "--max-line-length=120")

file(GLOB_RECURSE ${PROJECT_NAME}_PY_SRC
        RELATIVE ${PROJECT_SOURCE_DIR} src/${PROJECT_NAME}/**/*.py)
roslint_python(${${PROJECT_NAME}_PY_SRC})

file(GLOB_RECURSE ${PROJECT_NAME}_PY_STATES
        RELATIVE ${PROJECT_SOURCE_DIR} states/${PROJECT_NAME}/**/*.py)
roslint_python(${${PROJECT_NAME}_PY_STATES})

### TEST TARGETS
if(CATKIN_ENABLE_TESTING)
    # catkin_add_nosetests(test/test.py)
endif()