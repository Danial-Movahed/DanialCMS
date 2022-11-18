from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from . import ui_EditCreatePost

class EditCreate(QMainWindow, ui_EditCreatePost.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("DanialCMS blog post editor")
        self.EditCreateSavebtn.clicked.connect(lambda: self.save())
        self.EditCreateCancelbtn.clicked.connect(lambda: self.cancelSave())
        self.show()
        self.status=False
    def save(self):
        self.status=True
        self.close()
    def cancelSave(self):
        self.status=False
        self.close()