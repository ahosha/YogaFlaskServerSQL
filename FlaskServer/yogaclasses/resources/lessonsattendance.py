from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import jsonify
from FlaskServer.yogaclasses.models.lessonsattendance import LesssonAttendanceModel    

class LesssonAttendance(Resource):

    parser_argument_error = "This field cannot be left blank!" 

    parser = reqparse.RequestParser()

    parser.add_argument('lessonid',
        required=True,
        help=parser_argument_error
    )
    parser.add_argument('studentid',
        required=True,
        help=parser_argument_error
    )



    @jwt_required()
    def get(self, lessonid):
        #data = LesssonAttendance.parser.parse_args()
        attendance = LesssonAttendanceModel.find_by_lessonid(lessonid)
        if attendance:
            resp = jsonify(attendance.json())
            resp.status_code = 200
            return resp
        else:
            message = {'message': "attendance with lessonid '{}' not found.".format(lessonid)}
            resp = jsonify(message)
            resp.status_code = 404
            return resp




    @jwt_required()
    def post(self, lessonid):
        data = LesssonAttendance.parser.parse_args()
        if LesssonAttendanceModel.find_by_lessonid_studentid(data['lessonid'],data['studentid']):
            return {'message': "teacher with attendance '{0} {1}' already exists.".format(data['lessonid'],data['studentid'])}, 400

        attendance = LesssonAttendanceModel(data['lessonid'], data['studentid'])

        try:
            attendance.save_to_db()
        except:
            message = {'message': 'An error occurred inserting the attendance.'}
            resp = jsonify(message)
            resp.status_code = 500
            return resp

        return attendance.json(), 201

    @jwt_required()
    def delete(self, lessonid,studentid):
        item = LesssonAttendanceModel.find_by_lessonid_studentid(lessonid,studentid)
        if item:
            item.delete_from_db()

        return {'message': 'attendance {} was deleted'.format()}

    @jwt_required()
    def put(self,  lessonid,studentid):
        data = LesssonAttendance.parser.parse_args()

        attendance = LesssonAttendanceModel.find_by_lessonid_studentid(lessonid,studentid)

        if attendance:
            attendance.lessonid = data['lessonid']
            attendance.studentid = data['studentid']

        else:
            attendance = LesssonAttendanceModel(data['lessonid'], data['studentid'])

        attendance.save_to_db()

        return attendance.json()

class LesssonAttendancesList(Resource):
    def get(self):
        return {'attendances': list(map(lambda x: x.json(), LesssonAttendanceModel.query.all()))}
