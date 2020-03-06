if [ "$RAFCON_LIBRARY_PATH" != *$(rospack find task_storing_groceries)/states/task_storing_groceries* ]; then
export RAFCON_LIBRARY_PATH=$(rospack find task_storing_groceries)/states/task_storing_groceries:$RAFCON_LIBRARY_PATH
fi