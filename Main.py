from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from gui import ui_CreateBlogWizard, ui_BlogPicker
from os import path
from hashlib import blake2s
from gui.Login import *

Base = declarative_base()


class Blogs(Base):
    __tablename__ = 'Blogs'
    Title = Column(String(1000), nullable=False)
    UserDB = Column(String(1000), primary_key=True, nullable=False)


class User(Base):
    __tablename__ = 'UserDB'
    Username = Column(String(1000), primary_key=True, nullable=False)
    Password = Column(String(1000), nullable=False)
    isAdmin = Column(Boolean(), nullable=False)


engine = create_engine('sqlite:///Databases/Blogs.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class CreateBlogWizard(QMainWindow, ui_CreateBlogWizard.Ui_MainWindow):
    def __init__(self):
        super(CreateBlogWizard, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("DanialCMS blog wizard")
        self.Quitbtn.clicked.connect(lambda: self.close())
        self.Backbtn1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(
            self.stackedWidget.currentIndex()-1))
        self.Backbtn2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(
            self.stackedWidget.currentIndex()-1))
        self.Nextbtn1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(
            self.stackedWidget.currentIndex()+1))
        self.Nextbtn2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(
            self.stackedWidget.currentIndex()+1))
        self.Nextbtn3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(
            self.stackedWidget.currentIndex()+1))
        self.Donebtn.clicked.connect(lambda: self.createBlog())
        self.show()

    def createBlog(self):
        blog = Blogs()
        print(self.BlogTitle.text())
        blog.Title = self.BlogTitle.text()
        dbname = "Databases/Users_"+blog.Title+".db"
        i = 1
        while path.exists(dbname):
            dbname = "Databases/Users_"+blog.Title+str(i)+".db"
            i += 1
        blog.UserDB = dbname
        print(dbname)
        session.add(blog)
        session.commit()
        self.engine = create_engine('sqlite:///'+dbname)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        user = User()
        user.Username = self.BlogUsername.text()
        user.Password = blake2s(self.BlogPassword.text().encode()).hexdigest()
        user.isAdmin = True
        self.session.add(user)
        self.session.commit()
        self.close()


class ErrorDialog(QDialog):
    def __init__(self, label, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Error!")

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(lambda: self.close())
        self.layout = QVBoxLayout()
        message = QLabel(label)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class BlogPicker(QMainWindow, ui_BlogPicker.Ui_MainWindow):
    def __init__(self):
        super(BlogPicker, self).__init__()
        self.setupUi(self)
        self.NewBlogbtn.clicked.connect(lambda: self.startWizard())
        self.Refreshbtn.clicked.connect(lambda: self.refresh())
        self.actionQuit.triggered.connect(lambda: self.close())
        self.LoadBlogbtn.clicked.connect(lambda: self.loadblog())
        self.refresh()
        self.setWindowTitle("DanialCMS")
        self.show()

    def startWizard(self):
        self.wzd = CreateBlogWizard()
        self.wzd.closeEvent = self.refresh

    def refresh(self, e=None):
        existing_Blogs = session.query(Blogs).all()
        self.ListBlogs.clear()
        for blog in existing_Blogs:
            self.ListBlogs.addItem(blog.Title+", "+blog.UserDB)

    def loadblog(self):
        if len(self.ListBlogs.selectedItems()) < 1:
            self.dlg = ErrorDialog("Please select a blog!", self)
            self.dlg.exec()
            return
        self.loginWnd = BlogLogin(self.ListBlogs.selectedItems()[
                                  0].text().split(",")[1].strip())


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("DanialCMS")
    wnd = BlogPicker()
    app.exec()
