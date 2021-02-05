from flask_restful import Resource
from flask_jwt_extended import jwt_required
from utils.serializer import Serializer
from utils.catch_exception import catch_exception
from utils.log_request import log_request


class GetAllAddresses(Resource):

    def __init__(self, db):
        self.db = db

    @log_request
    @catch_exception
    @jwt_required
    def get(self):

        data = self.db.get(self.db.tables["Company_Address"])
        data = Serializer.serialize(data, self.db.tables["Company_Address"])

        return data, "200 "