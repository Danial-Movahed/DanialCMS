from hashlib import blake2s
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
import socket
import select
import threading
import pickle
import platform
import subprocess

Base = declarative_base()

class Post(Base):
    __tablename__ = 'PostDB'
    BlogUserDB = Column(String(), nullable=False)
    Title = Column(String(), primary_key=True, nullable=False)
    Message = Column(String(), nullable=False)
    Writer = Column(String(), nullable=False)
    ReadBy = Column(String(), nullable=True)
    isPrivate = Column(Boolean(), nullable=False)
    WhoCanRead = Column(String(), nullable=True)

class User():
    Username = None
    Password = None
    isAdmin = False

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

class Blogs(Base):
    __tablename__ = 'Blogs'
    Title = Column(String(1000), nullable=False)
    UserDB = Column(String(1000), primary_key=True, nullable=False)
    isSub = False
    WndHndl = None

class BlogLoginObj():
    Title = None
    UserDB = None
    Username = None
    Password = None