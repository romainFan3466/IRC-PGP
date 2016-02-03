# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget.ui'
#
# Created: Sun Dec 20 15:31:26 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from app.handlers.pgpHandler import PgpHandler
from app.models.message import Message
from app.core.Observer import Observer
import threading
import time

class MessageBox(QtWidgets.QTextEdit):
    keyPressed = QtCore.pyqtSignal()
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Return:
            self.keyPressed.emit()
        else:
            QtWidgets.QTextEdit.keyPressEvent(self, QKeyEvent)


class ChatWidget(QtWidgets.QWidget, Observer):

    def __init__(self, widget, ircHandler, apiHandler):
        QtWidgets.QWidget.__init__(self)
        self.irc = ircHandler
        self.api = apiHandler
        self.pgp = PgpHandler()
        self.setupUi(self)
        self.widgetParent = widget
        self.__signal = True
        self.username = self.irc.getUserName()
        r=self.api.updatePublicKey(self.pgp.getPublicKey())
        print(r)

    def setupUi(self, Widget):
        self.setObjectName("Widget")
        self.resize(871, 672)
        x = (QtWidgets.QApplication.desktop().screen().width() - 871 )/2
        y = (QtWidgets.QApplication.desktop().screen().height()- 672)/2
        self.move(x, y)
        self.usersList = QtWidgets.QListWidget(Widget)
        self.usersList.setGeometry(QtCore.QRect(670, 30, 161, 381))
        self.usersList.setObjectName("usersList")
        item = QtWidgets.QListWidgetItem()
        self.usersList.addItem(item)

        self.messageBox = MessageBox(Widget)
        self.messageBox.setGeometry(QtCore.QRect(30, 480, 621, 151))
        self.messageBox.setObjectName("messageBox")
        self.messageBox.keyPressed.connect(self.sendMessage)

        self.sendButton = QtWidgets.QPushButton(Widget)
        self.sendButton.setGeometry(QtCore.QRect(710, 510, 99, 27))
        self.sendButton.setObjectName("sendButton")
        self.sendButton.clicked.connect(self.sendMessage)

        self.resetButton = QtWidgets.QPushButton(Widget)
        self.resetButton.setGeometry(QtCore.QRect(710, 550, 99, 27))
        self.resetButton.setObjectName("resetButton")
        self.resetButton.clicked.connect(self.reset)

        self.disconnectButton = QtWidgets.QPushButton(Widget)
        self.disconnectButton.setGeometry(QtCore.QRect(710, 590, 99, 27))
        self.disconnectButton.setObjectName("disconnectButton")
        self.disconnectButton.clicked.connect(self.disconnect)

        self.channelMessages = QtWidgets.QTextEdit(Widget)
        self.channelMessages.setGeometry(QtCore.QRect(40, 30, 591, 381))
        self.channelMessages.setObjectName("channelMessages")
        self.channelMessages.setReadOnly(True)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)


    def disconnect(self):
        self.widgetParent.show()
        self.irc.stop()
        self.api.logout()
        self.close()


    def reset(self):
        self.messageBox.clear()


    def retranslateUi(self, Widget):
        Widget.setWindowTitle( "IRC-PGP : Romain's Irc Server")
        __sortingEnabled = self.usersList.isSortingEnabled()
        self.usersList.setSortingEnabled(False)
        item = self.usersList.item(0)
        item.setText( "bots1")
        self.usersList.setSortingEnabled(__sortingEnabled)

        self.sendButton.setText("Send")
        self.resetButton.setText( "Reset")
        self.disconnectButton.setText("Disconnect")


    def sendMessage(self):
        message = self.messageBox.toPlainText()

        if not message == '':
            self.irc.sendMessage(message)
            mess = '<span style="color:green; font-weight: bolder";>' + self.username + "</span>" + " : " + message
            self.appendMessage(mess)
        self.messageBox.clear()


    def appendMessage(self, str):
        self.channelMessages.append(str)
        self.channelMessages.ensureCursorVisible()


    def update(self, buffer):
        if "PRIVMSG" in buffer:
            formatted_message = Message.rawParse(buffer)
            buffer = formatted_message["username"] + " : " + formatted_message["message"]

        if "JOIN" in buffer:
            pass
            # ":romain!root@172.17.0.1 JOIN :#1"

        t = threading.Thread(target=self.appendMessage, args=(buffer,))
        t.start()
        t.join()
        time.sleep(0.07)

    def closeEvent(self, QCloseEvent):
        self.irc.stop()
