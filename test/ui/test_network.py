import json
import logging
import pytest
from playwright.sync_api import Playwright, Page, Route, Request


class TestNetwork:
    def test_abort(self, page: Page):

        page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())
        page.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())

        page.goto("https://www.baidu.com/")

    def test_update_request(self, page: Page):

        # Delete header
        def handle_route(route):
            headers = route.request.headers
            del headers["x-secret"]
            route.continue_(headers=headers)

        page.route("**/*", handle_route)

        # Continue requests as POST.
        page.route("**/*", lambda route: route.continue_(method="POST"))

        page.goto("https://www.baidu.com/")

    def test_update_response(self, page: Page):

        payload = {
            "country": "中国",
            "queryIp": "1.15.0.0",
            "city": "北京",
            "ip": "1.15.0.0",
            "region": "北京",
            "country_id": "CN",
        }

        body = json.dumps(payload, ensure_ascii=False)

        page.route(
            "**/outGetIpInfo*",
            lambda route, request: route.fulfill(status=200, content_type="application/json; charset=utf-8", body=body),
        )

        page.goto("https://ip.taobao.com/outGetIpInfo?ip=1.15.0.0&accessKey=alibaba-inc")

        body = json.loads(page.locator("body").text_content())
        logging.info(f"The Intercept Response: {body}")

        assert body == payload

        page.unroute("**/outGetIpInfo*")
        page.goto("https://ip.taobao.com/outGetIpInfo?ip=1.15.0.0&accessKey=alibaba-inc")
        logging.info(f"The Original  Response: {page.locator('body').text_content()}")

    def test_record_and_replay(self, page: Page):

        # Note: update=True for real test used; update=False will replay the exists har file (it's work even server down or offline)
        page.route_from_har("tmp/record.har", update=True)

        page.goto("https://ip.taobao.com/outGetIpInfo?ip=1.15.0.0&accessKey=alibaba-inc")
        logging.info(f"Response: {page.locator('body').text_content()}")

    def test_events(self, page: Page):

        page.on("request", lambda request: logging.info(">> {} {}".format(request.method, request.url)))
        page.on("response", lambda response: logging.info("<< {} {}".format(response.status, response.url)))
        page.goto("https://ip.taobao.com/outGetIpInfo?ip=1.15.0.0&accessKey=alibaba-inc")

    def test_WebSockets(self, page: Page):
        pass
