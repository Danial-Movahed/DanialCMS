from .main import *
from . import ui_Login,BlogManager

def fixWndHndl(blog):
    blog.WndHndl = None

def LoggedIn(u, blog):
    blog.WndHndl = BlogManager.Blog(u,blog.Title, blog.UserDB)
    blog.WndHndl.closeEvent = lambda event: fixWndHndl(blog)
class BlogLogin(QMainWindow, ui_Login.Ui_MainWindow):
    def __init__(self, blog, runFTSetup=True,username=None,password=None):
        super().__init__()
        self.setupUi(self)
        self.dbname = blog.UserDB
        self.title = blog.Title
        self.blog = blog
        self.engine = create_engine('sqlite:///'+self.dbname)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        if password != None:
            self.LoginPassword.setText(password)
        if username != None:
            self.LoginUsername.setText(username)
        if runFTSetup:
            self.LoginContinuebtn.clicked.connect(lambda: self.checkSecrets())
            self.LoginQuitbtn.clicked.connect(lambda: self.close())
            self.setWindowTitle("DanialCMS login")
            self.show()

    def checkSecrets(self,onlyCheck = False):
        self.session.expire_all()
        existing_Users = self.session.query(User).all()
        for user in existing_Users:
            if not onlyCheck:
                if self.LoginUsername.text() == user.Username and blake2s(self.LoginPassword.text().encode()).hexdigest() == user.Password:
                    self.label_6.setText("Welcome!")
                    LoggedIn(user, self.blog)
                    self.close()
                    self.session.close()
                    return
            else:
                if self.LoginUsername.text() == user.Username and self.LoginPassword.text() == user.Password:
                    self.session.close()
                    return True
        if onlyCheck:
            self.session.close()
            return False

        self.label_6.setText("Wrong username or password!")
