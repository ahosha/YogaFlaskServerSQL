from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import jsonify
from FlaskServer.yogaclasses.models.students import StudentModel    

class Student(Resource):

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
    parser.add_argument('abonementtypeid',
        required=True,
        help=parser_argument_error
    )
    parser.add_argument('abonementstartdate',
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
        student = StudentModel.find_by_username(username)
        if student:
            resp = jsonify(student.json())
            resp.status_code = 200
            return resp
        else:
            message = {'message': "student with username '{}' not found.".format(username)}
            resp = jsonify(message)
            resp.status_code = 404
            return resp



    @jwt_required()
    def post(self, username):
        if StudentModel.find_by_username(username):
            return {'message': "student with username '{}' already exists.".format(username)}, 400

        data = Student.parser.parse_args()

        student = StudentModel(username,  data['password'], data['firstname'], data['lastname'], data['abonementtypeid'], data['abonementstartdate'], data['active'])

        try:
            student.save_to_db()
        except:
            message = {'message': 'An error occurred inserting the student.'}
            resp = jsonify(message)
            resp.status_code = 500
            return resp

        return student.json(), 201

    @jwt_required()
    def delete(self, username):
        item = ItemModel.find_by_username(username)
        if item:
            item.delete_from_db()

        return {'message': 'student {} was deleted'.format()}

    @jwt_required()
    def put(self, username):
        data = Student.parser.parse_args()

        student = StudentModel.find_by_username(name)

        if student:
            student.password = data['password']
            student.firstname = data['firstname']
            student.lastname = data['lastname']
            student.location = data['abonementtypeid']
            student.location = data['abonementstartdate']
            student.active = data['active']

        else:
            student = StudentModel(name, data['password'], data['firstname'], data['lastname'], data['abonementtypeid'], data['abonementstartdate'], data['active'])

        student.save_to_db()

        return student.json()

class StudentsList(Resource):
    def get(self):
        return {'students': list(map(lambda x: x.json(), StudentModel.query.all()))}
