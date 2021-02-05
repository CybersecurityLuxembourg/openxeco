from flask_restful import Resource
from flask_jwt_extended import jwt_required
from utils.catch_exception import catch_exception
import os
from utils.log_request import log_request


class GetMailContent(Resource):

    def __init__(self, db):
        self.db = db

    @log_request
    @catch_exception
    @jwt_required
    def get(self, name):

        if name not in ["new_account", "reset_password"]:
            return "", "404 This mail template does not exist"
        else:
            with open(os.path.join(os.path.dirname(__file__), "..", "..", "template", f"{name}.html"), "r") as f:
                data = f.read()

        return data, "200 "