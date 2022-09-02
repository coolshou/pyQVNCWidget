#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtCore import (pyqtSlot)
    from PyQt5.QtWidgets import QMdiSubWindow
except ImportError as err:
    raise SystemExit("%s" % err)

from qvncwidget.qvncwidget import QVNCWidget

class MdiSubVnc(QMdiSubWindow):
    
    def __init__(self, clipboard, parent=None, flags = Qt.WindowFlags()):
        super(MdiSubVnc, self).__init__(parent, flags)
        self.parent = parent
        self.setSystemMenu(None)  # default system menu have close button, which need extra code to control close event!!

        self.vnc = None
        self.clipboard =clipboard

        self.host=""
        self.port=5900
        self.password=""

    def new(self, host, password="12345678", port=5900):
        self.host=host
        self.port=port
        self.password=password

        self.setWindowTitle(host)
        self.vnc = QVNCWidget(host=host, port=port, password=password,
            mouseTracking=True, parent=self.parent)
        # why?? following code cann not work!!
        # self.vnc.onErrorConnect.connect(self._onErrorConnect)
        # self.vnc.onUpdateClipboard.connect(self.on_update_clipboard)
        # self.setCentralWidget(self.vnc)
        self.setWidget(self.vnc)
        self.vnc.onInitialResize.connect(self.parent.resize)
        self.vnc.start()

    def disconnect(self):
        if self.vnc:
            self.vnc.stop()

    @pyqtSlot(str)
    def on_update_clipboard(self, newText):
        self.clipboard.setText(newText)
    
    @pyqtSlot(int, str)
    def _onErrorConnect(self, eno, err):
        print("[%s]%s" % (eno, err))