import base64
import logging
from io import BytesIO
from pathlib import Path
from WeTest.util import compare
from PIL import Image, ImageDraw
from playwright.sync_api import Page


def test_screenshots(page: Page, tmp_path: Path):

    page.goto("https://www.baidu.com/")

    screenshot_bytes = page.screenshot()
    logging.info(base64.b64encode(screenshot_bytes).decode())

    path = str(tmp_path / "fullpage.png")
    page.screenshot(path=path, full_page=True)
    logging.info(f"Save to: {path}")

    path = str(tmp_path / "element.png")
    page.locator("#s_lg_img").screenshot(path=path)
    logging.info(f"Save to: {path}")


def test_campare_pixel(page: Page):

    page.goto("https://www.baidu.com/")

    screenshot_bytes = page.screenshot()
    screenshot_bytes = BytesIO(screenshot_bytes)

    img = Image.open(screenshot_bytes)
    draw = ImageDraw.Draw(img)
    draw.text((28, 26), "Baidu", fill=(0, 0, 0))
    stream = BytesIO()
    img.save(stream, "PNG")

    assert compare.campre_image(screenshot_bytes, stream, output="tmp/diff.png") == False
