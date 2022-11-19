from gui import ui_NewUser
from .main import *
from . import ui_NewUser

class NewUser(QMainWindow, ui_NewUser.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("DanialCMS user creation wizard")
        self.NewUserContinuebtn.clicked.connect(lambda: self.save())
        self.NewUserCancelbtn.clicked.connect(lambda: self.cancelSave())
        self.show()
        self.status=False
    def save(self):
        self.status=True
        self.close()
    def cancelSave(self):
        self.status=False
        self.close()