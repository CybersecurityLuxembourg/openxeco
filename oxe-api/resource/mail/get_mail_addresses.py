from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from webargs import fields

from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access


class GetMailAddresses(MethodResource, Resource):

    def __init__(self, db):
        self.db = db

    @log_request
    @doc(tags=['mail'],
         description='Get the email addresses from the active users and the company contacts',
         responses={
             "200": {},
         })
    @use_kwargs({
        'companies': fields.List(fields.Str(), required=False),
        'taxonomies': fields.List(fields.Str(), required=False),
        'include_contacts': fields.Bool(required=False, allow_none=True, missing=True),
        'include_users': fields.Bool(required=False, allow_none=True, missing=True),
    }, location="query")
    @jwt_required
    @verify_admin_access
    @catch_exception
    def get(self, **kwargs):

        addresses = []
        companies = kwargs["companies"] if "companies" in kwargs else []
        filtered_users = None

        # Add companies related to the taxonomy

        if "taxonomies" in kwargs:
            taxonomy_companies = self.db.get_filtered_companies({"taxonomy_values": kwargs["taxonomies"]}).all()
            taxonomy_company_ids = [c.id for c in taxonomy_companies]
            companies = list(set(companies + taxonomy_company_ids))

        # Get user IDs respecting the taxonomy and company params

        if "companies" in kwargs or "taxonomies" in kwargs:
            filtered_users = self.db.get(self.db.tables["UserCompanyAssignment"], {"company_id": companies})
            filtered_users = [u.user_id for u in filtered_users]

        # Get the contact addresses

        if kwargs["include_contacts"] is True:
            filters = {"type": "EMAIL ADDRESS"}

            if "companies" in kwargs or "taxonomies" in kwargs:
                filters["company_id"] = companies

            contacts = self.db.get(
                self.db.tables["CompanyContact"],
                filters,
                ["value", "representative", "name"]
            )

            for c in contacts:
                addresses.append({
                    "source": "CONTACT OF COMPANY",
                    "email": c.value,
                    "information": c.name
                })

        # Get the user addresses

        if kwargs["include_users"] is True:
            filters = {"is_active": True}

            if filtered_users is not None:
                filters["id"] = filtered_users

            users = self.db.get(
                self.db.tables["User"],
                filters,
                ["email", "last_name", "first_name"]
            )

            for u in users:
                fullname = GetMailAddresses.build_fullname(u.first_name, u.last_name)

                addresses.append({
                    "source": "USER",
                    "email": u.email,
                    "information": fullname
                })

        return addresses, "200 "

    @staticmethod
    def build_fullname(first_name, last_name):
        fullname = None

        if first_name is not None or last_name is not None:
            fullname = ""

            if first_name is not None:
                fullname += first_name

            if last_name is not None:
                if len(fullname) > 0:
                    fullname += " "
                fullname += last_name

        return fullname
