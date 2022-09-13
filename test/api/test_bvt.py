import os
import sys

sys.path.append(os.getcwd())

import pytest
import allure
from config import apis
from WeTest.util.api import API
from WeTest.util import compare
from config.const import TIMEOUT


@allure.epic("BVT")
@pytest.mark.bvt
@pytest.mark.api
@pytest.mark.run(order=0)
class TestBVT:
    @allure.feature("User Authorization")
    @allure.story("Get User Profile")
    @pytest.mark.timeout(TIMEOUT)
    @pytest.mark.dependency(name="test_user_profile")
    def test_user_profile(self, api: API, resource):
        """Verify User Authorization Success"""

        path = apis.USER_PROFILE

        response = api.request("GET", path)

        expect = {"name": "root", "email": "root@test.com", "role": 0, "status": 1, "id": 1, "creator": 1}

        assert response.status_code == 200
        response = response.json()

        assert compare.campare_dict(response, expect) == []

        resource["user_id"] = response["id"]
        resource["user_email"] = response["email"]
