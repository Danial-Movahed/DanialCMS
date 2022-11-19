from .main import *
from . import ui_BlogMgmt


class BlogMgmt(QMainWindow, ui_BlogMgmt.Ui_MainWindow):
    def __init__(self,session):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("DanialCMS blog management")
        self.session = session
        self.users = []
        self.adminCount = 0
        self.refreshUsers()
        #self.BlogMgmtDeleteUser.clicked.connect(lambda: self.deleteUser())
        self.show()
    def refreshUsers(self):
        existing_users = self.session.query(User).all()
        self.users = []
        self.BlogMgmtUsersList.clear()
        for user in existing_users:
            self.users.append(user)
            self.BlogMgmtUsersList.addItem(user.Username)
    def findUserByUsername(self, username):
        for user in self.users:
            if user.Username == username:
                return user
        return None
    # def deleteUser(self):
    #     user = self.findUserByUsername(self.BlogMgmtUsersList.selectedItems()[0].text())
    #     if len(self.BlogMgmtUsersList.selectedItems()) < 1:
    #         self.dlg = CDialog("Please select a post!", "Error!", True, self)
    #         self.dlg.exec()
    #         return
    #     self.dlg = CDialog(
    #         "Are you sure you want to delete this post?", "Question!", False, self)
    #     if self.dlg.exec():
    #         self.sessionP.delete(self.sessionP.query(Post).filter(
    #             Post.Title == self.PostList.selectedItems()[0].text()).first())
    #         self.sessionP.commit()
    #         self.refreshPosts()
    #     else:
    #         print("Cancel!")
    #     return