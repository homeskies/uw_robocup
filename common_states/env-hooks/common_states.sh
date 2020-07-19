states_path="$(rospack find common_states)/states/common_states"
# Add to library path if not already present
echo "$RAFCON_LIBRARY_PATH" | grep -q "$states_path" \
|| export RAFCON_LIBRARY_PATH="$states_path:$RAFCON_LIBRARY_PATH"
