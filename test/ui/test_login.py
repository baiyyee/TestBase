import os
import sys

sys.path.append(os.getcwd())

import pytest
from page.app import App
from WeTest.util import provider


class TestLogin:

    path = "data/ui/testdata_login.xlsx"
    testdata_login = provider.read_excel_to_dict(path, "login")

    # @pytest.fixture
    # def browser_context_args(self, browser_context_args):
    #     browser_context_args.pop("storage_state")
    #     return {**browser_context_args}

    @pytest.mark.bvt
    @pytest.mark.p0
    @pytest.mark.ui
    @pytest.mark.parametrize("testdata", testdata_login, ids=lambda data: "[{tc_id}: {tc_desc}]".format(**data))
    def test_login(self, context, app: App, testdata):

        app.login_page.go()
        app.login_page.fill_email(testdata["email"])
        app.login_page.fill_password(testdata["password"])
        app.login_page.click_login()

        if "合法-" in testdata["tc_desc"]:
            assert testdata["expect_response"] in app.show_info()

            # Verify logout success
            app.click_signout()
            assert "Bye! See you soon :)" in app.show_info()

            # context.storage_state(path="config/storage.json")

        elif "非法-" in testdata["tc_desc"]:
            assert testdata["expect_response"] in app.show_error()
