from FlaskServer.db import db
from sqlalchemy.orm import relationship

class AbonementModel(db.Model):
    __tablename__ = 'abonements'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    duration = db.Column(db.Integer)
    price = db.Column(db.Integer)
    students = db.relationship('StudentModel', lazy='dynamic')


    def __init__(self, name, duration, price):
        self.name = name
        self.duration = duration
        self.price = price      
   

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'name': self.name, 
                'duration': self.duration, 
                'price': self.price,
                'students': [student.json() for student in self.students.all()] }


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


