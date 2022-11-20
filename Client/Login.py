from ast import expr_context
from gui import ui_Login
from gui.main import *


class ShowPost(QMainWindow, ui_Login.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("DanialCMS client login")
        self.LoginContinuebtn.clicked.connect(lambda: self.check())
        self.LoginQuitbtn.clicked.connect(lambda: self.close())
        self.show()

    def check(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.LoginIp.text(), 4411))
            self.s.sendall((self.LoginUsername.text()+" " +
                        blake2s(self.LoginPassword.text().encode()).hexdigest()).encode())
            if self.receive() == "Ok":
                self.label_6.setText("Welcome!")
                pass
            else:
                self.label_6.setText("Wrong username or password!")
                self.s.close()
        except:
            self.label_6.setText("An error occured! Check ip address.")
    def receive(self):
        data = self.s.recv(4096)
        while data.decode().replace("keep-alive","") == "":
            data = self.s.recv(4096)
        return data.decode().replace("keep-alive","")


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("DanialCMS")
    wnd = ShowPost()
    app.exec()
