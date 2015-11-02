
import sqlite3, hashlib, datetime, pymongo
from pymongo import MongoClient

connection = MongoClient()

db = connection['bloginator9000']

#print db.user.find()
#print db.user()

def makeTables():
    conn = sqlite3.connect("bloginator9000.db")
    c = conn.cursor()
    c.execute("create table if not exists post (title text, body text, postid INTEGER PRIMARY KEY, userid text, timestamp DATETIME, CHECK(title <> ''), CHECK(body <> ''))")
    c.execute("create table if not exists comment (body text, id INTEGER PRIMARY KEY, postid int, userid text, timestamp DATETIME, CHECK(body <> ''))")
    c.execute("create table if not exists user (username text UNIQUE, password text, CHECK(username <> ''), CHECK(password <> ''))")
    conn.commit()

#def makeTablesM():
#db.createCollection("post")
#    db.createCollection("comment")
#   db.createCollection("user")    

#--------------------------------------------------------------------------------------------------------------------------
    

def addPost(title, body, userid):
    try:
        conn = sqlite3.connect("bloginator9000.db")
        c = conn.cursor()
        c.execute("insert into post values (?, ?, NULL, ?, datetime(CURRENT_TIMESTAMP))",(title, body, userid))
        conn.commit()
        return True
    except:
        return False

    
def addPostM(title, body, userid):
    try:
        db.post.insert({"title": title, "blogtext": body, "username": userid, "date": datetime.datetime.now()})
        return True
    except:
        return False

#--------------------------------------------------------------------------------------------------------------------------
    

    
def getPosts():
    conn = sqlite3.connect("bloginator9000.db")
    c = conn.cursor()
    c.execute("select * from post order by timestamp")
    data = c.fetchall()
    data.reverse()
    data = [dict(zip(['title','blogtext','postid','username','date'], each)) for each in data]
    return data


def getPostsM():
    data = db.post.find().sort("date", pymongo.DESCENDING)
    datalist=[]
    for blah in data:
        datalist.append(blah)
    #print(datalist[0])
    return datalist
#--------------------------------------------------------------------------------------------------------------------------
    

    
def getPost(key, postid):
    conn = sqlite3.connect("bloginator9000.db")
    c = conn.cursor()
    c.execute("select * from post where {} = '{}'".format(key,postid))
    data = c.fetchall()
    data = [dict(zip(['title','blogtext','postid','username','date'], each)) for each in data]
    return data


#--------------------------------------------------------------------------------------------------------------------------
    

def addComment(body, replyid, userid):
    try:
        conn = sqlite3.connect("bloginator9000.db")
        c = conn.cursor()
        c.execute("insert into comment values (?, NULL, ?, ?, datetime(CURRENT_TIMESTAMP))",(body, replyid, userid))
        conn.commit()
        return True
    except:
        return False

#--------------------------------------------------------------------------------------------------------------------------
    

    
def getComments(key, postid):
    conn = sqlite3.connect("bloginator9000.db")
    c = conn.cursor()
    c.execute("select * from comment where {} = '{}' order by timestamp".format(key,postid))
    data = c.fetchall()
    data.reverse()
    data = [dict(zip(['commenttext','commentid','postid','username','date'], each)) for each in data]
    return data

#--------------------------------------------------------------------------------------------------------------------------
    


def newUser(username, password):
    try:
        conn = sqlite3.connect("bloginator9000.db")
        c = conn.cursor()
        m = hashlib.sha224(password)
        query = "INSERT INTO user VALUES (\"%s\", \"%s\")" % (username, m.hexdigest())
        c.execute(query)
        conn.commit()
        return True
    except:
        return False

def newUserM(usrname, password):
    try:
        m = hashlib.sha224(password)
        db.user.insert_one({"username":usrname,"password":m.hexdigest()})
        return True
    except:
        return False

    
#--------------------------------------------------------------------------------------------------------------------------
    

    
def authenticate(username, password):
    conn = sqlite3.connect("bloginator9000.db")
    c = conn.cursor()
    m = hashlib.sha224(password).hexdigest()
    query = "SELECT password FROM user WHERE username=\"%s\"" % (username)
    c.execute(query)
    s1 = c.fetchone()
    if s1 == None:
        return False
    s2 = s1[0]
    if s2 == m:
        return True
    return False

def authenticateM(usrname, password):
    m = hashlib.sha224(password).hexdigest()
    hashpass = db.user.find({"username":usrname},{"password":1})
    for blah in hashpass:
        #print m
        #print blah["password"]
        if blah["password"] == None:
            return False
        if m == blah["password"]:
            return True
    return False
    

