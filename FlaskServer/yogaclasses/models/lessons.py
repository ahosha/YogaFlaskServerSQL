from FlaskServer.db import db

class LesssonModel(db.Model):
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    teacherid = db.Column(db.Integer)
    date = db.Column(db.String(80))
    time = db.Column(db.String(80))
    lessontype = db.Column(db.String(80))
    lessonattendances = db.relationship('LesssonAttendanceModel', backref = 'lessons', cascade = 'all, delete-orphan', lazy = 'dynamic')  

    def __init__(self, name, teacherid, date, time, lessontype):
        self.name = name
        self.teacherid = teacherid
        self.date = date
        self.time = time      
        self.lessontype = lessontype

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'name': self.name,'teacherid': self.teacherid,
                'date': self.date, 'time': self.time, 
                'countlessonattendances': len([la for la in self.lessonattendances]),
                'lessonattendances': [la.json() for la in self.lessonattendances],
                'lessontype': self.lessontype}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(date=date).first()

    @classmethod
    def find_by_teacherid(cls, teacherid):
        return cls.query.filter_by(id=teacherid).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_lessontype(cls, lessontype):
        return cls.query.filter_by(id=lessontype).first()



