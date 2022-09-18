import os
import sys

sys.path.append(os.getcwd())

import logging
from page.login import LoginPage
from playwright.sync_api import Page, Request, Route, ConsoleMessage, Locator


class App:
    def __init__(self, page: Page):
        self.page = page

        self.login_page = LoginPage(page)

        def console_handler(message: ConsoleMessage):
            if message.type == "error":
                logging.error(f"page: {self.page.url}, console error: {message.text}")

        self.page.on("console", console_handler)

    def go(self):
        self.page.goto("/")
        self.page.wait_for_load_state()

    def show_logo(self) -> Locator:
        return self.page.locator("img[alt='letcode']")

    def show_menu(self):
        return self.page.locator(".is-uppercase").all_text_contents()

    def click_signout(self):
        self.page.click("text=Sign out")

    def show_error(self):
        return self.page.text_content(".toast-error")

    def show_info(self):
        return self.page.text_content(".toast-info")
