#!/bin/sh

if ! [ `which pyrcc5` ]; then
    echo "require pyqt5-dev-tools"
fi
echo pyrcc5 -o qvnc_rc.py qvnc.qrc
pyrcc5 -o qvnc_rc.py qvnc.qrc
