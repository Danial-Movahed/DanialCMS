from .main import *
from . import ui_ShowPost

class ShowPost(QMainWindow, ui_ShowPost.Ui_MainWindow):
    def __init__(self,title,postmessage):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("DanialCMS blog post viewer")
        self.ShowPostPostTitle.setText(title)
        self.ShowPostPostMessage.setText(postmessage)
        self.show()