#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
    from PyQt5.uic import loadUi
except ImportError as err:
    raise SystemExit(err)

class AddVnc(QWidget):
    def __init__(self, parent=None):
        super(AddVnc, self).__init__(parent)
        self.parent = parent
        loadUi("addvnc.ui", self)
        # self.initUI()

    def get_host(self):
        # return host address
        return self.le_host.text()

    def get_port(self):
        # return port number
        return self.sb_port.value()

    def get_password(self):
        # return password
        return self.le_password.text()
