from playwright.sync_api import Page,expect

def test_openurl(page:Page):
    page.goto("https://www.ticksupport.com/login")
    page.wait_for_timeout(3000)