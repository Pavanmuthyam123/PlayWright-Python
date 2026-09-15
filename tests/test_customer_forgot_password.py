import time

from playwright.sync_api import Page, expect

from utils.gmail_otp import get_reset_code


def test_customer_forgot_password(page: Page):

    # 1. Open Forgot Password page
    page.goto(
        "https://www.ticksupport.com/tcs/forgot-password"
    )

    # 2. Verify Forgot Password page
    expect(
        page.get_by_role(
            "heading",
            name="FORGOT PASSWORD"
        )
    ).to_be_visible()

    # 3. Enter registered email
    page.locator(
        'input[type="email"]'
    ).fill(
        "pavanmuthyam570+test70524@gmail.com"
    )

    # 4. Capture time before requesting reset code
    request_time = int(
        time.time() * 1000
    )

    # 5. Click Send Reset Code
    page.get_by_role(
        "button",
        name="Send Reset Code"
    ).click()

    # 6. Get NEW reset code from Gmail
    reset_code = get_reset_code(
        after_timestamp=request_time
    )

    print(
        "New reset code received from Gmail:",
        reset_code
    )

    # 7. Verify reset code input is visible
    expect(
        page.locator(
            'input[placeholder="Enter reset code"]'
        )
    ).to_be_visible()

    # 8. Fill reset code
    page.locator(
        'input[placeholder="Enter reset code"]'
    ).fill(
        reset_code
    )

    # 9. Click Verify Code
    page.get_by_role(
        "button",
        name="Verify Code"
    ).click()

    # 10. Verify NEW PASSWORD input is visible
    expect(
        page.locator(
            'input[placeholder="Min 6 characters"]'
        )
    ).to_be_visible()

    # 11. Enter new password
    new_password = "NewTest@123"

    page.locator(
        'input[placeholder="Min 6 characters"]'
    ).fill(
        new_password
    )

    # 12. Enter confirm password
    page.locator(
        'input[placeholder="Repeat new password"]'
    ).fill(
        new_password
    )

    # 13. Verify new password value
    expect(
        page.locator(
            'input[placeholder="Min 6 characters"]'
        )
    ).to_have_value(
        new_password
    )

    # 14. Verify confirm password value
    expect(
        page.locator(
            'input[placeholder="Repeat new password"]'
        )
    ).to_have_value(
        new_password
    )

    # 15. Click Reset Password
    page.get_by_role(
        "button",
        name="Reset Password"
    ).click()

    # 16. Wait for result
    page.wait_for_timeout(2000)

    # 17. Pause to inspect result
    page.pause()
