from playwright.sync_api import Page, expect


def test_login(page: Page):
    # 1. Open Admin Login page
    page.goto("https://www.ticksupport.com/admin/login")

    # 2. Enter Admin Email
    page.locator('[type="email"]').fill("admin@ticketflow.com")

    # 3. Enter Admin Password
    page.locator('[type="password"]').fill("123456")

    # 4. Click Authenticate
    page.locator('[type="submit"]').click()

    # 5. Verify successful login
    expect(page).to_have_url(
        "https://www.ticksupport.com/platform/dashboard"
    )

    # 6. Click the profile button in the top bar
    page.locator("button.topbar-profile-btn").click()

    # 7. Find Sign out button
    sign_out = page.locator("button").filter(has_text="Sign out")

    # 8. Verify Sign out is visible
    expect(sign_out).to_be_visible()
    
    page.wait_for_timeout(3000)
    

    # 9. Click Sign out
    sign_out.click()