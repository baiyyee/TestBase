import os
import sys

sys.path.append(os.getcwd())

import pytest
from page.app import App
from playwright.sync_api import expect


class TestApp:
    @pytest.mark.bvt
    @pytest.mark.p0
    @pytest.mark.ui
    @pytest.mark.skip(reason="No visual comparisons for now")
    def test_logo(self, app: App, assert_snapshot):

        app.go()
        app.show_logo().screenshot()
        assert_snapshot(app.show_logo().screenshot())
        expect(app.show_logo().screenshot())

    @pytest.mark.bvt
    @pytest.mark.p0
    @pytest.mark.ui
    def test_menu(self, app: App):

        app.go()
        assert app.show_menu() == ["Work Space", "Courses", "Product"]
