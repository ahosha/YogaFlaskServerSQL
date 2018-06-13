from FlaskServer.db import db
from sqlalchemy.orm import relationship
from FlaskServer.yogaclasses.models.abonement import *
from sqlalchemy.orm import relationship, backref


class StudentModel(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))

    abonementtypeid = db.Column(db.Integer, db.ForeignKey('abonements.id'))
    abonements = db.relationship('AbonementModel')

    #abons = db.relationship('AbonementModel', lazy='select', backref=db.backref('abonements', lazy='joined'))

    #lessonattendances = db.relationship('LesssonAttendanceModel', backref = 'students', cascade = 'all, delete-orphan', lazy = 'dynamic')
    lessonattendances = db.relationship('LesssonAttendanceModel', back_populates="lessonattendance")

    abonementstartdate = db.Column(db.String(80))
    active = db.Column(db.Integer)

    def __init__(self, username, password, firstname, lastname, abonementtypeid, abonementstartdate, active):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname      
        self.abonementtypeid = abonementtypeid
        self.abonementstartdate = abonementstartdate      
        self.active = active

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    def json(self):
        return {'username': self.username, 'password': self.password, 
                'firstname': self.firstname, 'lastname': self.lastname, 
                'countlessonattendances': len([la for la in self.lessonattendances]),
                'lessonattendances': [la.json() for la in self.lessonattendances],
                'abonementstartdate': self.abonementstartdate, 'active': self.active }

    def jsonAbonements(self):
        return {'abonements':  self.query(StudentModel).join(StudentModel.abonementstype).all()[0].name}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()



