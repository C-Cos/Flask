from Models.model import User

def index(db):
    users = User.getall(db)
    return users

def new(db, name, email, password):
    User.add_new(db, name, email, password)

def log(db, username):
    user = User.check(db, username)
    return user

def display_user(db, userid):
    user = User.display_one(db, userid)
    return user

def remove(db, id):
    User.delete_user(db, id)

def update(db, id, name, email, password):
    User.update_user(db, id, name, email, password)





  