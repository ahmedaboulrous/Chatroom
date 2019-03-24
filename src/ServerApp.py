import socket
import sys
import threading

from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication


class ServerApp:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_connections = []

    def __init__(self):
        designer_file = QFile("server.ui")
        designer_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(designer_file)
        designer_file.close()
        self.window.setWindowTitle("Server Application")
        self.window.lineEdit_host.setText('127.0.0.1')
        self.window.lineEdit_port.setText('1996')
        self.window.pushButton_start_server.clicked.connect(self.start_server)

    def start_server(self):
        host = self.window.lineEdit_host.text()
        port = self.window.lineEdit_port.text()
        self.server_socket.bind((host, int(port)))
        self.server_socket.listen(5)
        while True:
            conn, addr = self.server_socket.accept()
            conn_thread = threading.Thread(target=self.handler, args=(conn, addr))
            conn_thread.daemon = True
            conn_thread.start()
            print(str(addr[0]) + ' : ' + str(addr[1]) + ' Connected')
            self.client_connections.append(conn)

    def handler(self, conn, addr):
        while True:
            data = conn.recv(1024)
            for c in self.client_connections:
                c.send(bytes(data))
            if not data:
                print(str(addr[0]) + ' : ' + str(addr[1]) + ' Disconnected')
                self.client_connections.remove(conn)
                conn.close()
                break

    def show(self):
        self.window.show()


app = QApplication(sys.argv)
window = ServerApp()
window.show()
sys.exit(app.exec_())
