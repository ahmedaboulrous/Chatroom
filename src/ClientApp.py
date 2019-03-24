import sys
import socket
import threading

from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication


class ClientApp:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        designer_file = QFile("client.ui")
        designer_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(designer_file)
        designer_file.close()
        self.window.pushButton_send_msg.clicked.connect(self.send_msg)
        self.window.pushButton_connect_to_server.clicked.connect(self.connect_to_server)
        self.window.setWindowTitle("Chat Application")
        self.window.lineEdit_host.setText('127.0.0.1')
        self.window.lineEdit_port.setText('1996')
        self.window.lineEdit_alias.setText('Client')
        self.window.pushButton_send_msg.setEnabled(False)
        self.window.lineEdit_msg.setEnabled(False)
        self.window.pushButton_send_msg.setStyleSheet("background-color: rgb(200, 200, 200); color: rgb(0, 0, 0);")

    def connect_to_server(self):
        host = self.window.lineEdit_host.text()
        port = int(self.window.lineEdit_port.text())
        self.client_socket.connect((host, port))
        send_msg_thread = threading.Thread(target=self.receive_msg)
        send_msg_thread.daemon = True
        send_msg_thread.start()
        self.window.pushButton_send_msg.setEnabled(True)
        self.window.lineEdit_msg.setEnabled(True)
        self.window.lineEdit_host.setEnabled(False)
        self.window.lineEdit_port.setEnabled(False)
        self.window.lineEdit_alias.setEnabled(False)
        self.window.pushButton_connect_to_server.setEnabled(False)
        self.window.pushButton_connect_to_server.setStyleSheet("background-color: rgb(200, 200, 200); color: rgb(0, 0, 0);")
        self.window.pushButton_send_msg.setStyleSheet("background-color: rgb(85, 85, 255); color: rgb(0, 0, 0);")

    def receive_msg(self):
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            self.window.plainTextEdit_chatroom.appendPlainText(str(data, 'UTF-8'))

    def send_msg(self):
        alias = self.window.lineEdit_alias.text()
        msg = self.window.lineEdit_msg.text()
        data = alias + ': ' + msg
        self.client_socket.send(bytes(data, 'UTF-8'))

    def show(self):
        self.window.show()


app = QApplication(sys.argv)
window = ClientApp()
window.show()
sys.exit(app.exec_())
