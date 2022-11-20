from .main import *
from . import ui_Login,BlogManager

def LoggedIn(u, title, dbname):
    global blogmgrwnd
    blogmgrwnd = BlogManager.Blog(u,title, dbname)

class BlogLogin(QMainWindow, ui_Login.Ui_MainWindow):
    def __init__(self, dbname, title):
        super().__init__()
        self.setupUi(self)
        self.dbname = dbname
        self.title = title
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
                LoggedIn(user, self.title, self.dbname)
                self.close()
                return
        self.label_6.setText("Wrong username or password!")
