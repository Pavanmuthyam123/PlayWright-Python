import random

from playwright.sync_api import Page, expect

from utils.gmail_otp import (
    get_registration_otp,
    get_reset_code,
)


# ============================================================
# LOGOUT HELPER
# ============================================================

def logout(page: Page):
    print("\nLogging out...")

    # --------------------------------------------------------
    # Open profile menu
    # --------------------------------------------------------

    profile_button = page.locator(
        "button.topbar-profile-btn"
    )

    expect(
        profile_button
    ).to_be_visible(
        timeout=10000
    )

    profile_button.click()

    # --------------------------------------------------------
    # Verify Sign out option
    # --------------------------------------------------------

    sign_out = page.get_by_text(
        "Sign out",
        exact=True
    )

    expect(
        sign_out
    ).to_be_visible(
        timeout=5000
    )

    # --------------------------------------------------------
    # Click Sign out
    # --------------------------------------------------------

    sign_out.click()

    # --------------------------------------------------------
    # IMPORTANT:
    # Actual application redirects to /tcs/login
    # --------------------------------------------------------

    page.wait_for_url(
        "**/tcs/login",
        timeout=10000
    )

    print(
        f"After logout URL: {page.url}"
    )

    # Verify actual login URL
    expect(
        page
    ).to_have_url(
        "https://www.ticksupport.com/tcs/login"
    )

    # Verify login page
    expect(
        page.get_by_role(
            "heading",
            name="WELCOME BACK"
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        "Logout successful"
    )


# ============================================================
# COMPLETE CUSTOMER AUTHENTICATION E2E
# ============================================================

def test_customer_auth_complete_flow(
    page: Page
):

    # ========================================================
    # TEST DATA
    # ========================================================

    test_email = (
        f"pavanmuthyam570+test"
        f"{random.randint(10000, 99999)}"
        f"@gmail.com"
    )

    old_password = "Test@123"
    new_password = "NewTest@123"

    print()
    print("=" * 70)
    print(
        "CUSTOMER AUTHENTICATION E2E TEST"
    )
    print("=" * 70)

    print(
        f"Test Email: {test_email}"
    )

    print("=" * 70)

    # ========================================================
    # 1. CUSTOMER REGISTRATION
    # ========================================================

    print(
        "\n[1] CUSTOMER REGISTRATION"
    )

    page.goto(
        "https://www.ticksupport.com/tcs/user/register"
    )

    expect(
        page.get_by_role(
            "heading",
            name="CREATE ACCOUNT"
        )
    ).to_be_visible()

    # Full Name
    page.locator(
        "label"
    ).filter(
        has_text="Full Name"
    ).locator(
        "xpath=following-sibling::input"
    ).fill(
        "Test Customer"
    )

    # Email
    page.locator(
        'input[type="email"]'
    ).fill(
        test_email
    )

    # Phone
    page.locator(
        'input[placeholder="+91XXXXXXXXXX"]'
    ).fill(
        "9876543210"
    )

    # Password
    page.locator(
        'input[type="password"]'
    ).fill(
        old_password
    )

    # Send OTP
    page.get_by_role(
        "button",
        name="Send OTP & Create Account"
    ).click()

    # ========================================================
    # 2. REGISTRATION OTP
    # ========================================================

    print(
        "\n[2] REGISTRATION OTP"
    )

    expect(
        page.get_by_role(
            "heading",
            name="Verification Code Sent"
        )
    ).to_be_visible(
        timeout=10000
    )

    registration_otp = get_registration_otp(
        email=test_email,
        timeout=45
    )

    print(
        f"Registration OTP: "
        f"{registration_otp}"
    )

    # Fill OTP
    page.locator(
        'input[placeholder="123456"]'
    ).fill(
        registration_otp
    )

    # Verify OTP
    page.get_by_role(
        "button",
        name="Verify & Complete"
    ).click()

    # ========================================================
    # 3. ACCOUNT CREATION
    # ========================================================

    print(
        "\n[3] ACCOUNT CREATION"
    )

    # Wait for dashboard
    expect(
        page.get_by_text(
            "Welcome to Tcs support portal"
        )
    ).to_be_visible(
        timeout=15000
    )

    # Verify success message
    expect(
        page.get_by_text(
            "OTP verified! Account created successfully!",
            exact=True
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        f"After registration URL: {page.url}"
    )

    print(
        "Account created and dashboard opened successfully"
    )

    # ========================================================
    # 4. LOGOUT AFTER ACCOUNT CREATION
    # ========================================================

    print(
        "\n[4] LOGOUT AFTER ACCOUNT CREATION"
    )

    logout(page)

    # ========================================================
    # 5. LOGIN WITH OLD PASSWORD
    # ========================================================

    print(
        "\n[5] LOGIN WITH OLD PASSWORD"
    )

    page.locator(
        'input[type="email"]'
    ).fill(
        test_email
    )

    page.locator(
        'input[type="password"]'
    ).fill(
        old_password
    )

    page.get_by_role(
        "button",
        name="Sign In"
    ).click()

    # Verify dashboard
    expect(
        page
    ).to_have_url(
        "https://www.ticksupport.com/tcs/my/dashboard"
    )

    expect(
        page.get_by_text(
            "Welcome to Tcs support portal"
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        "Login with old password successful"
    )

    # ========================================================
    # 6. LOGOUT AFTER LOGIN
    # ========================================================

    print(
        "\n[6] LOGOUT AFTER LOGIN"
    )

    logout(page)

    # ========================================================
    # 7. FORGOT PASSWORD
    # ========================================================

    print(
        "\n[7] FORGOT PASSWORD"
    )

    page.get_by_text(
        "Forgot password?",
        exact=True
    ).click()

    expect(
        page.get_by_role(
            "heading",
            name="FORGOT PASSWORD"
        )
    ).to_be_visible(
        timeout=10000
    )

    # SAME EMAIL
    page.locator(
        'input[type="email"]'
    ).fill(
        test_email
    )

    # Send reset code
    page.get_by_role(
        "button",
        name="Send Reset Code"
    ).click()

    # ========================================================
    # 8. PASSWORD RESET OTP
    # ========================================================

    print(
        "\n[8] PASSWORD RESET OTP"
    )

    reset_code = get_reset_code(
        email=test_email,
        timeout=45
    )

    print(
        f"Reset Code: "
        f"{reset_code}"
    )

    # Fill reset code
    page.locator(
        'input[placeholder="Enter reset code"]'
    ).fill(
        reset_code
    )

    # Verify reset code
    page.get_by_role(
        "button",
        name="Verify Code"
    ).click()

    # ========================================================
    # 9. NEW PASSWORD
    # ========================================================

    print(
        "\n[9] SET NEW PASSWORD"
    )

    expect(
        page.locator(
            'input[placeholder="Min 6 characters"]'
        )
    ).to_be_visible(
        timeout=10000
    )

    # New password
    page.locator(
        'input[placeholder="Min 6 characters"]'
    ).fill(
        new_password
    )

    # Confirm password
    page.locator(
        'input[placeholder="Repeat new password"]'
    ).fill(
        new_password
    )

    # Reset password
    page.get_by_role(
        "button",
        name="Reset Password"
    ).click()

    # ========================================================
    # 10. VERIFY PASSWORD RESET
    # ========================================================

    print(
        "\n[10] VERIFY PASSWORD RESET"
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
        "Password reset successful"
    )

    # ========================================================
    # 11. LOGIN WITH NEW PASSWORD
    # ========================================================

    print(
        "\n[11] LOGIN WITH NEW PASSWORD"
    )

    page.locator(
        'input[type="email"]'
    ).fill(
        test_email
    )

    page.locator(
        'input[type="password"]'
    ).fill(
        new_password
    )

    page.get_by_role(
        "button",
        name="Sign In"
    ).click()

    # Verify dashboard
    expect(
        page
    ).to_have_url(
        "https://www.ticksupport.com/tcs/my/dashboard"
    )

    expect(
        page.get_by_text(
            "Welcome to Tcs support portal"
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        "Login with new password successful"
    )

    # ========================================================
    # 12. FINAL LOGOUT
    # ========================================================

    print(
        "\n[12] FINAL LOGOUT"
    )

    logout(page)

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("=" * 70)
    print(
        "CUSTOMER AUTHENTICATION E2E PASSED"
    )
    print("=" * 70)

    print(
        f"Test Email              : {test_email}"
    )

    print(
        "Registration             : PASS"
    )

    print(
        "Registration OTP         : PASS"
    )

    print(
        "Account Creation         : PASS"
    )

    print(
        "First Logout              : PASS"
    )

    print(
        "Old Password Login       : PASS"
    )

    print(
        "Second Logout             : PASS"
    )

    print(
        "Forgot Password           : PASS"
    )

    print(
        "Reset OTP                 : PASS"
    )

    print(
        "Password Reset            : PASS"
    )

    print(
        "New Password Login       : PASS"
    )

    print(
        "Final Logout              : PASS"
    )

    print("=" * 70)