states_path="$(rospack find task_storing_groceries)/states/task_storing_groceries"
# Add to library path if not already present
echo "$RAFCON_LIBRARY_PATH" | grep -q "$states_path" \
|| export RAFCON_LIBRARY_PATH="$states_path:$RAFCON_LIBRARY_PATH"