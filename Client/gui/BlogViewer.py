from .main import *
from . import ui_BlogViewer,ShowPost

class ShowBlogViewer(QMainWindow, ui_BlogViewer.Ui_MainWindow):
    def __init__(self,blog,socket,username):
        super().__init__()
        self.setupUi(self)
        self.socket = socket
        self.postList = []
        self.username = username
        self.selfBlog = blog
        self.BlogTitle.setText(blog.Title)
        self.setWindowTitle("DanialCMS blog viewer")
        self.ViewPost.clicked.connect(lambda: self.ShowPost())
        self.refreshPosts()
        self.show()
    def refreshPosts(self):
        print("Ran!")
        self.PostList.clear()
        for p in self.postList:
            self.PostList.addItem(p.Title)
    def ShowPost(self):
        if len(self.PostList.selectedItems()) < 1:
            self.dlg = CDialog("Please select a post!", "Error!", True, self)
            self.dlg.exec()
            return
        title = self.PostList.selectedItems()[0].text()
        post = self.findPostByTitle(title)
        self.socket.sendall((self.selfBlog.UserDB+"/"+title+"/"+self.username).encode())
        self.editCreateWnd = ShowPost.ShowPost(
            title, post.Message, post.Writer)
    def findPostByTitle(self, title):
        for post in self.postList:
            if post.Title == title:
                return post
        return None