# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect.ui'
#
# Created: Sun Dec 20 13:55:22 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from app.ChatWidget import ChatWidget
from app.handlers.IrcHandler import IRChandler

class ConnectionWidget(QtWidgets.QWidget):

    ircHandler  = None

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.fillData()


    def setupUi(self, Widget):
        self.setObjectName("Form")
        self.resize(749, 586)
        x = (QtWidgets.QApplication.desktop().screen().width() - 749 )/2
        y = (QtWidgets.QApplication.desktop().screen().height()- 586)/2
        self.move(x, y)

        self.serverBox = QtWidgets.QGroupBox(Widget)
        self.serverBox.setGeometry(QtCore.QRect(160, 60, 491, 231))
        self.serverBox.setObjectName("serverBox")

        self.serverLabel = QtWidgets.QLabel(self.serverBox)
        self.serverLabel.setGeometry(QtCore.QRect(50, 50, 111, 17))
        self.serverLabel.setObjectName("serverLabel")

        self.channelLabel = QtWidgets.QLabel(self.serverBox)
        self.channelLabel.setGeometry(QtCore.QRect(50, 100, 91, 17))
        self.channelLabel.setObjectName("channelLabel")

        self.serverPasswordLabel = QtWidgets.QLabel(self.serverBox)
        self.serverPasswordLabel.setGeometry(QtCore.QRect(50, 140, 91, 17))
        self.serverPasswordLabel.setObjectName("serverPasswordLabel")

        self.nicknameLabel = QtWidgets.QLabel(self.serverBox)
        self.nicknameLabel.setGeometry(QtCore.QRect(50, 180, 81, 17))
        self.nicknameLabel.setObjectName("nicknameLabel")

        self.serverText = QtWidgets.QLineEdit(self.serverBox)
        self.serverText.setGeometry(QtCore.QRect(200, 40, 231, 27))
        self.serverText.setObjectName("serverText")

        self.channelText = QtWidgets.QLineEdit(self.serverBox)
        self.channelText.setGeometry(QtCore.QRect(200, 90, 231, 27))
        self.channelText.setObjectName("channelText")

        self.serverPasswordText = QtWidgets.QLineEdit(self.serverBox)
        self.serverPasswordText.setGeometry(QtCore.QRect(200, 130, 231, 27))
        self.serverPasswordText.setObjectName("serverPasswordText")

        self.nicknameText = QtWidgets.QLineEdit(self.serverBox)
        self.nicknameText.setGeometry(QtCore.QRect(200, 180, 231, 27))
        self.nicknameText.setObjectName("nicknameText")

        self.apiBox = QtWidgets.QGroupBox(Widget)
        self.apiBox.setGeometry(QtCore.QRect(180, 300, 460, 181))
        self.apiBox.setObjectName("apiBox")

        self.loginLabel = QtWidgets.QLabel(self.apiBox)
        self.loginLabel.setGeometry(QtCore.QRect(50, 50, 101, 17))
        self.loginLabel.setObjectName("loginLabel")

        self.apiPasswordLabel = QtWidgets.QLabel(self.apiBox)
        self.apiPasswordLabel.setGeometry(QtCore.QRect(50, 100, 121, 17))
        self.apiPasswordLabel.setObjectName("apiPasswordLabel")

        self.loginText = QtWidgets.QLineEdit(self.apiBox)
        self.loginText.setGeometry(QtCore.QRect(130, 40, 231, 27))
        self.loginText.setObjectName("loginText")

        self.apiPasswordText = QtWidgets.QLineEdit(self.apiBox)
        self.apiPasswordText.setGeometry(QtCore.QRect(130, 90, 231, 27))
        self.apiPasswordText.setObjectName("apiPasswordText")

        self.errorLabel = QtWidgets.QLabel(self)
        self.errorLabel.setGeometry(QtCore.QRect(300, 450, 101, 17))
        self.errorLabel.setObjectName("errorLabel")
        self.errorLabel.setStyleSheet('color : red')

        self.connectButton = QtWidgets.QPushButton(self)
        self.connectButton.setGeometry(QtCore.QRect(350, 490, 99, 27))
        self.connectButton.setObjectName("connectButton")
        self.connectButton.clicked.connect(self.connect)

        self.widget2 = None

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)


    def connect(self):
        server = self.serverText.text().split("/")
        host = server[0]
        port = int(server[1])
        password = self.serverPasswordText.text()
        nick = self.nicknameText.text()
        channel = self.channelText.text()
        if self.ircHandler is not None:
            del self.ircHandler

        self.ircHandler = IRChandler(host, nick, port, password=password)

        if self.ircHandler.connect():
            self.ircHandler.join(channel)
            self.widget2 = ChatWidget(self, self.ircHandler)
            self.ircHandler.addObserver(self.widget2)
            self.widget2.show()
            self.hide()
        else :
            self.printError("Connection error")


    def printError(self, str):
        self.errorLabel.setText(str)


    def retranslateUi(self, Widget):
        Widget.setWindowTitle("IRC-PGP Connection")
        self.serverBox.setTitle("IRC Server")
        self.serverLabel.setText("Server host/port")
        self.channelLabel.setText("Channel #")
        self.serverPasswordLabel.setText("Password")
        self.nicknameLabel.setText("Nickname")
        self.apiBox.setTitle("API")
        self.loginLabel.setText("Login")

        self.apiPasswordLabel.setText("Password")
        self.connectButton.setText("Connect")

    def fillData(self):
        self.serverText.setText("127.0.0.1/6666")
        self.nicknameText.setText("bot1")
        self.channelText.setText('#1')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = ConnectionWidget()
    ex.show()
    sys.exit(app.exec_())



