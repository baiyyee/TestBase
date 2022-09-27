import random
import pytest
import logging
from pandas import DataFrame
from playwright.sync_api import Page, expect
from WeTest.util import compare, date, testdata, path
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


def test_slider(page: Page):

    page.goto("/slider")
    page.wait_for_load_state()

    src = page.locator("#generate").bounding_box()

    while page.locator("h1.has-text-info").text_content().split(":")[-1].strip() != "20":
        page.mouse.move(src["x"], src["y"])
        page.mouse.down()
        page.mouse.move(src["x"] + 15, src["y"])
        page.mouse.up()

        src["x"] = src["x"] + 15

        page.wait_for_timeout(1000)

    page.click(".block .button.is-primary")
    country = page.locator(".notification.is-primary").all_text_contents()[0].split("-")
    assert len(country) == 20


def test_table(page: Page):

    page.goto("/table")
    page.wait_for_load_state()

    shopping_tds = page.locator("#shopping td")

    prices = [int(shopping_tds.nth(i).text_content()) for i in range(shopping_tds.count()) if i % 2 != 0]

    logging.info(prices)
    assert sum(prices[:-1]) == prices[-1]

    # page.locator("#simpletable tr:has-text('Raj')").locator("input").check()
    page.locator("#simpletable tr:has-text('Raj') td >> nth=3").check()

    headers = page.locator("#advancedtable th")
    rows = page.locator("#advancedtable tr")
    cols = page.locator("#advancedtable td")

    # The original data without sorting
    datas = [[cols.nth(i).text_content() for i in range(j, cols.count(), headers.count())] for j in range(0, headers.count())]
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
    cols = page.locator("#advancedtable td")
    datas = [[cols.nth(i).text_content() for i in range(j, cols.count(), count)] for j in range(0, count)]

    # Note: page.locator(".paginate_button.next").is_enabled() is not worked here, looks so strange, so used class attribute instead
    while page.locator(".paginate_button.next").get_attribute("class") != "paginate_button next disabled":
        page.locator(".paginate_button.next").click()

        cols = page.locator("#advancedtable td")
        data = [[cols.nth(i).text_content() for i in range(j, cols.count(), count)] for j in range(0, count)]

        for i in range(count):
            datas[i] += data[i]

    df = DataFrame(columns=[page.locator("#advancedtable th").nth(i).text_content() for i in range(count)])
    for i, column in enumerate(df.columns):
        df[column] = datas[i]

    # Verify Search
    for column in df.columns:
        search = random.choice(df[column])
        filter = df.loc[df[column].str.contains(search), :].reset_index(drop=True)

        logging.info(f"column => {column}")
        logging.info(f"search => {search}")

        page.locator("input[type='search']").fill(search)

        # For below locator, only 1 pages shows, only verify page 1 for now
        tr = page.locator("#advancedtable tbody tr")
        filter = filter.head(tr.count())

        assert tr.count() == len(filter)

        for i in range(tr.count()):
            assert tr.nth(i).all_text_contents()[0] == "".join(filter.loc[i, :].to_list())


def test_calendar(page: Page):

    page.goto("/calendar")
    page.wait_for_load_state()

    today = date.get_today("D")
    today_add_3 = date.get_date_by_timedelta(date.get_today(), "D", days=3)

    page.locator(".datetimepicker-dummy.is-primary input >> nth=0").click()
    page.locator(f".datepicker-days >> nth=1 >> button:text-is('{today}')").click()
    page.locator(f".datepicker-days >> nth=1 >> button:text-is('{today_add_3}') >> nth=-1").click()

    logging.info(date.get_today("H"))
    logging.info(date.get_today("m"))

    for _ in range(int(date.get_today("H")) + 2):
        page.locator(".timepicker-next >> nth=0").click()
    for _ in range(int(date.get_today("m"))):
        page.locator(".timepicker-next >> nth=-1").click()


def test_waits(page: Page):

    page.goto("/waits")
    page.wait_for_load_state()

    def dialog_handler(dialog):
        logging.info(dialog.type)
        logging.info(dialog.message)
        logging.info(dialog.default_value)
        dialog.accept()

    page.on("dialog", dialog_handler)
    page.click("#accept")
    page.wait_for_event("dialog")


def test_forms(page: Page):

    page.goto("/forms")
    page.wait_for_load_state()

    page.fill("#firstname", "Huabo")
    page.fill("#lasttname", "He")
    page.fill("#email", testdata.email())
    page.select_option(".control select", value="86")
    page.fill("#Phno", testdata.string(seeds="123456789", length=10))
    page.fill("#Addl1", testdata.address())
    page.fill("#Addl2", testdata.address())
    page.fill("#state", testdata.address())
    page.fill("#postalcode", testdata.postcode())
    page.select_option("select:below(#country)", value="China")
    page.fill("#Date", "1990-08-28")
    page.check("#male")
    page.click("input[type='checkbox']")
    page.click("input[type='submit']")


def test_file(page: Page, tmp_path):

    page.goto("/file")
    page.wait_for_load_state()

    file = str(tmp_path / "test.txt")

    path.write_text("hello world", file)

    page.locator(".file-cta").set_input_files(file)

    def handler(download):
        logging.info(download.path())
        download.save_as(tmp_path)

    page.on("download", handler)
    page.click("#xls")
    page.click("#pdf")
    page.click("#txt")


def test_shadow(page: Page):

    page.goto("/shadow")
    page.wait_for_load_state()

    page.fill("#fname", "Huabo")
    # page.fill("#lname", "He")
    # page.fill("#email", testdata.email())


def test_scroll(page: Page):

    page.goto("/")
    page.wait_for_load_state()

    button = page.locator("a >> text=LetXPath")

    # Scroll Screen: Method 1
    # button.scroll_into_view_if_needed()

    # Scroll Screen: Method 2
    page.mouse.wheel(0, button.bounding_box()["y"])

    logging.info(button.text_content())


def test_game(page: Page):

    page.goto("/game")
    page.wait_for_load_state()

    page.click(".start-button")
    page.click(".new-game-button >> nth=1")

    while True:
        target = page.locator("div[style='background-color: rgb(236, 100, 75);']").bounding_box()

        while True:
            real = page.locator("div[style='background-color: rgb(51, 110, 123);']").bounding_box()

            if real["x"] == target["x"]:
                page.keyboard.down("ArrowDown")

            elif real["y"] == target["y"]:
                page.keyboard.down("ArrowRight")

            if real == target:
                page.keyboard.down("ArrowRight")
                page.wait_for_timeout(1000)
                page.keyboard.down("ArrowUp")
                break

            page.wait_for_timeout(10)

        page.wait_for_timeout(2000)
