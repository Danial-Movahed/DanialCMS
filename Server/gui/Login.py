from .main import *
from . import ui_Login,BlogManager

def LoggedIn(u, title, dbname):
    global blogmgrwnd
    blogmgrwnd = BlogManager.Blog(u,title, dbname)

class BlogLogin(QMainWindow, ui_Login.Ui_MainWindow):
    def __init__(self, dbname, title, runFTSetup=True,username=None,password=None):
        super().__init__()
        self.setupUi(self)
        self.dbname = dbname
        self.title = title
        self.engine = create_engine('sqlite:///'+dbname)
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
        existing_Users = self.session.query(User).all()
        for user in existing_Users:
            if not onlyCheck:
                if self.LoginUsername.text() == user.Username and blake2s(self.LoginPassword.text().encode()).hexdigest() == user.Password:
                    self.label_6.setText("Welcome!")
                    LoggedIn(user, self.title, self.dbname)
                    self.close()
                    return
            else:
                print(self.LoginUsername.text())
                print(self.LoginPassword.text())
                if self.LoginUsername.text() == user.Username and self.LoginPassword.text() == user.Password:
                    return True
        if onlyCheck:
            return False

        self.label_6.setText("Wrong username or password!")
