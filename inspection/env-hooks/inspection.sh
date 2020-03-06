if [ "$RAFCON_LIBRARY_PATH" != *$(rospack find inspection)/states/inspection* ]; then
export RAFCON_LIBRARY_PATH=$(rospack find inspection)/states/inspection:$RAFCON_LIBRARY_PATH
fi