import datetime

from flask import make_response, request
from flask_apispec import MethodResource
from flask_apispec import doc
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_refresh_token_required
from flask_restful import Resource
from config.config import ENVIRONMENT

from decorator.catch_exception import catch_exception
from decorator.log_request import log_request


class Refresh(MethodResource, Resource):

    db = None

    def __init__(self, db):
        self.db = db

    @log_request
    @doc(tags=['account'],
         description='Request the token',
         responses={
             "200": {},
         })
    @jwt_refresh_token_required
    @catch_exception
    def post(self):

        access_token_expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=get_jwt_identity(), expires_delta=access_token_expires, fresh=False)

        response = make_response({
            "user": get_jwt_identity(),
        })

        response.set_cookie(
            "access_token_cookie",
            value=access_token,
            path="/",
            domain=None if ENVIRONMENT == "dev"
            else (request.host[len("api"):] if request.host.startswith("api") else request.host),
            secure=True,
        )

        return response
