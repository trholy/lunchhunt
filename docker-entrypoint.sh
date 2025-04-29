#!/bin/bash
set -e

# Start cron as root (needed to write to /var/run)
service cron start

# Drop privileges and run your app as lunchhunt
exec su -s /bin/bash lunchhunt -c "$*"