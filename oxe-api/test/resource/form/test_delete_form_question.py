from test.BaseCase import BaseCase


class TestDeleteFormQuestion(BaseCase):

    @BaseCase.login
    @BaseCase.grant_access("/form/delete_form_question")
    def test_ok(self, token):
        form = self.db.insert({"name": "FORM1"}, self.db.tables["Form"])
        question = self.db.insert({"form_id": form.id, "position": 1}, self.db.tables["FormQuestion"])

        payload = {"id": question.id}

        response = self.application.post('/form/delete_form_question',
                                         headers=self.get_standard_post_header(token),
                                         json=payload)

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.db.get_count(self.db.tables["FormQuestion"]), 0)

    @BaseCase.login
    @BaseCase.grant_access("/form/delete_form_question")
    def test_ok_with_answers(self, token):
        form = self.db.insert({"name": "FORM1"}, self.db.tables["Form"])
        question = self.db.insert({"form_id": form.id, "position": 1}, self.db.tables["FormQuestion"])
        self.db.insert({
            "form_question_id": question.id,
            "user_id": 1,
        }, self.db.tables["FormAnswer"])

        payload = {"id": question.id}

        response = self.application.post('/form/delete_form_question',
                                         headers=self.get_standard_post_header(token),
                                         json=payload)

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.db.get_count(self.db.tables["Form"]), 1)
        self.assertEqual(self.db.get_count(self.db.tables["FormQuestion"]), 0)
        self.assertEqual(self.db.get_count(self.db.tables["FormAnswer"]), 0)

    @BaseCase.login
    @BaseCase.grant_access("/form/delete_form_question")
    def test_delete_unexisting(self, token):
        payload = {"id": 42}

        response = self.application.post('/form/delete_form_question',
                                         headers=self.get_standard_post_header(token),
                                         json=payload)

        self.assertEqual("422 Object not found", response.status)
