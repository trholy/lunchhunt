#!/bin/bash
set -e

# Start cron daemon in the background
cron

# Launch the app as lunchhunt
exec su -s /bin/bash lunchhunt -c "lunchhunt-web"