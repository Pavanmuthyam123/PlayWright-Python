import time

from playwright.sync_api import Page, expect

from utils.gmail_otp import get_reset_code


# ================================================================
# TEST DATA
# ================================================================

RESET_EMAIL = "pavanmuthyam570+test70524@gmail.com"

NEW_PASSWORD = "ResetTest@2026"


# ================================================================
# CUSTOMER FORGOT PASSWORD TEST
# ================================================================

def test_customer_forgot_password(
    page: Page
):
    """
    Customer Forgot Password End-to-End Test.

    Flow:

        Forgot Password
              ↓
        Enter Email
              ↓
        Send Reset Code
              ↓
        Get Fresh OTP from Gmail
              ↓
        Enter OTP
              ↓
        Verify OTP
              ↓
        Enter New Password
              ↓
        Confirm New Password
              ↓
        Reset Password
              ↓
        Login Page
              ↓
        SAME EMAIL
              ↓
        NEW PASSWORD
              ↓
        Login
              ↓
        SAME CUSTOMER ACCOUNT
              ↓
        Customer Dashboard
    """

    # ============================================================
    # 1. OPEN FORGOT PASSWORD PAGE
    # ============================================================

    page.goto(
        "https://www.ticksupport.com/tcs/forgot-password"
    )

    expect(
        page.get_by_role(
            "heading",
            name="FORGOT PASSWORD"
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        "\nForgot Password page opened."
    )

    # ============================================================
    # 2. ENTER EMAIL
    # ============================================================

    email_field = page.locator(
        'input[type="email"]'
    )

    expect(
        email_field
    ).to_be_visible(
        timeout=10000
    )

    email_field.fill(
        RESET_EMAIL
    )

    print(
        f"Reset email entered: {RESET_EMAIL}"
    )

    # ============================================================
    # 3. RECORD REQUEST TIME
    # ============================================================
    #
    # Record timestamp BEFORE requesting the OTP.
    #
    # This allows Gmail utility to ignore old reset emails.
    # ============================================================

    request_time = int(
        time.time() * 1000
    )

    print(
        f"Reset request timestamp: {request_time}"
    )

    # ============================================================
    # 4. SEND RESET CODE
    # ============================================================

    send_reset_button = page.get_by_role(
        "button",
        name="Send Reset Code",
        exact=True
    )

    expect(
        send_reset_button
    ).to_be_visible(
        timeout=10000
    )

    send_reset_button.click()

    print(
        "Send Reset Code clicked."
    )

    # ============================================================
    # 5. VERIFY RESET CODE SCREEN
    # ============================================================

    reset_code_field = page.locator(
        'input[placeholder="Enter reset code"]'
    )

    expect(
        reset_code_field
    ).to_be_visible(
        timeout=15000
    )

    print(
        "Reset code screen opened."
    )

    # ============================================================
    # 6. GET FRESH OTP FROM GMAIL
    # ============================================================

    reset_code = get_reset_code(
        email=RESET_EMAIL,
        timeout=60,
        after_timestamp=request_time
    )

    print(
        f"\nFresh reset code received: {reset_code}"
    )

    # ============================================================
    # 7. ENTER OTP
    # ============================================================

    reset_code_field.fill(
        reset_code
    )

    print(
        "Fresh reset code entered."
    )

    # ============================================================
    # 8. VERIFY OTP
    # ============================================================

    verify_code_button = page.get_by_role(
        "button",
        name="Verify Code",
        exact=True
    )

    expect(
        verify_code_button
    ).to_be_visible(
        timeout=10000
    )

    verify_code_button.click()

    print(
        "Verify Code clicked."
    )

    # ============================================================
    # 9. VERIFY NEW PASSWORD SCREEN
    # ============================================================

    new_password_message = page.get_by_text(
        "Code verified. Enter your new password.",
        exact=True
    )

    expect(
        new_password_message
    ).to_be_visible(
        timeout=10000
    )

    print(
        "Reset code verified successfully."
    )

    # ============================================================
    # 10. ENTER NEW PASSWORD
    # ============================================================

    new_password_field = page.locator(
        'input[placeholder="Min 6 characters"]'
    )

    expect(
        new_password_field
    ).to_be_visible(
        timeout=10000
    )

    new_password_field.fill(
        NEW_PASSWORD
    )

    print(
        "New password entered."
    )

    # ============================================================
    # 11. CONFIRM NEW PASSWORD
    # ============================================================

    confirm_password_field = page.locator(
        'input[placeholder="Repeat new password"]'
    )

    expect(
        confirm_password_field
    ).to_be_visible(
        timeout=10000
    )

    confirm_password_field.fill(
        NEW_PASSWORD
    )

    print(
        "New password confirmed."
    )

    # ============================================================
    # 12. RESET PASSWORD
    # ============================================================

    reset_password_button = page.get_by_role(
        "button",
        name="Reset Password",
        exact=True
    )

    expect(
        reset_password_button
    ).to_be_visible(
        timeout=10000
    )

    reset_password_button.click()

    print(
        "Reset Password clicked."
    )

    # ============================================================
    # 13. VERIFY LOGIN PAGE
    # ============================================================
    #
    # IMPORTANT:
    #
    # Application redirects to:
    #
    #     https://www.ticksupport.com/login
    #
    # NOT:
    #
    #     https://www.ticksupport.com/tcs/login
    #
    # ============================================================

    page.wait_for_url(
        "**/login",
        timeout=15000
    )

    expect(
        page.get_by_role(
            "heading",
            name="WELCOME BACK"
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        f"Login page opened successfully: {page.url}"
    )

    # ============================================================
    # 14. LOGIN WITH SAME EMAIL + NEW PASSWORD
    # ============================================================

    login_email_field = page.locator(
        'input[type="email"]'
    )

    login_password_field = page.locator(
        'input[type="password"]'
    )

    expect(
        login_email_field
    ).to_be_visible(
        timeout=10000
    )

    expect(
        login_password_field
    ).to_be_visible(
        timeout=10000
    )

    # SAME EMAIL USED FOR PASSWORD RESET
    login_email_field.fill(
        RESET_EMAIL
    )

    # NEWLY CHANGED PASSWORD
    login_password_field.fill(
        NEW_PASSWORD
    )

    print(
        "Same email entered."
    )

    print(
        "New password entered."
    )

    # ============================================================
    # 15. CLICK SIGN IN
    # ============================================================

    sign_in_button = page.get_by_role(
        "button",
        name="Sign In",
        exact=True
    )

    expect(
        sign_in_button
    ).to_be_visible(
        timeout=10000
    )

    sign_in_button.click()

    print(
        "Sign In clicked."
    )

    # ============================================================
    # 16. VERIFY SAME CUSTOMER ACCOUNT LOGIN
    # ============================================================

    page.wait_for_url(
        "**/tcs/my/dashboard",
        timeout=15000
    )

    expect(
        page.get_by_text(
            "Welcome to Tcs support portal",
            exact=True
        )
    ).to_be_visible(
        timeout=10000
    )

    # ============================================================
    # 17. FINAL SUCCESS
    # ============================================================

    print()
    print("=" * 70)
    print("FORGOT PASSWORD TEST PASSED")
    print("=" * 70)

    print(
        f"Email        : {RESET_EMAIL}"
    )

    print(
        "OTP          : Fresh OTP verified"
    )

    print(
        "Password     : Successfully changed"
    )

    print(
        "Login        : Successful"
    )

    print(
        "Account      : Same customer account"
    )

    print(
        f"Dashboard    : {page.url}"
    )

    print("=" * 70)