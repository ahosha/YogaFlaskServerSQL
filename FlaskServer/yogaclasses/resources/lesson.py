from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import jsonify
from FlaskServer.yogaclasses.models.lessons import LesssonModel    

class Lesson(Resource):

    parser_argument_error = "This field cannot be left blank!" 

    parser = reqparse.RequestParser()

    parser.add_argument('teacherid',
        required=True,
        help=parser_argument_error
    )
    parser.add_argument('date',
        required=True,
        help=parser_argument_error
    )
    parser.add_argument('time',
        required=True,
        help=parser_argument_error
    )
    parser.add_argument('lessontype',
        required=True,
        help=parser_argument_error
    )


    @jwt_required()
    def get(self, name):
        lesson = LesssonModel.find_by_name(name)
        if lesson:
            resp = jsonify(lesson.json())
            resp.status_code = 200
            return resp
        else:
            message = {'message': "lesson with name '{}' not found.".format(name)}
            resp = jsonify(message)
            resp.status_code = 404
            return resp




    @jwt_required()
    def post(self, name):
        if LesssonModel.find_by_name(name):
            return {'message': "lesson with name '{}' already exists.".format(name)}, 400

        data = Lesson.parser.parse_args()

        lesson = LesssonModel(name,  data['teacherid'], data['date'], data['time'], data['lessontype'])

        try:
            lesson.save_to_db()
        except:
            message = {'message': 'An error occurred inserting the lesson.'}
            resp = jsonify(message)
            resp.status_code = 500
            return resp

        return lesson.json(), 201

    @jwt_required()
    def delete(self, username):
        item = LesssonModel.find_by_username(username)
        if item:
            item.delete_from_db()

        return {'message': 'lessons {} was deleted'.format()}

    @jwt_required()
    def put(self, name):
        data = Lessson.parser.parse_args()

        lesson = LesssonModel.find_by_name(name)

        if lesson:
            lesson.teacherid = data['teacherid']
            lesson.date = data['date']
            lesson.time = data['time']
            lesson.lessontype = data['lessontype']
 
        else:
            lesson = LesssonModel(name, data['teacherid'], data['date'], data['time'], data['lessontype'])

        lesson.save_to_db()

        return lesson.json()

class LessonsList(Resource):
    def get(self):
        return {'lessons': list(map(lambda x: x.json(), LesssonModel.query.all()))}
