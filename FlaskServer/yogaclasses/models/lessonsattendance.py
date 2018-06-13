from FlaskServer.db import db

class LesssonAttendanceModel(db.Model):
    __tablename__ = 'lessonattendance'
    
    id = db.Column(db.Integer, primary_key=True)
    lessonid = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable = False)
    studentid = db.Column(db.Integer, db.ForeignKey('students.id'), nullable = False)
    #lesson = db.relationship("LesssonModel", back_populates="lessons")
    student = db.relationship("StudentModel", back_populates="username")
    
    def __init__(self, lessonid, studentid):
        self.lessonid = lessonid
        self.studentid = studentid


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'lessonid': self.lessonid,'studentid': self.studentid ,
                 'student': self.student.json()
                }

    @classmethod
    def find_by_studentid(cls, studentid):
        return cls.query.filter_by(studentid=studentid).first()

    @classmethod
    def find_by_lessonid(cls, lessonid):
        return cls.query.filter_by(lessonid=lessonid).first()


    @classmethod
    def find_by_lessonid_studentid(cls, _lessonid, _studentid):
        return cls.query.filter_by(lessonid = _lessonid).first()





