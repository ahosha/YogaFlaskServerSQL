from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from werkzeug.contrib.cache import SimpleCache
from FlaskServer.errorhandlers import configure_error_handlers

from FlaskServer.Users.security import authenticate, identity
from FlaskServer.Users.resources.user import UserRegister
from FlaskServer.Users.resources.item import Item, ItemList
from FlaskServer.Users.resources.store import Store, StoreList
import FlaskServer.consts as consts 
import FlaskServer.setting as setting
from FlaskServer.db import db

from FlaskServer.yogaclasses.resources.teachers import Teacher, TeachersList
from FlaskServer.yogaclasses.resources.students import Student, StudentsList
from FlaskServer.yogaclasses.resources.abonement import Abonement, AbonementsList
from FlaskServer.yogaclasses.resources.lesson import Lesson, LessonsList
from FlaskServer.yogaclasses.resources.lessonsattendance import LesssonAttendance, LesssonAttendancesList

app = Flask(__name__)

app.cache = SimpleCache()
app.config['SQLALCHEMY_DATABASE_URI'] = setting.DB_CONNECTION_STR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = setting.SECURITY_KEY

# Error handlers for 400, 404, 500 codes
configure_error_handlers(app)

# JWT
jwt = JWT(app, authenticate, identity)

api = Api(app)

@app.before_first_request
def create_tables():

    db.create_all()


#store api
api.add_resource(Store, consts.STORE_URL)
api.add_resource(StoreList, consts.STORE_LIST_URL)
api.add_resource(Item, consts.ITEM_URL)
api.add_resource(ItemList, consts.ITEMS_URL)
api.add_resource(UserRegister, consts.USER_REGISTER_URL)

#yoga classes api
api.add_resource(TeachersList, consts.TEACHERS_URL)
api.add_resource(Teacher, consts.TEACHER_URL)
api.add_resource(StudentsList, consts.STUDENTS_URL)
api.add_resource(Student, consts.STUDENT_URL)
api.add_resource(AbonementsList, consts.ABONEMENTS_URL)
api.add_resource(Abonement, consts.ABONEMENT_URL)
api.add_resource(LessonsList, consts.LESSONS_URL)
api.add_resource(Lesson, consts.LESSON_URL)
api.add_resource(LesssonAttendancesList, consts.LESSONATTENDANCELIST_URL)
api.add_resource(LesssonAttendance, consts.LESSONATTENDANCE_URL)








