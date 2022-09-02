#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import signal
try:
    from PyQt5.QtWidgets import (QApplication)
except ImportError as err:
    raise SystemExit("pip install PyQt5\n %s" % err)

# You HAVE TO reimplement QApplication.event, otherwise it does not work.
# I believe that you need some python callable to catch the signal
# or KeyboardInterrupt exception.
class MyApp(QApplication):
    """wrapper to the QApplication """
    def __init__(self, argv=None):
        super(MyApp, self).__init__(argv)

    def event(self, event_):
        """handle event """
        return QApplication.event(self, event_)

    def signal_handler(self, signal_, frame):
        """signal handler"""
        print('You pressed Ctrl+C!')
        sys.exit(0)

def sig_segv(signum, frame):
    print("segfault: %s" % frame)

from mainwindow import MainWindow

# main
if __name__ == '__main__':
    APP = MyApp(sys.argv)
    # Connect your cleanup function to signal.SIGINT
    signal.signal(signal.SIGINT, APP.signal_handler)
    signal.signal(signal.SIGSEGV, sig_segv)
    # And start a timer to call Application.event repeatedly.
    # You can change the timer parameter as you like.
    APP.startTimer(200)
    # add your code here ...
    main = MainWindow(APP)
    main.show()
    sys.exit(APP.exec_())
