import logging
from playwright.sync_api import Page


class TestAPI:
    def test_page_api(self, page: Page):

        response = page.request.get("/")
        assert response.ok
        logging.info(response.text())
