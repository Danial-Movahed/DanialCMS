from ast import Delete
from hashlib import blake2s
from sqlalchemy import Column, Boolean, String, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from . import EditCreate, ui_BlogManager, ShowPost
Base = declarative_base()


class CDialog(QDialog):
    def __init__(self, label, Title, mode, parent=None):
        super().__init__(parent)

        self.setWindowTitle(Title)
        if mode:
            QBtn = QDialogButtonBox.Ok
        else:
            QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        if not mode:
            self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        message = QLabel(label)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class User(Base):
    __tablename__ = 'UserDB'
    Username = Column(String(1000), primary_key=True, nullable=False)
    Password = Column(String(1000), nullable=False)
    isAdmin = Column(Boolean(), nullable=False)


class Post(Base):
    __tablename__ = 'PostDB'
    Title = Column(String(), primary_key=True, nullable=False)
    Message = Column(String(), nullable=False)


class Blog(QMainWindow, ui_BlogManager.Ui_MainWindow):
    def __init__(self, LoggedInUser, title, dbname):
        super().__init__()
        self.setupUi(self)
        self.title = title
        self.dbname = dbname
        self.loggedInUser = LoggedInUser
        self.setWindowTitle("DanialCMS blog manager")
        self.BlogTitle.setText(title)
        self.NewPost.clicked.connect(lambda: self.addPost())
        self.ViewPost.clicked.connect(lambda: self.viewPost())
        # self.EditPost.clicked.connect(lambda: self.editPost())
        self.DeletePost.clicked.connect(lambda: self.deletePost())
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
        self.users = []
        self.posts = []
        self.refreshPosts()
        self.refreshUsers()

    def addPost(self):
        self.editCreateWnd = EditCreate.EditCreate()
        self.editCreateWnd.closeEvent = self.savePost

    def savePost(self, e):
        if self.editCreateWnd.status:
            post = Post()
            post.Title = self.editCreateWnd.EditCreatePostTitle.text()
            post.Message = self.editCreateWnd.EditCreatePostMessage.toPlainText()
            self.sessionP.add(post)
            self.sessionP.commit()
            self.refreshPosts()

    def viewPost(self):
        if len(self.PostList.selectedItems()) < 1:
            self.dlg = CDialog("Please select a post!", "Error!", True, self)
            self.dlg.exec()
            return
        for post in self.posts:
            if post.Title == self.PostList.selectedItems()[0].text():
                self.editCreateWnd = ShowPost.ShowPost(
                    post.Title, post.Message)
                return
    def deletePost(self):
        self.dlg = CDialog("Are you sure you want to delete this post?", "Question!", False, self)
        if self.dlg.exec():
            print(self.PostList.selectedItems()[0].text())
            self.session.delete(self.session).where(self.session.Post.Title=="test2")
            self.session.commit()
            self.refreshPosts()
        else:
            print("Cancel!")

        return
    def refreshPosts(self):
        existing_posts = self.sessionP.query(Post).all()
        self.PostList.clear()
        self.posts = []
        for post in existing_posts:
            self.posts.append(post)
            self.PostList.addItem(post.Title)

    def refreshUsers(self):
        existing_users = self.session.query(User).all()
        self.users = []
        for user in existing_users:
            self.users.append(user)

    def addUser(self, Username, Password, isAdmin):
        if self.loggedInUser.isAdmin:
            for u in self.users:
                if Username == u.Username:
                    print("This user already exists!")
                    return
            user = User()
            user.Username = Username
            user.Password = Password
            user.isAdmin = isAdmin
            self.session.add(user)
            self.session.commit()
            self.users.append(user)
            return
        print("You are not admin!")

    def printUsers(self):
        for u in self.users:
            print(u.Username)

# a.addPost("asdf", "lorem ipsum dolor sit amet")
# a.addUser(input(), blake2s(input().encode()).hexdigest(), True)
# a.printPosts()
# a.printUsers()
