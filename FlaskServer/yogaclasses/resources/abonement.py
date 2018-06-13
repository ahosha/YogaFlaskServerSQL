from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import jsonify
from FlaskServer.yogaclasses.models.abonement import AbonementModel    

class Abonement(Resource):

    parser_argument_error = "This field cannot be left blank!" 

    parser = reqparse.RequestParser()


    parser.add_argument('duration',
        required=True,
        help=parser_argument_error
    )
    parser.add_argument('price',
        required=True,
        help=parser_argument_error
    )


    @jwt_required()
    def get(self, name):
        abonement = AbonementModel.find_by_name(name)
        if abonement:
            resp = jsonify(abonement.json())
            resp.status_code = 200
            return resp
        else:
            message = {'message': "abonement with name '{}' not found.".format(name)}
            resp = jsonify(message)
            resp.status_code = 404
            return resp




    @jwt_required()
    def post(self, name):
        if AbonementModel.find_by_name(name):
            return {'message': "abonenment with name '{}' already exists.".format(name)}, 400

        data = Abonement.parser.parse_args()

        abonement = AbonementModel(name,  data['duration'], data['price'])

        try:
            abonement.save_to_db()
        except:
            message = {'message': 'An error occurred inserting the abonement.'}
            resp = jsonify(message)
            resp.status_code = 500
            return resp

        return abonement.json(), 201

    @jwt_required()
    def delete(self, name):
        item = AbonementModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'student {} was deleted'.format()}

    @jwt_required()
    def put(self, name):
        data = Abonement.parser.parse_args()

        abonement = AbonementModel.find_by_name(name)

        if abonement:
            abonement.name = data['name']
            abonement.duration = data['duration']
            abonement.price = data['price']


        else:
            abonement = AbonementModel(name, data['duration'], data['price'])

        abonement.save_to_db()

        return abonement.json()

class AbonementsList(Resource):
    def get(self):
        return {'abonement': list(map(lambda x: x.json(), AbonementModel.query.all()))}
