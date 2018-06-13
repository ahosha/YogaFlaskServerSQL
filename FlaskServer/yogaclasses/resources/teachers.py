from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import jsonify
from FlaskServer.yogaclasses.models.teachers import TeacherModel    

class Teacher(Resource):

    parser_argument_error = "This field cannot be left blank!" 

    parser = reqparse.RequestParser()

    parser.add_argument('password',
        required=True,
        help=parser_argument_error
    )
    parser.add_argument('firstname',
        required=True,
        help=parser_argument_error
    )
    parser.add_argument('lastname',
        required=True,
        help=parser_argument_error
    )
    parser.add_argument('location',
        required=True,
        help=parser_argument_error
    )
    parser.add_argument('active',
        type=int,
        required=True,
        help=parser_argument_error
    )



    @jwt_required()
    def get(self, username):
        teacher = TeacherModel.find_by_username(username)
        if teacher:
            resp = jsonify(teacher.json())
            resp.status_code = 200
            return resp
        else:
            message = {'message': "teacher with username '{}' not found.".format(username)}
            resp = jsonify(message)
            resp.status_code = 404
            return resp



    @jwt_required()
    def post(self, username):
        if TeacherModel.find_by_username(username):
            return {'message': "teacher with username '{}' already exists.".format(username)}, 400

        data = Teacher.parser.parse_args()

        teacher = TeacherModel(username,  data['password'], data['firstname'], data['lastname'], data['location'], data['active'])

        try:
            teacher.save_to_db()
        except:
            message = {'message': 'An error occurred inserting the teacher.'}
            resp = jsonify(message)
            resp.status_code = 500
            return resp

        return teacher.json(), 201

    @jwt_required()
    def delete(self, username):
        item = ItemModel.find_by_username(username)
        if item:
            item.delete_from_db()

        return {'message': 'teacher {} was deleted'.format()}

    @jwt_required()
    def put(self, username):
        data = Teacher.parser.parse_args()

        teacher = TeacherModel.find_by_username(name)

        if teacher:
            teacher.password = data['password']
            teacher.firstname = data['firstname']
            teacher.lastname = data['lastname']
            teacher.location = data['location']
            teacher.active = data['active']

        else:
            teacher = TeacherModel(name, data['password'], data['firstname'], data['lastname'], data['location'], data['active'])

        teacher.save_to_db()

        return teacher.json()

class TeachersList(Resource):
    def get(self):
        return {'teachers': list(map(lambda x: x.json(), TeacherModel.query.all()))}
