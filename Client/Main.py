from os import stat
from gui import ui_IpSelector, ui_BlogPicker, Login, BlogViewer
from gui.main import *

blogList = []
ifLoggingIn = False

class client_thread(threading.Thread):
    def __init__(self, clientsocket, blgPkrHndl):
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket
        self.blgPkrHndl = blgPkrHndl

    def run(self):
        global blogList
        status = ""
        while True:
            if not ifLoggingIn:
                data = self.clientsocket.recv(4096)
                try:
                    data = data.decode()
                    if not data == "keep-alive":
                        print(data)
                        if data == "Done":
                            status = ""
                            continue
                        status = data
                        if status == "FS" or status == "NB" or status == "FSP" or status == "NP":
                            continue
                        elif status == "DB":
                            blogList = []
                            continue
                        elif status.split(" ")[0] == "DP" or status.split(" ")[0] == "EP":
                            for b in blogList:
                                if b.UserDB == status.split(" ")[1]:
                                    if b.WndHndl != None:
                                        b.WndHndl.postList=[]
                                        b.WndHndl.refreshPosts()
                except:
                    tmp = pickle.loads(data)
                    print(type(tmp))
                    if type(tmp)==Blogs:
                        blogList.append(tmp)
                        self.blgPkrHndl.refreshBlogs()
                    else:
                        for b in blogList:
                            if tmp.BlogUserDB == b.UserDB:
                                if status == "NP":
                                    if b.WndHndl != None:
                                        if tmp.isPrivate and not b.WndHndl.username in tmp.WhoCanRead:
                                            break
                                        b.WndHndl.postList.append(tmp)
                                        b.WndHndl.refreshPosts()
                                    if not tmp.isPrivate:
                                        self.blgPkrHndl.checkNotif(tmp,b)
                                elif b.WndHndl != None:
                                    if tmp.isPrivate and not b.WndHndl.username in tmp.WhoCanRead:
                                            break
                                    b.WndHndl.postList.append(tmp)
                                    b.WndHndl.refreshPosts()
                                break


class ShowBlogPicker(QMainWindow, ui_BlogPicker.Ui_MainWindow):
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
        global ifLoggingIn
        ifLoggingIn=True
        self.loginBlgWnd = Login.Login(blog,self.socket)
        self.loginBlgWnd.closeEvent = self.OpenBlog

    def OpenBlog(self,e):
        global blogList, ifLoggingIn
        ifLoggingIn=False
        if self.loginBlgWnd.status:
            for b in blogList:
                if b == self.loginBlgWnd.blog:
                    b.WndHndl = BlogViewer.ShowBlogViewer(b,self.socket,self.loginBlgWnd.LoginUsername.text())
                    b.WndHndl.closeEvent = lambda event: self.CloseBlog(b)
                    break
            print("masalan post gereft!")

    def CloseBlog(self,blog):
        blog.WndHndl = None

    def SubToBlog(self):
        if len(self.BlogList.selectedItems()) < 1:
            self.dlg = CDialog("Please select a blog!", "Error!", True, self)
            self.dlg.exec()
            return
        title = self.BlogList.selectedItems()[0].text()
        blog = self.findBlogByTitle(title)
        blog.isSub = not blog.isSub
        self.refreshBlogs()

    def checkNotif(self,p,b):
        blog = self.findBlogByTitle(b.UserDB,False)
        if blog.isSub:
            if platform.system() == "Linux":
                subprocess.Popen(["notify-send",b.Title,p.Title])

    def findBlogByTitle(self, title, mode=True):
        global blogList
        for blog in blogList:
            if mode:
                if blog.Title+", "+blog.UserDB+", "+str(blog.isSub) == title:
                    return blog
            else:
                if blog.UserDB == title:
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
