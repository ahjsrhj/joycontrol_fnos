#!/bin/bash
service dbus start
echo "Starting bluetoothd"
bluetoothd --noplugin=input > /var/log/bluetoothd.log 2>&1 &
echo "Bluetoothd started"

exec "$@"