import os
import sys

sys.path.append(os.getcwd())

import allure
import pytest
from page.app import App


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    result = outcome.get_result()
    setattr(item, f"result_{result.when}", result)


# @pytest.fixture(scope="function", autouse=True)
# def take_screenshot(request):

#     yield

#     if request.node.rep_call.failed:
#         for arg in request.node.funcargs.values():
#             if isinstance(arg, App):
#                 allure.attach(body=arg.page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)


def pytest_addoption(parser):
    parser.addini("base_url", help="base url of site under test", default="https://letcode.in")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):

    return {
        **browser_context_args,
        "storage_state": "config/storage.json",
    }


@pytest.fixture
def app(page):

    app = App(page)
    return app
