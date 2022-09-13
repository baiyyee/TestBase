import os
import sys

sys.path.append(os.getcwd())

import json
import pytest
import allure
from config import apis
from pathlib import Path
from WeTest.util.api import API
from config.const import TIMEOUT
from WeTest.util.client import DataBase
from WeTest.util import provider, compare


@allure.epic("File Management")
@pytest.mark.p0
@pytest.mark.api
@pytest.mark.run(order=1)
class TestFileManagement:

    file = {}

    path = "data/api/testdata_file.xlsx"
    testdata_file = provider.read_excel_to_dict(path, "file")

    @allure.story("Upload File")
    @pytest.mark.timeout(TIMEOUT)
    @pytest.mark.dependency(name="test_upload_file")
    @pytest.mark.parametrize("testdata", testdata_file, ids=lambda data: "[{tc_id}: {tc_desc}]".format(**data))
    def test_upload_file(self, api: API, resource, testdata):
        """Verify Upload File Success"""

        path = apis.FILE_UPLOAD

        status_code = int(testdata["expect_code"])

        paths = [path.strip() for path in testdata["path"].split(",")]

        response = api.upload(path, paths)

        assert response.status_code == status_code

        response = response.json()
        assert len(response) == len(paths)

        if status_code == 200:
            file_info = {file["id"]: file["name"] for file in response}

            for file in response:
                self.file["id"] = file["id"]

                assert file["creator"] == resource["user_id"]
                assert compare.campare_file(f"server/{file['path']}", f"data/api/{file_info[file['id']]}")
        else:
            assert response == json.loads(testdata["expect_response"])

    @allure.story("Get Specific File")
    @pytest.mark.timeout(TIMEOUT)
    @pytest.mark.dependency(depends=["test_upload_file"])
    def test_get_specific_file(self, api: API, sqlite: DataBase):
        """Verify Get Specific File Success"""

        path = apis.FILE_SPECIFIC
        path = path.format(id=self.file.get("id"))

        response = api.request("GET", path)

        assert response.status_code == 200

        response = response.json()
        response["created"] = response["created"].replace("T", " ")

        sql = "select id,name,type,path,creator,created from file where id='{}'".format(self.file.get("id"))
        expect = sqlite.query_to_dict(sql)[0]

        assert compare.campare_dict(response, expect) == []

    @allure.story("Download File")
    @pytest.mark.timeout(TIMEOUT)
    # @pytest.mark.dependency(depends=["test_upload_file"])
    def test_get_download_file(self, api: API, sqlite: DataBase, tmp_path: Path):
        """Verify Download File Success"""

        path = apis.FILE_DOWNLOAD
        path = path.format(id=self.file.get("id"))

        path = api.download(path, str(tmp_path))

        sql = "select path from file where id='{}'".format(self.file.get("id"))
        expect = sqlite.query_to_dict(sql)[0]

        assert compare.campare_file(path, f"server/{expect['path']}")

    @allure.story("Get Files")
    @pytest.mark.timeout(TIMEOUT)
    @pytest.mark.dependency(depends=["test_upload_file"])
    @pytest.mark.parametrize("testdata", [(0, 10)], ids=lambda data: "[offset:{}__limit:{}]".format(data[0], data[1]))
    def test_get_files(self, api: API, sqlite: DataBase, resource, testdata):
        """Verify Get All Files Success"""

        path = apis.FILE
        params = {"offset": testdata[0], "limit": testdata[1]}
        response = api.request("GET", path, params=params)

        assert response.status_code == 200
        response = response.json()

        sql = "select id,name,type,path,creator,created from file limit {},{}".format(testdata[0], testdata[1])
        expect = sqlite.query_to_dict(sql)

        expect = [{**_, **{"email": resource["user_email"]}} for _ in expect]

        assert len(response) == len(expect)

        for i in range(len(response)):
            response[i]["created"] = response[i]["created"].replace("T", " ")
            assert compare.campare_dict(response[i], expect[i]) == []

    @allure.story("Delete File")
    @pytest.mark.timeout(TIMEOUT)
    @pytest.mark.dependency(depends=["test_upload_file"])
    def test_get_delete_file(self, api: API):
        """Verify Delete File Success"""

        path = apis.FILE_SPECIFIC
        path = path.format(id=self.file.get("id"))

        response = api.request("DELETE", path)

        assert response.status_code == 200
        assert response.json() == {"detail": "success"}
