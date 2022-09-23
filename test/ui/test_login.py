import os
import sys

sys.path.append(os.getcwd())

import pytest
import allure
from page.app import App
from WeTest.util import provider


@allure.epic("BVT")
@pytest.mark.bvt
@pytest.mark.api
@pytest.mark.run(order=0)
class TestLogin:

    path = "data/ui/testdata_login.xlsx"
    testdata_login = provider.read_excel_to_dict(path, "login")

    @pytest.fixture(scope="class")
    def browser_context_args(self, browser_context_args, user_info):

        # Note: With login test scenarios, should keep un-login status, so remove storage_state related here
        if "storage_state" in browser_context_args:
            browser_context_args.pop("storage_state")

        return browser_context_args

    @pytest.mark.bvt
    @pytest.mark.p0
    @pytest.mark.ui
    @pytest.mark.dependency(name="test_login")
    @pytest.mark.parametrize("testdata", testdata_login, ids=lambda data: "[{tc_id}: {tc_desc}]".format(**data))
    def test_login(self, app: App, testdata):

        app.login_page.go()
        app.login_page.fill_email(testdata["email"])
        app.login_page.fill_password(testdata["password"])
        app.login_page.click_login()

        if "合法-" in testdata["tc_desc"]:
            assert testdata["expect_response"] in app.show_info()

            # Verify logout success
            app.click_signout()
            assert "Bye! See you soon :)" in app.show_info()

        elif "非法-" in testdata["tc_desc"]:
            assert testdata["expect_response"] in app.show_error()

    @pytest.mark.bvt
    @pytest.mark.p0
    @pytest.mark.ui
    @pytest.mark.dependency(depends=["test_login"])
    def test_role(self, context, user_info, app: App):

        app.login_page.go()
        app.login_page.fill_email(user_info["email"])
        app.login_page.fill_password(user_info["password"])
        app.login_page.click_login()

        context.storage_state(path=f"config/storage_{user_info['username']}.json")
