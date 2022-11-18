from base64 import encode
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from hashlib import blake2s
from gui import ui_Login

Base = declarative_base()

LoggedInUser = None


def LoggedIn(u):
    global LoggedInUser
    LoggedInUser = u
    print(LoggedInUser.Username)


class User(Base):
    __tablename__ = 'UserDB'
    Username = Column(String(1000), primary_key=True, nullable=False)
    Password = Column(String(1000), nullable=False)
    isAdmin = Column(Boolean(), nullable=False)

class BlogLogin(QMainWindow, ui_Login.Ui_MainWindow):
    def __init__(self, dbname):
        super().__init__()
        self.setupUi(self)
        self.engine = create_engine('sqlite:///'+dbname)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.LoginContinuebtn.clicked.connect(lambda: self.checkSecrets())
        self.LoginQuitbtn.clicked.connect(lambda: self.close())
        self.setWindowTitle("DanialCMS login")
        self.show()

    def checkSecrets(self):
        existing_Users = self.session.query(User).all()
        for user in existing_Users:
            if self.LoginUsername.text() == user.Username and blake2s(self.LoginPassword.text().encode()).hexdigest() == user.Password:
                self.label_6.setText("Welcome!")
                LoggedIn(user)
                return
        self.label_6.setText("Wrong username or password!")
