from .main import *
from . import ui_ShowPost

class ShowPost(QMainWindow, ui_ShowPost.Ui_MainWindow):
    def __init__(self,title,postmessage,writer,socketPost):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("DanialCMS blog post viewer")
        self.ShowPostPostTitle.setText(title)
        self.ShowPostPostMessage.setText(postmessage)
        self.ShowPostWriter.setText("Written by: "+writer+"\tRead by: "+str(socketPost))
        self.show()