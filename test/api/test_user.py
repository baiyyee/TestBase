import os
import sys

sys.path.append(os.getcwd())

import json
import pytest
import allure
from config import apis
from WeTest.util.api import API
from config.const import TIMEOUT
from WeTest.util.client import DataBase
from WeTest.util import provider, compare


@allure.epic("User Management")
@pytest.mark.run(order=1)
@pytest.mark.p0
@pytest.mark.api
class TestUser:

    user = {}

    path = "data/api/testdata_user.xlsx"
    testdata_user_create = provider.read_excel_to_dict(path, "user")

    # Reused the same testcase, filter cases by needs
    testdata_user_edit = [
        # data for data in testdata_user_create if "-密码-" not in data["tc_desc"] or "邮箱-重名-baseline" not in data["tc_desc"]
        data
        for data in testdata_user_create
        if all([desc not in data["tc_desc"] for desc in ("-密码-", "邮箱-重名-baseline")])
    ]
    testdata_user_reset_pwd = [data for data in testdata_user_create if "-密码-" in data["tc_desc"]]

    @allure.story("Create User")
    @pytest.mark.timeout(TIMEOUT)
    @pytest.mark.dependency(name="test_create_user")
    @pytest.mark.parametrize("testdata", testdata_user_create, ids=lambda data: "[{tc_id}: {tc_desc}]".format(**data))
    def test_create_user(self, api: API, testdata):
        """Verify Create User Success"""

        path = apis.USER

        _, kw = provider.replace_macro(None, None, **testdata)

        status_code = int(kw["expect_code"])

        payload = """
        {{
            "name": "{name}",
            "email": "{email}",
            "role": "{role}",
            "status": "{status}",
            "password": "{password}"
        }}
        """.format(
            **kw
        )

        payload = json.loads(payload)

        response = api.request("POST", path, json=payload)

        assert response.status_code == status_code

        response = response.json()

        if status_code == 200:
            self.user["id"] = response["id"]

            assert response["name"] == payload["name"]
            assert response["email"] == payload["email"]
            assert response["role"] == int(payload["role"])
            assert response["status"] == int(payload["status"])
            assert response["name"] == payload["name"]
        else:
            assert response == json.loads(kw["expect_response"])

    @allure.story("Edit User")
    @pytest.mark.timeout(TIMEOUT)
    @pytest.mark.dependency(depends=["test_create_user"])
    @pytest.mark.parametrize("testdata", testdata_user_edit, ids=lambda data: "[{tc_id}: {tc_desc}]".format(**data))
    def test_edit_user(self, api: API, testdata):
        """Verify Edit User Success"""

        path = apis.USER_SPECIFIC
        path = path.format(id=self.user.get("id"))

        _, kw = provider.replace_macro(None, None, **testdata)

        status_code = int(kw["expect_code"])

        payload = """
        {{
            "name": "{name}",
            "email": "{email}",
            "role": "{role}",
            "status": "{status}"
        }}
        """.format(
            **kw
        )

        payload = json.loads(payload)

        response = api.request("PATCH", path, json=payload)

        assert response.status_code == status_code

        response = response.json()

        if status_code == 200:
            self.user["id"] = response["id"]

            assert response["name"] == payload["name"]
            assert response["email"] == payload["email"]
            assert response["role"] == int(payload["role"])
            assert response["status"] == int(payload["status"])
            assert response["name"] == payload["name"]
        else:
            assert response == json.loads(kw["expect_response"])

    @allure.story("Reset User Password")
    @pytest.mark.timeout(TIMEOUT)
    @pytest.mark.dependency(depends=["test_create_user"])
    @pytest.mark.parametrize("testdata", testdata_user_reset_pwd, ids=lambda data: "[{tc_id}: {tc_desc}]".format(**data))
    def test_reset_user_pwd(self, api: API, testdata):
        """Verify Reset User Password Success"""

        path = apis.USER_RESET_PWD
        path = path.format(id=self.user.get("id"))

        _, kw = provider.replace_macro(None, None, **testdata)

        status_code = int(kw["expect_code"])

        payload = """
        {{
            "password": "{password}"
        }}
        """.format(
            **kw
        )

        payload = json.loads(payload)

        response = api.request("PATCH", path, json=payload)

        assert response.status_code == status_code

        response = response.json()

        if status_code == 200:
            assert response == {"detail": "success"}
        else:
            assert response == json.loads(kw["expect_response"])

    @allure.story("Get Users")
    @pytest.mark.timeout(TIMEOUT)
    @pytest.mark.parametrize("testdata", [(0, 10)], ids=lambda data: "[offset:{}__limit:{}]".format(data[0], data[1]))
    def test_get_users(self, api: API, sqlite: DataBase, testdata):
        """Verify Get All Users Success"""

        path = apis.USER
        params = {"offset": testdata[0], "limit": testdata[1]}
        response = api.request("GET", path, params=params)

        assert response.status_code == 200
        response = response.json()

        sql = "select id,name,email,role,status,creator from user limit {},{}".format(testdata[0], testdata[1])
        expect = sqlite.query_to_dict(sql)

        assert len(response) == len(expect)

        for i in range(len(response)):
            assert compare.campare_dict(response[i], expect[i]) == []

    @allure.story("Get Specific User")
    @pytest.mark.timeout(TIMEOUT)
    def test_get_specific_user(self, api: API, sqlite: DataBase):
        """Verify Get Specific User Success"""

        path = apis.USER_SPECIFIC
        path = path.format(id=self.user.get("id"))

        response = api.request("GET", path)

        assert response.status_code == 200

        sql = "select id,name,email,role,status,creator from user where id={}".format(self.user.get("id"))
        expect = sqlite.query_to_dict(sql)[0]

        assert compare.campare_dict(response.json(), expect) == []

    @allure.story("Delete User")
    @pytest.mark.timeout(TIMEOUT)
    def test_get_delete_user(self, api: API):
        """Verify Delete User Success"""

        path = apis.USER_SPECIFIC
        path = path.format(id=self.user.get("id"))

        response = api.request("DELETE", path)

        assert response.status_code == 200
        assert response.json() == {"detail": "success"}
