from test.BaseCase import BaseCase


class TestGetTaxonomyValueHierarchy(BaseCase):

    @BaseCase.login
    def test_ok(self, token):
        self.db.insert({"name": "CAT1"}, self.db.tables["TaxonomyCategory"])
        self.db.insert({"name": "CAT2"}, self.db.tables["TaxonomyCategory"])
        self.db.insert({"parent_category": "CAT1", "child_category": "CAT2"},
                       self.db.tables["TaxonomyCategoryHierarchy"])
        self.db.insert({"id": 1, "name": "VAL1", "category": "CAT1"}, self.db.tables["TaxonomyValue"])
        self.db.insert({"id": 2, "name": "VAL2", "category": "CAT2"}, self.db.tables["TaxonomyValue"])
        self.db.insert({"parent_value": 1, "child_value": 2}, self.db.tables["TaxonomyValueHierarchy"])

        response = self.application.get(
            '/taxonomy/get_taxonomy_value_hierarchy',
            headers=self.get_standard_header(token)
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual([{'parent_value': 1, 'child_value': 2}], response.json)
