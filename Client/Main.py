from os import stat
from gui import ui_Login,ui_BlogViewer,ShowPost
from gui.main import *

postList = []


class client_thread(threading.Thread):
    def __init__(self,clientsocket,shblgvHndl):
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket
        self.shblgvHndl = shblgvHndl
    def run(self):
        global postList
        status = ""
        while True:
            data = self.clientsocket.recv(4096)
            try:
                data=data.decode()
                if not data == "keep-alive":
                    print(data)
                    if data == "Done":
                        status=""
                        continue
                    status = data
                    if status == "NP":
                        continue
                        # Notification
                    elif status == "FS":
                        continue
                    elif status == "EP" or status == "DP":
                        postList = []
                        continue
            except:
                postList.append(pickle.loads(data))
                self.shblgvHndl.refreshPosts()

class ShowBlogViewer(QMainWindow, ui_BlogViewer.Ui_MainWindow):
    def __init__(self,blogTitle):
        super().__init__()
        self.setupUi(self)
        self.BlogTitle.setText(blogTitle)
        self.setWindowTitle("DanialCMS blog viewer")
        self.ViewPost.clicked.connect(lambda: self.ShowPost())
        self.refreshPosts()
        self.show()
    def refreshPosts(self):
        print("Ran!")
        self.PostList.clear()
        global postList
        for p in postList:
            self.PostList.addItem(p.Title)
    def ShowPost(self):
        if len(self.PostList.selectedItems()) < 1:
            self.dlg = CDialog("Please select a post!", "Error!", True, self)
            self.dlg.exec()
            return
        title = self.PostList.selectedItems()[0].text()
        post = self.findPostByTitle(title)
        self.editCreateWnd = ShowPost.ShowPost(
            title, post.Message, post.Writer)
    def findPostByTitle(self, title):
        global postList
        for post in postList:
            if post.Title == title:
                return post
        return None


class ShowLogin(QMainWindow, ui_Login.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("DanialCMS client login")
        self.LoginContinuebtn.clicked.connect(lambda: self.check())
        self.LoginQuitbtn.clicked.connect(lambda: self.close())
        self.loggedIn = User()
        self.show()

    def check(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.LoginIp.text(), 4523))
            self.s.sendall((self.LoginUsername.text()+" " +
                            blake2s(self.LoginPassword.text().encode()).hexdigest()).encode())
            tmp = self.receive().split(" ")
            if tmp[0] == "Ok":
                self.label_6.setText("Welcome!")
                self.loggedIn.Username = self.LoginUsername.text()
                self.loggedIn.Password = blake2s(
                    self.LoginPassword.text().encode()).hexdigest()
                self.close()
                self.shblgvHndl = ShowBlogViewer(tmp[1])
                self.dataReceive = client_thread(self.s,self.shblgvHndl)
                self.dataReceive.daemon = True
                self.dataReceive.start()
            else:
                self.label_6.setText("Wrong username or password!")
                self.s.close()
        except:
            self.label_6.setText("An error occured! Check ip address.")

    def receive(self):
        data = self.s.recv(4096)
        while data.decode()=="keep-alive":
            data = self.s.recv(4096)
        return data.decode()


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("DanialCMS")
    wnd = ShowLogin()
    app.exec()
