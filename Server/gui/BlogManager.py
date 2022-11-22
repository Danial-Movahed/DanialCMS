from . import SocketSystem
from .main import *
from . import EditCreate, ui_BlogManager, ShowPost, BlogMgmt


class Blog(QMainWindow, ui_BlogManager.Ui_MainWindow):
    def __init__(self, loggedInUser, title, dbname):
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
        SocketSystem.userList = []
        for user in existing_users:
            SocketSystem.userList.append(user)
        self.serverThread = threading.Thread(
            target=SocketSystem.runServer, args=(title,))
        self.serverThread.daemon = True
        self.serverThread.start()
        self.rssServerThread = threading.Thread(target=SocketSystem.runRSSServer,args=())
        self.rssServerThread.daemon = True
        self.rssServerThread.start()

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
            post.WhoCanRead = self.editCreateWnd.EditCreateWhoCanRead.text()
            if self.loggedInUser.Username not in post.WhoCanRead.split(" "):
                post.WhoCanRead+=" "+self.loggedInUser.Username
            self.sessionP.add(post)
            self.sessionP.commit()
            self.refreshPosts()
            for conn in SocketSystem.conn:
                conn.whatWrk = "n"

    def viewPost(self):
        if len(self.PostList.selectedItems()) < 1:
            self.dlg = CDialog("Please select a post!", "Error!", True, self)
            self.dlg.exec()
            return
        title = self.PostList.selectedItems()[0].text()
        self.sessionP.query(Post).filter(Post.Title == title).ReadBy = self.findPostByTitleInSocket(title).ReadBy
        self.sessionP.commit()
        post = self.findPostByTitle(title)
        self.editCreateWnd = ShowPost.ShowPost(
            title, post.Message, post.Writer, post.ReadBy)

    def findPostByTitle(self, postTitle):
        for post in self.posts:
            if post.Title == postTitle:
                return post
        return None

    def findPostByTitleInSocket(self, postTitle):
        for post in SocketSystem.postList:
            if post.Title == postTitle:
                return post
        return None

    def deletePost(self, title=None):
        if not title == None:
            self.sessionP.delete(self.sessionP.query(Post).filter(
                Post.Title == title).first())
            self.sessionP.commit()
            self.refreshPosts()
            for conn in SocketSystem.conn:
                conn.whatWrk = "d"
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
            for conn in SocketSystem.conn:
                conn.whatWrk = "d"
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
            title, self.savedPost.Message, self.savedPost.WhoCanRead)
        self.deletePost(title)
        self.editCreateWnd.closeEvent = self.saveEditPost

    def saveEditPost(self, e):
        if self.editCreateWnd.status:
            post = Post()
            post.Title = self.editCreateWnd.EditCreatePostTitle.text()
            post.Message = self.editCreateWnd.EditCreatePostMessage.toPlainText()
            post.Writer = self.loggedInUser.Username
            post.WhoCanRead = self.editCreateWnd.EditCreateWhoCanRead.text()
            if self.loggedInUser.Username not in post.WhoCanRead.split(" "):
                post.WhoCanRead+=" "+self.loggedInUser.Username
            self.sessionP.add(post)
            self.sessionP.commit()
            self.refreshPosts()
            for conn in SocketSystem.conn:
                conn.whatWrk = "e"
        else:
            make_transient(self.savedPost)
            self.savedPost._oid = None
            self.sessionP.add(self.savedPost)
            self.sessionP.commit()
            self.refreshPosts()
            for conn in SocketSystem.conn:
                conn.whatWrk = "e"

    def blogMgmt(self):
        self.blogMgmtWnd = BlogMgmt.BlogMgmt(self.session, "Databases/Posts_"+(
            self.dbname.split("/")[1].split("_")[1]), self.dbname, self.loggedInUser)

    def refreshPosts(self):
        existing_posts = self.sessionP.query(Post).all()
        self.PostList.clear()
        self.posts = []
        SocketSystem.postList = []
        fg = FeedGenerator()
        fg.link(href="http://"+SocketSystem.get_ip_address()+":8080",rel="alternate")
        fg.title(self.title)
        fg.description("A DanialCMS blog!")
        fg.language('en')
        for post in existing_posts:
            if self.loggedInUser.Username in post.WhoCanRead.split(" "):
                self.posts.append(post)
                self.PostList.addItem(post.Title)
            SocketSystem.postList.append(post)
            fe = fg.add_entry()
            fe.id(post.Message)
            fe.title(post.Title)
        SocketSystem.rss = fg.rss_str(pretty=True)
