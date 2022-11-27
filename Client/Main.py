from os import stat
from gui import ui_IpSelector, ui_BlogViewer, ShowPost
from gui.main import *

blogList = []


class client_thread(threading.Thread):
    def __init__(self, clientsocket, blgPkrHndl):
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket
        self.blgPkrHndl = blgPkrHndl

    def run(self):
        global blogList
        status = ""
        while True:
            data = self.clientsocket.recv(4096)
            try:
                data = data.decode()
                if not data == "keep-alive":
                    print(data)
                    if data == "Done":
                        status = ""
                        continue
                    status = data
                    if status == "FS" or status == "NB":
                        continue
                    elif status == "DB":
                        blogList = []
                        continue
            except:
                blogList.append(pickle.loads(data))
                self.blgPkrHndl.refreshBlogs()


class ShowBlogPicker(QMainWindow, ui_BlogViewer.Ui_MainWindow):
    def __init__(self, socket):
        super().__init__()
        self.setupUi(self)
        self.socket = socket
        self.setWindowTitle("DanialCMS blog picker")
        self.ViewBlog.clicked.connect(lambda: self.ShowBlog())
        self.Subscribe.clicked.connect(lambda: self.SubToBlog())
        self.refreshBlogs()
        self.show()

    def refreshBlogs(self):
        print("Ran!")
        self.BlogList.clear()
        global blogList
        for b in blogList:
            self.BlogList.addItem(b.Title+", "+b.UserDB+", "+str(b.isSub))

    def ShowBlog(self):
        if len(self.BlogList.selectedItems()) < 1:
            self.dlg = CDialog("Please select a blog!", "Error!", True, self)
            self.dlg.exec()
            return
        title = self.BlogList.selectedItems()[0].text()
        blog = self.findBlogByTitle(title)
        self.editCreateWnd = ShowPost.ShowPost(
            title, blog.Title)

    def SubToBlog(self):
        if len(self.BlogList.selectedItems()) < 1:
            self.dlg = CDialog("Please select a blog!", "Error!", True, self)
            self.dlg.exec()
            return
        title = self.BlogList.selectedItems()[0].text()
        blog = self.findBlogByTitle(title)
        blog.isSub = not blog.isSub
        self.refreshBlogs()

    def findBlogByTitle(self, title):
        global blogList
        for blog in blogList:
            if blog.Title+", "+blog.UserDB+", "+str(blog.isSub) == title:
                return blog
        return None


class ShowIpSelector(QMainWindow, ui_IpSelector.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("DanialCMS ip selector")
        self.IpSelectorContinuebtn.clicked.connect(lambda: self.check())
        self.IpSelectorQuitbtn.clicked.connect(lambda: self.close())
        self.show()

    def check(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.IpSelectorIp.text(), 4524))
            self.label_6.setText("Welcome!")
            self.close()
            self.blgPkrHndl = ShowBlogPicker(self.s)
            self.dataReceive = client_thread(self.s, self.blgPkrHndl)
            self.dataReceive.daemon = True
            self.dataReceive.start()
        except:
            self.label_6.setText("An error occured! Check ip address.")


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("DanialCMS")
    wnd = ShowIpSelector()
    app.exec()
