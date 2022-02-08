from unittest.mock import patch

from test.BaseCase import BaseCase


class TestResetPassword(BaseCase):

    @BaseCase.login
    @BaseCase.grant_access("/account/reset_password")
    def test_ok(self, token):
        payload = {
            "new_password": "MyNewPass1!"
        }

        response = self.application.post('/account/reset_password',
                                         headers=self.get_standard_post_header(token),
                                         json=payload)

        self.assertEqual(200, response.status_code)

    @BaseCase.login
    @BaseCase.grant_access("/account/reset_password")
    def test_password_with_wrong_format(self, token):
        payload = {
            "new_password": "MyNewPass"
        }

        response = self.application.post('/account/reset_password',
                                         headers=self.get_standard_post_header(token),
                                         json=payload)

        self.assertEqual("422 The new password does not have the right format", response.status)

    @BaseCase.login
    @patch('db.db.DB.get')
    def test_user_not_found(self, mock_get, token):
        mock_get.return_value = []

        payload = {
            "new_password": "MyNewPass1!"
        }

        response = self.application.post('/account/reset_password',
                                         headers=self.get_standard_post_header(token),
                                         json=payload)

        self.assertEqual("401 The user has not been found", response.status)
