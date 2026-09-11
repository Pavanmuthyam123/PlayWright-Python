from playwright.sync_api import Page, expect


def test_customer_login_with_new_password(page: Page):

    # 1. Open Customer Login page
    page.goto(
        "https://www.ticksupport.com/tcs/user/login"
    )

    # 2. Verify Login page
    expect(
        page.get_by_role(
            "heading",
            name="WELCOME BACK"
        )
    ).to_be_visible()

    # 3. Enter registered email
    page.locator(
        'input[type="email"]'
    ).fill(
        "pavanmuthyam570+test70524@gmail.com"
    )

    # 4. Enter NEW password
    page.locator(
        'input[type="password"]'
    ).fill(
        "NewTest@123"
    )

    # 5. Verify email
    expect(
        page.locator(
            'input[type="email"]'
        )
    ).to_have_value(
        "pavanmuthyam570+test70524@gmail.com"
    )

    # 6. Verify new password is entered
    expect(
        page.locator(
            'input[type="password"]'
        )
    ).to_have_value(
        "NewTest@123"
    )

    # 7. Click Sign In
    page.get_by_role(
        "button",
        name="Sign In"
    ).click()

    # 8. Verify Customer Dashboard
    expect(
        page.get_by_role(
            "link",
            name="Dashboard"
        )
    ).to_be_visible()

    # 9. Verify customer dashboard URL
    expect(
        page
    ).to_have_url(
        "https://www.ticksupport.com/tcs/my/dashboard"
    )

    # 10. Pause for inspection
    page.pause()