from hashlib import blake2s
from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'UserDB'
    Username = Column(String(1000), primary_key=True, nullable=False)
    Password = Column(String(1000), nullable=False)
    isAdmin = Column(Boolean(), nullable=False)


engine = create_engine('sqlite:///Users.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Blog():
    def __init__(self):
        self.posts = []
        self.users = []
        existing_users = session.query(User).all()
        for user in existing_users:
            self.users.append(user)
        self.loggedInUser = None
        self.loggedIn = False

    def addPost(self, Title, PostMessage):
        if self.loggedIn:
            tmp = [Title, self.loggedInUser.Username, PostMessage]
            self.posts.append(tmp)
        else:
            print("You need to login before posting!")

    def login(self, Username, Password):
        for u in self.users:
            if Username == u.Username and Password == u.Password:
                self.loggedInUser = u
                self.loggedIn = True
                print("Welcome", Username)
                if self.loggedInUser.isAdmin:
                    print("You are admin!")
                else:
                    print("You are normal user!")
                return
        print("Wrong username or password!")

    def printPosts(self):
        print(self.posts)

    def addUser(self, Username, Password, isAdmin):
        if self.loggedInUser.isAdmin:
            for u in self.users:
                if Username == u.Username:
                    print("This user already exists!")
                    return
            user = User()
            user.Username = Username
            user.Password = Password
            user.isAdmin = isAdmin
            session.add(user)
            session.commit()
            self.users.append(user)
            return
        print("You are not admin!")

    def printUsers(self):
        for u in self.users:
            print(u.Username)


a = Blog()
print("Please login!")
a.login(input("Username: "), blake2s(input("Password: ").encode()).hexdigest())
a.addPost("asdf", "lorem ipsum dolor sit amet")
a.addUser(input(), blake2s(input().encode()).hexdigest(), True)
a.printPosts()
a.printUsers()
