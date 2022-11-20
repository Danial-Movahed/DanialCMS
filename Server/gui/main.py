from hashlib import blake2s
from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, make_transient
from sqlalchemy import create_engine
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from os import path, remove
import socket
import threading
import select


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


class Post(Base):
    __tablename__ = 'PostDB'
    Title = Column(String(), primary_key=True, nullable=False)
    Message = Column(String(), nullable=False)
    Writer = Column(String(), nullable=False)


class User(Base):
    __tablename__ = 'UserDB'
    Username = Column(String(1000), primary_key=True, nullable=False)
    Password = Column(String(1000), nullable=False)
    isAdmin = Column(Boolean(), nullable=False)


class Blogs(Base):
    __tablename__ = 'Blogs'
    Title = Column(String(1000), nullable=False)
    UserDB = Column(String(1000), primary_key=True, nullable=False)
