from .main import *
from . import ui_Login

class Login(QMainWindow, ui_Login.Ui_MainWindow):
    def __init__(self,blog,sock):
        super().__init__()
        self.setupUi(self)
        self.blog = blog
        self.sock = sock
        self.LoginContinuebtn.clicked.connect(lambda: self.check())
        self.LoginQuitbtn.clicked.connect(lambda: self.close())
        self.status = False
        self.show()
    def check(self):
        tmp = BlogLoginObj()
        tmp.UserDB = self.blog.UserDB
        tmp.Password = blake2s(self.LoginPassword.text().encode()).hexdigest()
        tmp.Title = self.blog.Title
        tmp.Username = self.LoginUsername.text()
        self.sock.sendall(pickle.dumps(tmp))
        if self.receive() == "Ok":
            self.status = True
            self.close()
        else:
            self.label_6.setText("Wrong username or password!")
    def receive(self):
        data = self.sock.recv(4096)
        while data.decode().replace("keep-alive","") == "":
            data = self.sock.recv(4096)
        return data.decode().replace("keep-alive","")