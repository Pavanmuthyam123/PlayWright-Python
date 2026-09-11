import random

from playwright.sync_api import Page, expect

from utils.gmail_otp import get_latest_otp


# ============================================================
# REG-001 - POSITIVE REGISTRATION TEST
# ============================================================

def test_customer_registration(page: Page):

    # 1. Generate unique test email
    test_email = (
        f"pavanmuthyam570+test{random.randint(10000, 99999)}@gmail.com"
    )

    print("Test email:", test_email)

    # 2. Open Customer Registration page
    page.goto(
        "https://www.ticksupport.com/tcs/user/register"
    )

    # 3. Verify registration page
    expect(
        page.get_by_role(
            "heading",
            name="CREATE ACCOUNT"
        )
    ).to_be_visible()

    # 4. Enter Full Name
    page.locator("label").filter(
        has_text="Full Name"
    ).locator(
        "xpath=following-sibling::input"
    ).fill("Test Customer")

    # 5. Enter Email
    page.locator(
        'input[type="email"]'
    ).fill(test_email)

    # 6. Enter Phone Number
    page.locator(
        'input[placeholder="+91XXXXXXXXXX"]'
    ).fill("9876543210")

    # 7. Enter Password
    page.locator(
        'input[type="password"]'
    ).fill("Test@123")

    # 8. Verify entered data
    expect(
        page.locator(
            'input[placeholder="John Doe"]'
        )
    ).to_have_value("Test Customer")

    expect(
        page.locator(
            'input[type="email"]'
        )
    ).to_have_value(test_email)

    # 9. Click Send OTP & Create Account
    page.get_by_role(
        "button",
        name="Send OTP & Create Account"
    ).click()

    # 10. Verify OTP screen
    expect(
        page.get_by_role(
            "heading",
            name="Verification Code Sent"
        )
    ).to_be_visible()

    # 11. Wait temporarily for OTP email
    page.wait_for_timeout(5000)

    # 12. Get latest OTP from Gmail
    otp = get_latest_otp()

    print("OTP received from Gmail:", otp)

    # 13. Enter OTP
    page.locator(
        'input[placeholder="123456"]'
    ).fill(otp)

    # 14. Verify OTP
    page.get_by_role(
        "button",
        name="Verify & Complete"
    ).click()

    # 15. Wait temporarily to check result
    page.wait_for_timeout(5000)


# ============================================================
# REG-017 - NEGATIVE / VALIDATION TEST
# Empty registration form
# ============================================================

def test_registration_required_field_validation(page: Page):

    # 1. Open Customer Registration page
    page.goto(
        "https://www.ticksupport.com/tcs/user/register"
    )

    # 2. Verify registration page
    expect(
        page.get_by_role(
            "heading",
            name="CREATE ACCOUNT"
        )
    ).to_be_visible()

    # 3. Leave all fields empty
    # No data is entered

    # 4. Click Send OTP & Create Account
    page.get_by_role(
        "button",
        name="Send OTP & Create Account"
    ).click()

    # 5. Verify user-friendly field-level validation
    #
    # Expected:
    # Full Name error should appear BELOW
    # the Full Name input field.

    full_name_input = page.locator(
        'input[placeholder="John Doe"]'
    )

    # This looks for an error element associated
    # with the Full Name input.
    full_name_error = full_name_input.locator(
        "xpath=following-sibling::*"
    ).filter(
        has_text="Full name is required."
    )

    # 6. Assertion
    # If the application displays the error only
    # at the top of the page, this assertion fails.
    #
    # FAIL -> Playwright screenshot
    # FAIL -> HTML report
    expect(
        full_name_error
    ).to_be_visible(timeout=5000)