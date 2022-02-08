from test.BaseCase import BaseCase


class TestGetGlobalAnalytics(BaseCase):

    @BaseCase.login
    def test_ok(self, token):
        self.db.insert({"name": "ECOSYSTEM ROLE"}, self.db.tables["TaxonomyCategory"])
        self.db.insert({"id": 1, "name": "ACTOR", "category": "ECOSYSTEM ROLE"}, self.db.tables["TaxonomyValue"])

        response = self.application.get('/public/get_public_taxonomy',
                                        headers=self.get_standard_header(token))

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json, {
            "categories": [
                {
                    'name': 'ECOSYSTEM ROLE',
                    'accepted_article_types': None,
                    'active_on_articles': 0,
                    'active_on_companies': 0,
                    'is_standard': 0,
                }
            ],
            "values": [
                {'category': 'ECOSYSTEM ROLE', 'id': 1, 'name': 'ACTOR'}
            ],
            "category_hierarchy": [],
            "value_hierarchy": []
        })
