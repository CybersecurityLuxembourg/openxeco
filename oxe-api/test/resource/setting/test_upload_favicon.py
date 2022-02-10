import base64
import os
from unittest.mock import patch

from test.BaseCase import BaseCase


class TestUploadFavicon(BaseCase):

    @BaseCase.login
    @BaseCase.grant_access("/setting/upload_favicon")
    @patch('resource.setting.upload_favicon.IMAGE_FOLDER', os.path.join(os.path.dirname(os.path.realpath(__file__)),
           "test_upload_favicon"))
    def test_ok(self, token):

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_upload_favicon", "original_favicon.ico")
        target_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_upload_favicon", "favicon.ico")

        if os.path.exists(target_path):
            os.remove(target_path)

        f = open(path, 'rb')
        data = base64.b64encode(f.read()).decode("utf-8")

        payload = {"image": data}

        f.close()

        response = self.application.post('/setting/upload_favicon',
                                         headers=self.get_standard_post_header(token),
                                         json=payload)

        self.assertEqual(200, response.status_code)
        self.assertTrue(os.path.exists(target_path))
        os.remove(target_path)

    @BaseCase.login
    @BaseCase.grant_access("/setting/upload_favicon")
    @patch('resource.setting.upload_favicon.IMAGE_FOLDER', os.path.join(os.path.dirname(os.path.realpath(__file__)),
           "test_upload_favicon"))
    def test_ko_wrong_format(self, token):

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_upload_favicon", "original_image.png")
        target_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_upload_favicon", "favicon.ico")

        if os.path.exists(target_path):
            os.remove(target_path)

        f = open(path, 'rb')
        data = base64.b64encode(f.read()).decode("utf-8")

        payload = {"image": data}

        f.close()

        response = self.application.post('/setting/upload_favicon',
                                         headers=self.get_standard_post_header(token),
                                         json=payload)

        self.assertEqual("422 Wrong image format. Must be an ICO file", response.status)
        self.assertFalse(os.path.exists(target_path))

    @BaseCase.login
    @BaseCase.grant_access("/setting/upload_favicon")
    @patch('resource.setting.upload_favicon.IMAGE_FOLDER', os.path.join(os.path.dirname(os.path.realpath(__file__)),
           "test_upload_favicon"))
    def test_ko_file_exception(self, token):

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_upload_favicon", "original_image.png")
        target_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_upload_favicon", "favicon.ico")

        payload = {"image": "FAKE FILE"}

        response = self.application.post('/setting/upload_favicon',
                                         headers=self.get_standard_post_header(token),
                                         json=payload)

        self.assertEqual("422 Impossible to read the image", response.status)
        self.assertFalse(os.path.exists(target_path))
