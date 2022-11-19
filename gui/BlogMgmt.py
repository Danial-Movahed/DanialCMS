from .main import *
from . import ui_BlogMgmt


class BlogMgmt(QMainWindow, ui_BlogMgmt.Ui_MainWindow):
    def __init__(self, session):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("DanialCMS blog management")
        self.session = session
        self.Users = []
        self.adminCount = 0
        self.refreshUsers()
        self.BlogMgmtDeleteUser.clicked.connect(lambda: self.deleteUser())
        self.show()

    def refreshUsers(self):
        existing_users = self.session.query(User).all()
        self.Users = []
        self.adminCount = 0
        self.BlogMgmtUsersList.clear()
        for user in existing_users:
            self.Users.append(user)
            self.BlogMgmtUsersList.addItem(user.Username)
            if user.isAdmin:
                self.adminCount += 1

    def findUserByUsername(self, username):
        for user in self.Users:
            if user.Username == username:
                return user
        return None

    def deleteUser(self):
        if len(self.BlogMgmtUsersList.selectedItems()) < 1:
            self.dlg = CDialog("Please select a User!", "Error!", True, self)
            self.dlg.exec()
            return
        username = self.BlogMgmtUsersList.selectedItems()[0].text()
        user = self.findUserByUsername(username)
        self.dlg = CDialog(
            "Are you sure you want to delete this user?", "Question!", False, self)
        if self.dlg.exec():
            if user.isAdmin and self.adminCount == 1:
                self.dlg = CDialog("You should at least have one admin!", "Error!", True, self)
                self.dlg.exec()
                return
            self.session.delete(self.session.query(User).filter(User.Username == username).first())
            self.session.commit()
            self.refreshUsers()
        return
