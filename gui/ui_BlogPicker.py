# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Resources/BlogPicker.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(861, 621)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(43)
        self.label.setFont(font)
        self.label.setStyleSheet("background: url(:/bg/background.png);\n"
"background-position: bottom;\n"
"margin-bottom: 10px;\n"
"border-radius: 20px;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(30, -1, 30, -1)
        self.horizontalLayout.setSpacing(17)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ListBlogs = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ListBlogs.sizePolicy().hasHeightForWidth())
        self.ListBlogs.setSizePolicy(sizePolicy)
        self.ListBlogs.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.ListBlogs.setFont(font)
        self.ListBlogs.setStyleSheet("background-color: #444;\n"
"border-radius:10px;")
        self.ListBlogs.setObjectName("ListBlogs")
        self.horizontalLayout.addWidget(self.ListBlogs)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Refreshbtn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Refreshbtn.sizePolicy().hasHeightForWidth())
        self.Refreshbtn.setSizePolicy(sizePolicy)
        self.Refreshbtn.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.Refreshbtn.setFont(font)
        self.Refreshbtn.setStyleSheet("background-color: rgb(5, 163, 55);\n"
"border-radius: 10px;\n"
"padding: 0px 5px;")
        self.Refreshbtn.setObjectName("Refreshbtn")
        self.verticalLayout_2.addWidget(self.Refreshbtn)
        self.NewBlogbtn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NewBlogbtn.sizePolicy().hasHeightForWidth())
        self.NewBlogbtn.setSizePolicy(sizePolicy)
        self.NewBlogbtn.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.NewBlogbtn.setFont(font)
        self.NewBlogbtn.setStyleSheet("border-radius: 10px;\n"
"padding: 0px 5px;\n"
"background-color: rgb(5, 87, 163);")
        self.NewBlogbtn.setObjectName("NewBlogbtn")
        self.verticalLayout_2.addWidget(self.NewBlogbtn)
        self.LoadBlogbtn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LoadBlogbtn.sizePolicy().hasHeightForWidth())
        self.LoadBlogbtn.setSizePolicy(sizePolicy)
        self.LoadBlogbtn.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.LoadBlogbtn.setFont(font)
        self.LoadBlogbtn.setStyleSheet("background-color: #cf9904;\n"
"border-radius: 10px;\n"
"padding: 0px 5px;")
        self.LoadBlogbtn.setObjectName("LoadBlogbtn")
        self.verticalLayout_2.addWidget(self.LoadBlogbtn)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 861, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionMr_Ahmadi_Mode = QtWidgets.QAction(MainWindow)
        self.actionMr_Ahmadi_Mode.setObjectName("actionMr_Ahmadi_Mode")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionMr_Ahmadi_Mode_2 = QtWidgets.QAction(MainWindow)
        self.actionMr_Ahmadi_Mode_2.setObjectName("actionMr_Ahmadi_Mode_2")
        self.menuFile.addAction(self.actionQuit)
        self.menuFile.addSeparator()
        self.menuOptions.addAction(self.actionMr_Ahmadi_Mode_2)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Welcome to DanialCMS!"))
        self.Refreshbtn.setText(_translate("MainWindow", "Refresh"))
        self.NewBlogbtn.setText(_translate("MainWindow", "New Blog"))
        self.LoadBlogbtn.setText(_translate("MainWindow", "Load Blog"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.actionMr_Ahmadi_Mode.setText(_translate("MainWindow", "Mr.Ahmadi Mode!"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionMr_Ahmadi_Mode_2.setText(_translate("MainWindow", "Mr.Ahmadi Mode!"))
from . import bg_rc
