""" database dependencies to support Users db examples """
from flask import url_for
from werkzeug.utils import redirect
from werkzeug.wrappers import request
from random import randrange
from __init__ import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user


# Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along

# Define the Users table within the model
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) Users represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Discussion(db.Model):
    __tablename__ = 'discussion'

    uid = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Text, unique=False, nullable=False)
    uname = db.Column(db.Text, unique=False, nullable=False)

    def __init__(self, post, uname):
        self.uname = uname
        self.post = post

    def __repr__(self):
        return "Posts(" + str(self.uid) + "," + self.post + "," + self.uname + ",)"

    def create(self):
        try:
            # creates a person object from Users(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "User ID": self.uid,
            "post": self.post,
            "name": self.uname,
        }

class Notes(db.Model):
    __tablename__ = 'notes'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    unit = db.Column(db.Text, unique=False, nullable=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    #
    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, note, unit, userID):
        self.note = note
        self.unit = unit
        self.userID = userID

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + self.unit + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "note": self.note,
            "unit": self.unit,
            "userID": self.userID
        }


# ACCESS = {
#     'guest': 0,
#     'user': 1,
#     'admin': 2
# }

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    # define the Users schema
    userID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    phone = db.Column(db.String(255), unique=False, nullable=False)
    # roles = db.relationship('Role', secondary='user_roles')
    notes = db.relationship("Notes", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes of instance variables within object
    def __init__(self, name, email, password, phone):
        self.name = name
        self.email = email
        self.set_password(password)
        self.phone = phone


    # def is_admin(self):
    #     return self.access == ACCESS['admin']
    #
    # def allowed(self, access_level):
    #     return self.access >= access_level

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from Users(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "userID": self.userID,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "query": "by_alc"  # This is for fun, a little watermark
        }

    # CRUD update: updates users name, password, phone
    # returns self
    def update(self, name, password="", phone=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(password) > 0:
            self.set_password(password)
        if len(phone) > 0:
            self.phone = phone
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    # set password method is used to create encrypted password
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    # check password to check versus encrypted password
    def is_password_match(self, password):
        """Check hashed password."""
        result = check_password_hash(self.password, password)
        return result

    # required for login_user, overrides id (login_user default) to implemented userID
    def get_id(self):
        return self.userID


#
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(50), unique=True)
#
# class Userroles(db.Model):
#     __tablename__ = 'user_roles'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class coolendar(db.Model):
    __tablename__ = 'coolendar'

    ID = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer,  unique=True, nullable=False)
    information = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, day, information):
        self.day = day
        self.information = information

    def __repr__(self):
        return "coolendar(" + str(self.ID) + "," + self.day + "," + self.information + ")"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "day": self.day,
            "information": self.information
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing section"""


def model_builder():
    print("--------------------------")
    print("Seed Data for Table: users")
    print("--------------------------")
    db.create_all()
    """Tester data for table"""
    u1 = Users(name='Thomas Edison', email='tedison@example.com', password='123toby', phone="1111111111")
    u2 = Users(name='Nicholas Tesla', email='ntesla@example.com', password='123niko', phone="1111112222")
    u3 = Users(name='Alexander Graham Bell', email='agbell@example.com', password='123lex', phone="1111113333")
    u4 = Users(name='Eli Whitney', email='eliw@example.com', password='123whit', phone="1111114444")
    u5 = Users(name='John Mortensen', email='jmort1021@gmail.com', password='123qwerty', phone="8587754956")
    u6 = Users(name='John Mortensen', email='jmort1021@yahoo.com', password='123qwerty', phone="8587754956")
    # U7 intended to fail as duplicate key
    u7 = Users(name='John Mortensen', email='jmort1021@yahoo.com', password='123qwerty', phone="8586791294")
    u8 = Users(name='admin', email='admin@admin.admin', password='password', phone="1")
    table = [u1, u2, u3, u4, u5, u6, u7, u8]
    # admin_role = Role(name='Admin')
    # db.session.commit()
    # u8.roles = [admin_role,]
    # db.session.commit()
    for row in table:
        try:
            '''add a few 1 to 4 notes per user'''

            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {row.email}")

def model_driver():
    print("---------------------------")
    print("Create Tables and Seed Data")
    print("---------------------------")
    model_builder()

    print("---------------------------")
    print("Table: " + Users.__tablename__)
    print("Columns: ", Users.__table__.columns.keys())
    print("---------------------------")
    print("Table: " + Notes.__tablename__)
    print("Columns: ", Notes.__table__.columns.keys())
    print("---------------------------")
    print()


    users = Users.query
    for user in users:
        print("User" + "-" * 81)
        print(user.read())
        print("Notes" + "-" * 80)
        for note in user.notes:
            print(note.read())
        print("-" * 85)
        print()

class Events(db.Model):
    eventID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date = db.Column(db.String(255))
    description = db.Column(db.Text)

    def __init__(self, name, date, description):
        self.name = name
        self.date = date
        self.description = description

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def update(self, name, date="", description=""):
        if len(name) > 0:
            self.name = name
        if len(date) > 0:
            self.date = date
        if len(description) > 0:
            self.description = description
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    def read(self):
        return {
            "eventID": self.eventID,
            "date": self.date,
            "name": self.name,
            "description": self.description,
        }




def model_testerr():
    print("--------------------------")
    print("Seed Data for Table: coolendar")
    print("--------------------------")
    db.create_all()
    """Tester data for table"""
    u1 = coolendar(day='1', information='test tomorrow')
    u2 = coolendar(day='18', information='Chapters 28 and 29 homework due', )
    u3 = Events(name="Civil War", date="Apr 12, 1861 – Apr 9, 1865", description="the war that was civil")

    table = [u1, u2, u3]
    for row in table:
        try:
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            db.session.remove()

def model_printerr():
    print("------------")
    print("Table: users with SQL query")
    print("------------")
    result = db.session.execute('select * from coolendar')
    print(result.keys())
    for row in result:
        print(row)

def discussion_tester():
    print("--------------------------")
    print("Seed Data for Table: discussion")
    print("--------------------------")
    db.create_all()
    # p1 = Discussion(post='hi',uname=current_user.name)
    # p2 = Discussion(post='bye',uname=current_user.name)
    #
    # table = [p1, p2]
    # for row in table:
    #     try:
    #         db.session.add(row)
    #         db.session.commit()
    #     except IntegrityError:
    #         db.session.remove()

def discussion_printer():
    print("------------")
    print("Table: users with SQL query")
    print("------------")
    result = db.session.execute('select * from Discussion')
    print(result.keys())
    for row in result:
        print(row)

if __name__ == "__main__":
    model_driver()
    model_testerr()
    model_printerr()
    discussion_tester()
    discussion_printer()


