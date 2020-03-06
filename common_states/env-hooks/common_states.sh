if [ "$RAFCON_LIBRARY_PATH" != *$(rospack find common_states)/states/common_states* ]; then
    export RAFCON_LIBRARY_PATH=$(rospack find common_states)/states/common_states:$RAFCON_LIBRARY_PATH
fi