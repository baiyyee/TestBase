import os
import sys

sys.path.append(os.getcwd())

import allure
import pytest
from page.app import App
from WeTest.util import path
from pytest import FixtureRequest
from playwright.sync_api import BrowserContext


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(context: BrowserContext, request: FixtureRequest):

    yield context

    # If requst.node is missing rep_call, then some error happened during execution
    # that prevented teardown, but should still be counted as a failure
    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else True

    if failed:
        for arg in request.node.funcargs.values():
            if isinstance(arg, App):
                allure.attach(body=arg.page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)


def pytest_addoption(parser):
    parser.addini("base_url", help="base url of site under test", default="https://letcode.in")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, user_info):

    # https://playwright.dev/python/docs/api/class-browser#browser-new-context

    # browser_context_args.update({"record_har_path": "config/record.har", "record_har_url_filter": "**/**"})
    # browser_context_args.update({"http_credentials": {"username": "bill", "password": "pa55w0rd"}})
    # browser_context_args.update({"proxy": {"server": "http://myproxy.com:3128"}})
    # browser_context_args.update({"color_scheme": "dark"})
    # browser_context_args.update({"user_agent": 'My user agent'})
    # browser_context_args.update(playwright.devices['iPhone 12'])
    # browser_context_args.update({"viewport": {"width": 1920, "height": 1080}})
    # browser_context_args.update({"locale"="de-DE", "timezone_id"="Europe/Berlin"})
    # browser_context_args.update({"permissions": ["notifications"]})
    # browser_context_args.update({"geolocation": {"longitude": 48.858455, "latitude": 2.294474}, "permissions": ["geolocation"]})
    # browser_context_args.grant_permissions(['notifications'], origin='https://skype.com')
    # browser_context_args.clear_permissions()

    storage_state = f"config/storage_{user_info['username']}.json"
    if path.is_exists(storage_state):
        browser_context_args.update({"storage_state": storage_state})

    return browser_context_args


@pytest.fixture
def app(page):
    app = App(page)
    return app
