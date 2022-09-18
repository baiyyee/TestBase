import os
import sys

sys.path.append(os.getcwd())

from config import urls
from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def go(self):
        self.page.goto(urls.LOGIN_PAGE)
        self.page.wait_for_load_state()

    def fill_email(self, username):
        self.page.fill("input[name='email']", username)

    def fill_password(self, password):
        self.page.fill("input[name='password']", password)

    def click_login(self):
        self.page.click("text=LOGIN")
        self.page.wait_for_load_state()

    def click_forget_pwd(self):
        self.page.click(".is-light")
