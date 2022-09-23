import pytest
import logging
from WeTest.util import compare
from playwright.sync_api import Page, expect
from playwright._impl._browser_context import BrowserContext


def test_input(page: Page):

    page.goto("/edit")
    page.wait_for_load_state()

    page.fill("#fullName", "Huabo He")

    join = page.locator("#join")
    join.focus()
    page.keyboard.press(key="End")
    join.type(" Human")

    page.keyboard.press(key="Tab")
    assert page.get_attribute("#getMe", "value") == "ortonikc"

    # page.fill("#clearMe", "")
    page.fill("//input[@value='Koushik Chatterjee']", "")

    assert page.locator("#noEdit").is_disabled() == True
    assert page.locator("#dontwrite").is_editable() == False


def test_button(page: Page):

    page.goto("/buttons")
    page.wait_for_load_state()

    page.click("#home")
    expect(page).to_have_title("LetCode with Koushik")

    page.go_back()
    expect(page).to_have_url("https://letcode.in/buttons")

    assert compare.campare_dict(page.locator("#position").bounding_box(), {"x": 88, "y": 338, "width": 130, "height": 40}) == []

    # Get CSS properties
    # page.locator("#color").evaluate("element => {return window.getComputedStyle(element).getPropertyValue('background-color')}")
    expect(page.locator("#color")).to_have_css("background-color", "rgb(138, 77, 118)")

    expect(page.locator(".is-info")).to_be_disabled()

    # Add delay param for click and hold operation
    page.click("button:has-text('Button Hold!')", delay=3000)

    assert page.locator("h2").text_content() == "Button has been long pressed"
    expect(page.locator("h2")).to_contain_text("long pressed")


def test_select(page: Page):

    page.goto("/dropdowns")
    page.wait_for_load_state()

    fruits = page.locator("#fruits")
    fruits.select_option("0")

    expect(page.locator(".subtitle")).to_have_text("You have selected Apple")

    superheros = page.locator("#superheros")
    superheros.select_option(label=["Aquaman"], value=["ta"], index=[3])

    lang = page.locator("#lang option")
    assert lang.count() == 5
    assert lang.all_text_contents() == ["JavaScript", "Java", "Python", "Swift", "C#"]

    country = page.locator("#country")
    country.select_option(value=["India"])
    assert country.evaluate("element => element.value") == "India"


def test_alert(page: Page):

    page.goto("/alert")
    page.wait_for_load_state()

    def dialog_handler(dialog):
        logging.info(dialog.type)
        logging.info(dialog.message)
        logging.info(dialog.default_value)
        dialog.accept("Huabo He")
        # dialog.dismiss()

    # page.on("dialog", lambda dialog: dialog.accept())

    page.on("dialog", dialog_handler)
    page.click("#accept")
    page.click("#confirm")
    page.click("#prompt")

    # Note: For sweet modern alert, just use locator and click as usual will be OK
    # See: https://www.youtube.com/watch?v=jGIbyNtugKI
    page.click("#modern")

    assert page.locator("#myName").text_content() == "Your name is: Huabo He"


def test_frame(page: Page):

    page.goto("/frame")
    page.wait_for_load_state()

    first_frame = page.frame(name="firstFr")

    first_frame.fill("input[name='fname']", "Huabo He")
    first_frame.fill("input[name='lname']", "root@test.com")

    child_frames = first_frame.child_frames
    assert len(child_frames) == 4

    child_frames[0].fill("input[name='email']", "admin@test.com")

    # Frame Switch
    # Method 01:
    # first_frame.fill("input[name='fname']", "Huabo He Update")

    # Method 02:
    parent = child_frames[0].parent_frame
    parent.fill("input[name='fname']", "Huabo He Update")


def test_radio(page: Page):

    page.goto("/radio")
    page.wait_for_load_state()

    page.check(".radio >> nth=1")

    radio_2 = page.locator(".radio >> nth=2")
    radio_3 = page.locator(".radio >> nth=3")
    radio_2.check()
    assert radio_2.is_checked
    assert radio_3.is_checked() == False
    radio_3.check()
    assert radio_3.is_checked()
    assert radio_2.is_checked() == False

    assert page.locator(".radio >> nth=8").is_enabled()
    assert page.locator(".radio >> nth=9").is_enabled()
    assert page.locator(".radio >> nth=10").is_enabled() == False
    assert page.locator("text=Remember me").is_checked()

    page.locator("text=I agree to the").check()


def test_window(page: Page, context: BrowserContext):

    page.goto("/windows")
    page.wait_for_load_state()

    with context.expect_page() as new_page:
        page.click("#home")

    new_page = new_page.value
    new_page.wait_for_load_state()
    expect(new_page).to_have_title("LetCode - Testing Hub")

    # Bring the specific page tag to the front
    page.bring_to_front()
    new_page.close()

    with context.expect_page() as new_page:
        page.click("#multi")

    # Get new opened page tabs
    pages = new_page.value.context.pages
    for new_page in pages:
        new_page.wait_for_load_state()
        logging.info(new_page.title())

    # Get all opened page tabs(include the ori one)
    pages_all = page.context.pages
    for page in pages_all:
        logging.info(page.title())

    # Get all new pages (including popups) in the context
    # def handle_page(page):
    #     page.wait_for_load_state()
    #     print(page.title())

    # context.on("page", handle_page)


def test_element(page: Page):

    page.goto("/elements")
    page.wait_for_load_state()

    # page.fill("input", "ortonikc")
    page.fill("input", "baiyyee")
    page.click("#search")

    # Note: Need to wait here to get the api response, it's different with Auto-waiting (https://playwright.dev/python/docs/actionability)
    page.wait_for_selector("app-gitrepos li", timeout=5000)
    elements = page.locator("app-gitrepos li")

    logging.info(f"Repos Count: {elements.count()}")

    logging.info("=" * 50)
    logging.info(elements.all_text_contents())

    logging.info("=" * 50)
    for i in range(elements.count()):
        logging.info(elements.nth(i).inner_text())

    texts = elements.evaluate_all("list => list.map(element => element.textContent)")
    logging.info("=" * 50)
    logging.info(texts)

    assert "https://avatars.githubusercontent.com" in page.locator("figure img").get_attribute("src")


@pytest.mark.skip(reason="Not impement yet")
def test_draggable(page: Page):

    page.goto("/draggable")
    page.wait_for_load_state()

    box = page.locator("#sample-box").bounding_box()
    boundary = page.locator(".example-boundary").bounding_box()

    logging.info(box)
    logging.info(boundary)

    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.mouse.down()
    page.mouse.move(boundary["x"] + boundary["width"] / 2, boundary["y"] + boundary["height"] / 2)
    page.mouse.up()


def test_dropable(page: Page):

    page.goto("/dropable")
    page.wait_for_load_state()

    # Method 01:
    # source = page.locator("#draggable").bounding_box()
    # target = page.locator("#droppable").bounding_box()
    # page.mouse.move(source["x"] + source["width"] / 2, source["y"] + source["height"] / 2)
    # page.mouse.down()
    # page.mouse.move(target["x"] + target["width"] / 2, target["y"] + target["height"] / 2)
    # page.mouse.up()

    # Method 02:
    # page.locator("#draggable").drag_to(page.locator("#droppable"))

    # Method 03:
    page.drag_and_drop("#draggable", "#droppable")


@pytest.mark.skip(reason="Not impement yet")
def test_sortable(page: Page):

    page.goto("/sortable")
    page.wait_for_load_state()

    elements = page.locator("#cdk-drop-list-0 div")
    for i in range(elements.count()):
        elements.nth(i).drag_to(page.locator("#cdk-drop-list-1 div >> nth=0"))


def test_selectable(page: Page):

    page.goto("/selectable")
    page.wait_for_load_state()

    page.click("#selectable >> nth=0")
    page.keyboard.down("Shift")
    page.click("#selectable >> nth=8")
    page.keyboard.up("Shift")


@pytest.mark.skip(reason="Not impement yet")
def test_slider(page: Page):

    page.goto("/slider")
    page.wait_for_load_state()


def test_table(page: Page):

    page.goto("/table")
    page.wait_for_load_state()

    shopping_tds = page.locator("#shopping td")

    prices = [int(shopping_tds.nth(i).text_content()) for i in range(shopping_tds.count()) if i % 2 != 0]

    logging.info(prices)
    assert sum(prices[:-1]) == prices[-1]

    page.locator("#simpletable tr:has-text('Raj')").locator("input").check()

    headers = page.locator("#advancedtable th")
    rows = page.locator("#advancedtable tr")
    cols = page.locator("#advancedtable td")

    # The original data without sorting
    datas = [[cols.nth(i).text_content() for i in range(j, cols.count(), headers.count())] for j in range(0, rows.count())]
    logging.info(datas)

    # Sort data by column and verify data
    for i in range(headers.count()):
        headers.nth(i).click()
        sort = headers.nth(i).get_attribute("aria-sort")

        if sort == "ascending":
            reverse = False
        elif sort == "descending":
            reverse = True

        data = [
            int(cols.nth(i).text_content()) if cols.nth(i).text_content().isdigit() else cols.nth(i).text_content()
            for i in range(i, cols.count(), 6)
        ]
        assert data == sorted(data, reverse=reverse)


def test_advancedtable(page: Page):

    page.goto("/advancedtable")
    page.wait_for_load_state()

    select = page.locator("select")
    options = select.locator("option").all_text_contents()

    for option in options:
        page.locator("select").select_option(value=[option])
        assert page.locator("#advancedtable tbody tr").count() == int(option)

    # page = 1
    page.locator("a[data-dt-idx='2']").click()

    count = page.locator("#advancedtable th").count()
    rows = page.locator("#advancedtable tr")
    cols = page.locator("#advancedtable td")
    datas = [[cols.nth(i).text_content() for i in range(j, cols.count(), count)] for j in range(0, rows.count())]

    # Note: page.locator(".paginate_button.next").is_enabled() is not worked here, looks so strange, so used class attribute instead
    while page.locator(".paginate_button.next").get_attribute("class") != "paginate_button next disabled":
        page.locator(".paginate_button.next").click()

        rows = page.locator("#advancedtable tr")
        cols = page.locator("#advancedtable td")
        datas += [[cols.nth(i).text_content() for i in range(j, cols.count(), count)] for j in range(0, rows.count())]

    logging.info(datas)
