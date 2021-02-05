from flask_restful import Resource
from db.db import DB
from utils.catch_exception import catch_exception
from utils.serializer import Serializer


class GetPublicAnalytics(Resource):

    def __init__(self, db: DB):
        self.db = db

    @catch_exception
    def get(self):

        tc = self.db.tables["TaxonomyCategory"]
        tch = self.db.tables["TaxonomyCategoryHierarchy"]
        ta = self.db.tables["TaxonomyAssignment"]
        tvh = self.db.tables["TaxonomyValueHierarchy"]
        tv = self.db.tables["TaxonomyValue"]

        data = {
            "workforces": Serializer.serialize(self.db.get_latest_workforce(), self.db.tables["Workforce"]),
            "taxonomy_categories": Serializer.serialize(self.db.get(tc), tc),
            "taxonomy_category_hierarchy": Serializer.serialize(self.db.get(tch), tch),
            "taxonomy_values": Serializer.serialize(self.db.get(tv), tv),
            "taxonomy_value_hierarchy": Serializer.serialize(self.db.get(tvh), tvh),
            "taxonomy_assignments": Serializer.serialize(self.db.get(ta), ta),
        }

        return data, "200 "