from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import ui_BlogPicker
import ui_CreateBlogWizard

class CreateBlogWizard(QMainWindow, ui_CreateBlogWizard.Ui_MainWindow):
    def __init__(self):
        super(CreateBlogWizard, self).__init__()
        self.setupUi(self)
        self.show()
class BlogPicker(QMainWindow, ui_BlogPicker.Ui_MainWindow):
    def __init__(self):
        super(BlogPicker, self).__init__()
        self.setupUi(self)
        self.show()
        self.NewBlogbtn.clicked.connect(lambda: self.startWizard())
        self.Refreshbtn.clicked.connect(lambda: self.refresh())
    def startWizard(self):
       self.wzd = CreateBlogWizard()
       self.wzd.closeEvent = self.refresh
    def refresh(self,e=None):
        print("aa")


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("DanialCMS")
    wnd = BlogPicker()
    app.exec()
