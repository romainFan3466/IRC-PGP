# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget.ui'
#
# Created: Sun Dec 20 15:31:26 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from app.handlers.IrcHandler import IRChandler
import threading
import time

class ChatWidget(QtWidgets.QWidget):
    buffer = None
    __signal = False

    def __init__(self, widget, ircHandler):
        QtWidgets.QWidget.__init__(self)
        self.irc = ircHandler
        self.setupUi(self)
        self.widgetParent = widget
        self.buffer = threading.Thread(target=self.runBuffer)
        self.__signal = True
        self.buffer.start()




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

        self.messageBox = QtWidgets.QTextEdit(Widget)
        self.messageBox.setGeometry(QtCore.QRect(30, 480, 621, 151))
        self.messageBox.setObjectName("messageBox")

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

        self.channelMessages.append("<span>Hello</span></br>")
        self.channelMessages.append("<span>Romain</span></br>")
        self.channelMessages.append("<span>c moi </span></br>")

    def sendMessage(self):
        message = self.messageBox.toPlainText()
        self.irc.sendMessage(message)
        self.messageBox.clear()

    def runBuffer(self):
        while self.__signal :
            buf = self.irc.getBuffer()
            old_buf = self.channelMessages.toPlainText()
            if not buf == old_buf:
                self.channelMessages.append(buf)
            time.sleep(1)

    def closeEvent(self, QCloseEvent):
        if self.buffer.isAlive():
            self.__signal = False

        self.irc.stop()
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     ex = ChatWidget()
#     ex.show()
#     sys.exit(app.exec_())
