from .main import *
from time import sleep
from .Login import *

conn = []
blogList = []
rss = ""
id = 0


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


# class RSSServer(BaseHTTPRequestHandler):
#     def do_GET(self):
#         global rss
#         self.send_response(200)
#         self.send_header("Content-type", "application/rss+xml")
#         self.end_headers()
#         self.wfile.write(rss)


class client_thread(threading.Thread):
    def __init__(self, clientsocket, id, blogPkrWnd):
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket
        self.clientsocket.setblocking(0)
        self.blogPkrWnd = blogPkrWnd
        self.id = id
        self.connected = True
        self.whatWrk = "f"
        self.whichBlg = "f"

    def run(self):
        global blogList
        while self.connected:
            try:
                if self.whatWrk == "f":
                    self.clientsocket.send("FS".encode())
                    sleep(0.5)
                    for b in blogList:
                        tosend = Blogs()
                        tosend.Title = b.Title
                        tosend.UserDB = b.UserDB
                        self.clientsocket.send(pickle.dumps(tosend))
                        sleep(0.5)
                    self.clientsocket.send("Done".encode())
                    sleep(0.5)
                    self.whatWrk = ""
                elif self.whatWrk == "n":
                    self.clientsocket.send("NB".encode())
                    sleep(0.5)
                    tosend = Blogs()
                    tosend.Title = blogList[-1].Title
                    tosend.UserDB = blogList[-1].UserDB
                    tmp = pickle.dumps(tosend)
                    self.clientsocket.send(tmp)
                    sleep(0.5)
                    self.clientsocket.send("Done".encode())
                    sleep(0.5)
                    self.whatWrk = ""
                elif self.whatWrk == "np":
                    for b in blogList:
                        if b.UserDB == self.whichBlg:
                            self.clientsocket.send("NP".encode())
                            sleep(0.5)
                            self.clientsocket.send(pickle.dumps(b.WndHndl.posts[-1]))
                            sleep(0.5)
                            self.clientsocket.send("Done".encode())
                            sleep(0.5)
                    self.whatWrk = ""
                    self.whichBlg = ""
                elif self.whatWrk == "dp":
                    for b in blogList:
                        if b.UserDB == self.whichBlg:
                            self.clientsocket.send(("DP "+self.whichBlg).encode())
                            sleep(0.5)
                            for p in b.WndHndl.posts:
                                self.clientsocket.send(pickle.dumps(p))
                                sleep(0.5)
                            self.clientsocket.send("Done".encode())
                            sleep(0.5)
                    self.whatWrk = ""
                    self.whichBlg = ""                
                elif self.whatWrk == "ep":
                    for b in blogList:
                        if b.UserDB == self.whichBlg:
                            self.clientsocket.send(("EP "+self.whichBlg).encode())
                            sleep(0.5)
                            for p in b.WndHndl.posts:
                                self.clientsocket.send(pickle.dumps(p))
                                sleep(0.5)
                            self.clientsocket.send("Done".encode())
                            sleep(0.5)
                    self.whatWrk = ""
                    self.whichBlg = ""
                elif self.whatWrk == "db":
                    self.clientsocket.send("DB".encode())
                    sleep(0.5)
                    for b in blogList:
                        tosend = Blogs()
                        tosend.Title = b.Title
                        tosend.UserDB = b.UserDB
                        self.clientsocket.send(pickle.dumps(tosend))
                        sleep(0.5)
                    self.clientsocket.send("Done".encode())
                    sleep(0.5)
                    self.whatWrk = ""


                ready = select.select([self.clientsocket], [], [], 1)
                if ready[0]:
                    data = self.clientsocket.recv(4096)
                    try:
                        data=data.decode()
                        data=data.split("/")
                        enginePost = create_engine(
                            'sqlite:///Databases/Posts_'+(data[1].split("_")[1]))
                        SessionPost = sessionmaker(bind=enginePost)
                        sessionPost = SessionPost()
                        tmp = sessionPost.query(Post).filter(Post.Title == data[2]).first()
                        print(tmp.Title)
                        if tmp.ReadBy == None:
                            tmp.ReadBy=data[3]
                        elif data[3] not in tmp.ReadBy.split(" "):
                            tmp.ReadBy+=" "+data[3]
                        sessionPost.commit()
                    except:
                        tmp=pickle.loads(data)
                        tmp2=Blogs()
                        tmp2.Title=tmp.Title
                        tmp2.UserDB=tmp.UserDB
                        self.loginWnd = BlogLogin(tmp2,False,tmp.Username,tmp.Password)
                        if self.loginWnd.checkSecrets(True):
                            print("Yep!")
                            self.clientsocket.send("Ok".encode())
                            sleep(0.5)
                            engine = create_engine('sqlite:///'+tmp.UserDB)
                            Base.metadata.create_all(engine)
                            Session = sessionmaker(bind=engine)
                            session = Session()
                            engineP = create_engine(
                                'sqlite:///Databases/Posts_'+(tmp.UserDB.split("/")[1].split("_")[1]))
                            Base.metadata.create_all(engineP)
                            SessionP = sessionmaker(bind=engineP)
                            sessionP = SessionP()
                            existing_posts = sessionP.query(Post).all()
                            self.clientsocket.send("FSP".encode())
                            sleep(2)
                            for post in existing_posts:
                                print(post.Title)
                                self.clientsocket.send(pickle.dumps(post))
                                sleep(0.5)
                        else:
                            self.clientsocket.send("Nope".encode())
                            sleep(0.5)

                self.clientsocket.send("keep-alive".encode())
                sleep(0.5)
            except:
                self.connected = False
                global id, conn
                id -= 1
                conn.remove(self)
                print(conn)


def runServer(blogPkrWnd):
    global id, conn, userList
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(("", 4524))
    serversocket.listen(5)
    while True:
        (clientsocket, address) = serversocket.accept()
        print("accepted!")
        conn.append(client_thread(clientsocket, id, blogPkrWnd))
        conn[id].start()
        id += 1

# def runRSSServer():
#     webServer = HTTPServer(("", 8080), RSSServer)
#     webServer.serve_forever()