#!/bin/bash

# Fast API based inference server
python ./backend/inference_server.py &
# Streamlit front
streamlit run ./front/eurygaster_app.py &
# Wait for any process to exit
wait -n
# Exit with status of process that exited first
exit $?