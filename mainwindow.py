#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QTabBar,
                                 QLabel, QFrame)
    from PyQt5.QtGui import (QKeyEvent, QIcon)
    from PyQt5.QtCore import (Qt)
    from PyQt5.uic import loadUi
except ImportError as err:
    raise SystemExit("pip install PyQt5\n %s" % err)

import logging
logging.basicConfig(
    format="[%(name)s] %(levelname)s: %(message)s", level=logging.DEBUG
)
# from qvncwidget.qvncwidget import QVNCWidget
from mdisubvnc import MdiSubVnc
from addvnc import AddVnc

import qvnc_rc

class MainWindow(QMainWindow):
    log = logging.getLogger("MainWindow")
    def __init__(self, app: QApplication):
        super(MainWindow, self).__init__()
        self.app = app
        self.initUI()
        self.resize(1024, 768)
        self.center()
        # self.subwins =[]
        
        # vnc clients
        self.actionConnect.triggered.connect(self.newvnc)
        self.actionDisconnect.triggered.connect(self.on_Disconnect)
        self.actionTiled.triggered.connect(self.on_Tiled)
        self.actionCascade.triggered.connect(self.on_Cascade)
        self.actionNext.triggered.connect(self.on_Next)
        self.actionPrevious.triggered.connect(self.on_Previous)
        self.setWindowIcon(QIcon(":/images/qvnc"))

        self.toolBar.addAction(self.actionConnect)
        self.initStatusBar()

    def initUI(self):
        self.setWindowTitle("QVNCWidget")
        loadUi("mainwindow.ui", self)
        # toolbar
        self.w_vnc = AddVnc(self.toolBar)
        self.toolBar.addWidget(self.w_vnc)
        self.mdiArea.setTabShape(QTabWidget.Triangular)
        child = self.mdiArea.findChild(QTabBar)
        child.setExpanding(False)

    def initStatusBar(self):
        stat = QLabel("test", self.statusbar)
        stat.setAlignment(Qt.AlignRight)
        stat.setFrameShape(QFrame.Panel)
        stat.setFrameShadow(QFrame.Sunken)
        self.statusbar.insertPermanentWidget(0,stat)
        self.statusbar.showMessage("testing...")

    def newvnc(self):
        sub = MdiSubVnc(clipboard=self.app.clipboard(), parent=self)
        sub.new(self.w_vnc.get_host(), self.w_vnc.get_password(), self.w_vnc.get_port())
        self.mdiArea.addSubWindow(sub)
        # self.menuWindow.  //add menu item
        sub.showMaximized()

    def on_Disconnect(self):
        subwin = self.mdiArea.activeSubWindow()
        subwin.disconnect()

    def keyPressEvent(self, ev: QKeyEvent):
        #print(ev.nativeScanCode(), ev.text(), ord(ev.text()), ev.key())
        subwin = self.mdiArea.activeSubWindow()
        if subwin:
            subwin.vnc.onKeyPress.emit(ev)
        return super().keyPressEvent(ev)

    def keyReleaseEvent(self, ev: QKeyEvent):
        #print(ev.nativeScanCode(), ev.text(), ord(ev.text()), ev.key())
        subwin = self.mdiArea.activeSubWindow()
        if subwin:
            subwin.vnc.onKeyRelease.emit(ev)
        return super().keyReleaseEvent(ev)

    def center(self):
        qr = self.frameGeometry()
        cp = self.app.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_Cascade(self):
        self.mdiArea.cascadeSubWindows()

    def on_Tiled(self):
        self.mdiArea.tileSubWindows()
    
    def on_Next(self):
        self.mdiArea.activateNextSubWindow()

    def on_Previous(self):
        self.mdiArea.activatePreviousSubWindow()