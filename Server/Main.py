from gui.main import *
from gui import ui_CreateBlogWizard, ui_BlogPicker, SocketSystem
from gui.Login import *

Base = declarative_base()


class Blogs(Base):
    __tablename__ = 'Blogs'
    Title = Column(String(1000), nullable=False)
    UserDB = Column(String(1000), primary_key=True, nullable=False)


engine = create_engine('sqlite:///Databases/Blogs.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'UserDB'
    Username = Column(String(1000), primary_key=True, nullable=False)
    Password = Column(String(1000), nullable=False)
    isAdmin = Column(Boolean(), nullable=False)


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
        blog.Title = self.BlogTitle.text()
        dbname = "Databases/Users_"+blog.Title+".db"
        i = 1
        while path.exists(dbname):
            dbname = "Databases/Users_"+blog.Title+str(i)+".db"
            i += 1
        blog.UserDB = dbname
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
        self.serverThread = threading.Thread(
            target=SocketSystem.runServer, args=())
        self.serverThread.daemon = True
        self.serverThread.start()
        self.show()

    def startWizard(self):
        self.wzd = CreateBlogWizard()
        self.wzd.closeEvent = self.saveBlog

    def saveBlog(self, e):
        self.refresh()
        for conn in SocketSystem.conn:
            conn.whatWrk = "n"

    def refresh(self):
        existing_Blogs = session.query(Blogs).all()
        self.ListBlogs.clear()
        for blog in existing_Blogs:
            self.ListBlogs.addItem(blog.Title+", "+blog.UserDB)
            SocketSystem.blogList.append(blog)

    def loadblog(self):
        if len(self.ListBlogs.selectedItems()) < 1:
            self.dlg = ErrorDialog("Please select a blog!", self)
            self.dlg.exec()
            return
        existing_Blogs = session.query(Blogs).all()
        for blog in existing_Blogs:
            if blog.Title+", "+blog.UserDB == self.ListBlogs.selectedItems()[0].text():
                self.loginWnd = BlogLogin(blog,True)

if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("DanialCMS")
    wnd = BlogPicker()
    app.exec()
