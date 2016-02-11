from PyQt5 import QtCore, QtWidgets
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

    keys = {"public" : "", "private" : ""}
    api = None
    irc = None
    widgetParent = None
    username=""

    def __init__(self, widget, ircHandler, apiHandler):
        QtWidgets.QWidget.__init__(self)
        self.api = apiHandler
        self.irc = ircHandler
        self.setupUi(self)
        self.widgetParent = widget
        self.username = self.irc.getUserName()
        self.keys = PgpHandler.generateNewPairs()
        self.api.updatePublicKey(PgpHandler.exportKey(self.keys["public"]))

    def setupUi(self, Widget):
        self.setObjectName("Widget")
        self.resize(871, 672)
        x = (QtWidgets.QApplication.desktop().screen().width() - 871 )/2
        y = (QtWidgets.QApplication.desktop().screen().height()- 672)/2
        self.move(x, y)
        self.usersList = QtWidgets.QListWidget(Widget)
        self.usersList.setGeometry(QtCore.QRect(670, 30, 161, 381))
        self.usersList.setObjectName("usersList")

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
        Widget.setWindowTitle( "IRC-PGP : Romain's Irc Server - " + self.username)
        self.sendButton.setText("Send")
        self.resetButton.setText( "Reset")
        self.disconnectButton.setText("Disconnect")


    def sendMessage(self):
        message = self.messageBox.toPlainText()

        if not message == '':
            keys = self.api.getAllPublicKeys()
            for key in keys:
                m = Message(message,key["publicKey"])
                me = m.getFinal(key["username"])
                print(me)
                self.irc.sendMessage(me)
            mess = '<span style="color:green; font-weight: bolder";>' + self.username + "</span>" + " : " + message
            self.appendMessage(mess)
            self.messageBox.clear()




    def appendMessage(self, str):
        self.channelMessages.append(str)
        self.channelMessages.ensureCursorVisible()



    def updateNames(self, buffer):
        names = Message.exportNames(buffer, self.irc.getNamePattern())

        __sortingEnabled = self.usersList.isSortingEnabled()
        self.usersList.setSortingEnabled(False)
        self.usersList.clear()
        for name in names:
            item = QtWidgets.QListWidgetItem()
            txt = '@'+name if name == self.username else name
            item.setText(txt)
            self.usersList.addItem(item)
        self.usersList.setSortingEnabled(__sortingEnabled)


    def update(self, buffer):

        if "PRIVMSG" in buffer:

            content_message = Message.rawParse(buffer)
            decoded = Message.decode(content_message["message"])

            if "to" in decoded and decoded["to"] == self.username:
                decoded_buffer = Message.rawParse(buffer)
                message = Message.decrypt(decoded_buffer["message"],self.keys["private"])
                buffer = decoded_buffer["username"] + " : " + message.getPlainText()
                t = threading.Thread(target=self.appendMessage, args=(buffer,))
                t.start()
                t.join()
        else:
            t = threading.Thread(target=self.appendMessage, args=(buffer,))
            t.start()
            t.join()

    def closeEvent(self, QCloseEvent):
        self.irc.stop()
