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

    page.bring_to_front()
    new_page.close()

    with context.expect_page() as new_page:
        page.click("#multi")

    pages = new_page.value.context.pages
    for new_page in pages:
        new_page.wait_for_load_state()
        logging.info(new_page.title())
