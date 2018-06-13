from FlaskServer.db import db

class TeacherModel(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    location = db.Column(db.String(80))
    active = db.Column(db.Integer)

    def __init__(self, username, password, firstname, lastname, location, active):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname      
        self.location = location
        self.active = active

    def json(self):
        return {'username': self.username, 'password': self.password, 
                'firstname': self.firstname, 'lastname': self.lastname, 
                'location': self.location, 'active': self.active}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()






