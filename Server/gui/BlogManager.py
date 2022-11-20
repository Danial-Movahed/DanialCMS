from . import SocketSystem
from .main import *
from . import EditCreate, ui_BlogManager, ShowPost, BlogMgmt


class Blog(QMainWindow, ui_BlogManager.Ui_MainWindow):
    def __init__(self,loggedInUser, title, dbname):
        super().__init__()
        self.setupUi(self)
        self.title = title
        self.dbname = dbname
        self.loggedInUser = loggedInUser
        self.setWindowTitle("DanialCMS blog manager")
        self.BlogTitle.setText(title)
        self.NewPost.clicked.connect(lambda: self.addPost())
        self.ViewPost.clicked.connect(lambda: self.viewPost())
        self.EditPost.clicked.connect(lambda: self.editPost())
        self.DeletePost.clicked.connect(lambda: self.deletePost())
        self.BlogMgmt.clicked.connect(lambda: self.blogMgmt())
        self.actionQuit.triggered.connect(lambda: self.close())
        self.show()
        self.engine = create_engine('sqlite:///'+self.dbname)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.engineP = create_engine(
            'sqlite:///Databases/Posts_'+(self.dbname.split("/")[1].split("_")[1]))
        Base.metadata.create_all(self.engineP)
        self.SessionP = sessionmaker(bind=self.engineP)
        self.sessionP = self.SessionP()
        self.savedPost = Post()

        existing_users = self.session.query(User).all()
        self.users = []
        for user in existing_users:
            self.users.append(user)

        self.serverThread = threading.Thread(target = SocketSystem.runServer, args = (self.users,))
        self.serverThread.daemon = True
        self.serverThread.start()

        self.posts = []
        self.refreshPosts()

    def addPost(self):
        self.editCreateWnd = EditCreate.EditCreate()
        self.editCreateWnd.closeEvent = self.savePost

    def savePost(self, e):
        if self.editCreateWnd.status:
            post = Post()
            post.Title = self.editCreateWnd.EditCreatePostTitle.text()
            post.Message = self.editCreateWnd.EditCreatePostMessage.toPlainText()
            post.Writer = self.loggedInUser.Username
            self.sessionP.add(post)
            self.sessionP.commit()
            self.refreshPosts()

    def viewPost(self):
        if len(self.PostList.selectedItems()) < 1:
            self.dlg = CDialog("Please select a post!", "Error!", True, self)
            self.dlg.exec()
            return
        title = self.PostList.selectedItems()[0].text()
        post = self.findPostByTitle(title)
        self.editCreateWnd = ShowPost.ShowPost(
            title, post.Message, post.Writer)

    def findPostByTitle(self, postTitle):
        for post in self.posts:
            if post.Title == postTitle:
                return post
        return None

    def deletePost(self, title=None):
        if not title == None:
            self.sessionP.delete(self.sessionP.query(Post).filter(
                Post.Title == title).first())
            self.sessionP.commit()
            self.refreshPosts()
            return
        if len(self.PostList.selectedItems()) < 1:
            self.dlg = CDialog("Please select a post!", "Error!", True, self)
            self.dlg.exec()
            return
        if not self.loggedInUser.isAdmin and self.sessionP.query(Post).filter(Post.Title == self.PostList.selectedItems()[0].text()).first().Writer != self.loggedInUser.Username:
            self.dlg = CDialog(
                "This post is not yours!", "Error!", True, self)
            self.dlg.exec()
            return
        self.dlg = CDialog(
            "Are you sure you want to delete this post?", "Question!", False, self)
        if self.dlg.exec():
            self.sessionP.delete(self.sessionP.query(Post).filter(
                Post.Title == self.PostList.selectedItems()[0].text()).first())
            self.sessionP.commit()
            self.refreshPosts()
        return

    def editPost(self):
        if len(self.PostList.selectedItems()) < 1:
            self.dlg = CDialog("Please select a post!", "Error!", True, self)
            self.dlg.exec()
            return
        if not self.loggedInUser.isAdmin and self.sessionP.query(Post).filter(Post.Title == self.PostList.selectedItems()[0].text()).first().Writer != self.loggedInUser.Username:
            self.dlg = CDialog(
                "This post is not yours!", "Error!", True, self)
            self.dlg.exec()
            return
        title = self.PostList.selectedItems()[0].text()
        self.savedPost = self.findPostByTitle(title)
        self.editCreateWnd = EditCreate.EditCreate(
            title, self.findPostByTitle(title).Message)
        self.deletePost(title)
        self.editCreateWnd.closeEvent = self.saveEditPost

    def saveEditPost(self, e):
        if self.editCreateWnd.status:
            post = Post()
            post.Title = self.editCreateWnd.EditCreatePostTitle.text()
            post.Message = self.editCreateWnd.EditCreatePostMessage.toPlainText()
            post.Writer = self.loggedInUser.Username
            self.sessionP.add(post)
            self.sessionP.commit()
            self.refreshPosts()
        else:
            make_transient(self.savedPost)
            self.savedPost._oid=None
            self.sessionP.add(self.savedPost)
            self.sessionP.commit()
            self.refreshPosts()

    def blogMgmt(self):
        self.blogMgmtWnd = BlogMgmt.BlogMgmt(self.session,"Databases/Posts_"+(self.dbname.split("/")[1].split("_")[1]),self.dbname,self.loggedInUser)

    def refreshPosts(self):
        existing_posts = self.sessionP.query(Post).all()
        self.PostList.clear()
        self.posts = []
        for post in existing_posts:
            self.posts.append(post)
            self.PostList.addItem(post.Title)