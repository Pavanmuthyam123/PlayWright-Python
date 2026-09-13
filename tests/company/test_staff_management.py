import os
import pytest

from playwright.sync_api import expect
from pages.staff_management_page import StaffManagementPage


# ================================================================
# EXISTING STAFF DATA
# ================================================================

EXISTING_STAFF_NAME = "Playwright Agent"

# IMPORTANT:
# This email already exists in the application.
EXISTING_EMAIL = "playwright.agent2026@gmail.com"


# ================================================================
# DUPLICATE EMAIL TEST DATA
# ================================================================

ATTEMPTED_STAFF_NAME = "Duplicate Email Test Agent"

PASSWORD = "1234567"

PHONE = "9676565544"

SPECIALIZATION = "Playwright Issue"


# ================================================================
# DUPLICATE EMAIL TEST
# ================================================================

def test_company_duplicate_staff_email(
    company_login
):
    """
    Negative Test Case:

    Try to create a staff member using an
    already registered email.

    PROJECT REQUIREMENT:

    Duplicate email must be reported as FAIL.

    Failure evidence must include:

    1. Clear failure reason
    2. Actual API response message
    3. Screenshot
    4. HTML pytest report
    """

    # ============================================================
    # COMPANY LOGIN
    # ============================================================
    #
    # Company login is handled by the reusable
    # company_login fixture from conftest.py.
    #
    # ============================================================

    page = company_login

    print("\nCompany dashboard verified through fixture.")

    # ============================================================
    # SCREENSHOT DIRECTORY
    # ============================================================

    screenshot_dir = os.path.join(
        "reports",
        "screenshots"
    )

    os.makedirs(
        screenshot_dir,
        exist_ok=True
    )

    # ============================================================
    # STAFF MANAGEMENT
    # ============================================================

    staff_page = StaffManagementPage(page)

    staff_page.open_staff_management()

    # ============================================================
    # VERIFY EXISTING EMAIL
    # ============================================================

    staff_page.verify_existing_staff(
        EXISTING_STAFF_NAME,
        EXISTING_EMAIL
    )

    # ============================================================
    # OPEN ADD STAFF FORM
    # ============================================================

    staff_page.open_add_staff_form()

    # ============================================================
    # ENTER DUPLICATE EMAIL
    # ============================================================

    staff_page.enter_staff_basic_details(
        name=ATTEMPTED_STAFF_NAME,
        email=EXISTING_EMAIL,
        password=PASSWORD
    )

    print(
        f"\nDuplicate email entered: {EXISTING_EMAIL}"
    )

    # ============================================================
    # SELECT ROLE
    # ============================================================

    staff_page.select_agent_role()

    # ============================================================
    # SELECT DEPARTMENT
    # ============================================================

    staff_page.select_department()

    # ============================================================
    # ENTER VALID PHONE
    # ============================================================

    staff_page.enter_phone_and_skills(
        phone=PHONE,
        skills=SPECIALIZATION
    )

    # ============================================================
    # BEFORE SUBMIT SCREENSHOT
    # ============================================================

    before_path = os.path.join(
        screenshot_dir,
        "duplicate_email_before_submit.png"
    )

    page.screenshot(
        path=before_path,
        full_page=True
    )

    print(
        f"\nBefore-submit screenshot: {before_path}"
    )

    # ============================================================
    # SUBMIT AND CAPTURE API RESPONSE
    # ============================================================

    print(
        "\nSubmitting duplicate email..."
    )

    try:

        with page.expect_response(
            lambda response:
                response.request.method == "POST"
                and "/staff" in response.url,
            timeout=10000
        ) as response_info:

            staff_page.click_add()

        response = response_info.value

    except Exception as error:

        failure_path = os.path.join(
            screenshot_dir,
            "duplicate_email_api_error.png"
        )

        page.screenshot(
            path=failure_path,
            full_page=True
        )

        pytest.fail(
            "DUPLICATE EMAIL TEST FAILED\n"
            "Reason: Staff API response was not captured.\n"
            f"Screenshot: {failure_path}\n"
            f"Error: {error}"
        )

    # ============================================================
    # READ API RESPONSE
    # ============================================================

    try:

        response_data = response.json()

    except Exception as error:

        raw_response = response.text()

        failure_path = os.path.join(
            screenshot_dir,
            "duplicate_email_invalid_response.png"
        )

        page.screenshot(
            path=failure_path,
            full_page=True
        )

        pytest.fail(
            "DUPLICATE EMAIL TEST FAILED\n"
            "Reason: Staff API returned an invalid response.\n"
            f"Raw Response: {raw_response}\n"
            f"Screenshot: {failure_path}\n"
            f"Error: {error}"
        )

    # ============================================================
    # EXTRACT API VALUES
    # ============================================================

    success = response_data.get(
        "success"
    )

    message = response_data.get(
        "message",
        ""
    )

    # ============================================================
    # AFTER SUBMIT SCREENSHOT
    # ============================================================

    after_path = os.path.join(
        screenshot_dir,
        "duplicate_email_failure.png"
    )

    page.screenshot(
        path=after_path,
        full_page=True
    )

    print(
        f"\nAfter-submit screenshot: {after_path}"
    )

    # ============================================================
    # PRINT API INFORMATION
    # ============================================================

    print("\n==============================================")
    print("DUPLICATE EMAIL VALIDATION")
    print("==============================================")

    print(
        f"Status Code : {response.status}"
    )

    print(
        f"Success     : {success}"
    )

    print(
        f"Message     : {message}"
    )

    print(
        f"Screenshot  : {after_path}"
    )

    print("==============================================")

    # ============================================================
    # PROJECT RULE
    # ============================================================
    #
    # Existing / duplicate email was intentionally supplied.
    #
    # Therefore:
    #
    # DUPLICATE EMAIL = TEST FAILURE
    #
    # This is OUR PROJECT TESTING CONVENTION.
    #
    # ============================================================

    if success is False:

        pytest.fail(
            "DUPLICATE EMAIL TEST FAILED\n"
            "\n"
            "Reason: Already registered email was provided.\n"
            "\n"
            f"Email: {EXISTING_EMAIL}\n"
            f"Application Message: {message}\n"
            f"API Status Code: {response.status}\n"
            f"Screenshot: {after_path}"
        )

    # ============================================================
    # DUPLICATE EMAIL WAS ACCEPTED
    # ============================================================

    if success is True:

        pytest.fail(
            "DUPLICATE EMAIL TEST FAILED\n"
            "\n"
            "Reason: Application accepted an already "
            "registered email.\n"
            "\n"
            f"Email: {EXISTING_EMAIL}\n"
            f"Application Message: {message}\n"
            f"API Status Code: {response.status}\n"
            f"Screenshot: {after_path}"
        )

    # ============================================================
    # UNKNOWN API RESPONSE
    # ============================================================

    pytest.fail(
        "DUPLICATE EMAIL TEST FAILED\n"
        "\n"
        "Reason: Unexpected staff API response.\n"
        f"API Response: {response_data}\n"
        f"Screenshot: {after_path}"
    )


# ################################################################
# ################################################################
# POSITIVE STAFF CREATION TEST
# ################################################################
# ################################################################


def test_company_create_staff(
    company_login
):
    """
    Positive Test Case:

    Create a new Staff / Agent using unique details.

    Expected Result:

    Staff should be created successfully.
    """

    # ============================================================
    # COMPANY LOGIN
    # ============================================================
    #
    # Reusable company_login fixture handles:
    #
    # 1. Open Login page
    # 2. Enter company email
    # 3. Enter company password
    # 4. Click Sign In
    # 5. Verify Company Dashboard
    #
    # ============================================================

    page = company_login

    print("\nCompany dashboard verified through fixture.")

    # ============================================================
    # STAFF MANAGEMENT PAGE OBJECT
    # ============================================================

    staff_page = StaffManagementPage(page)

    # ============================================================
    # OPEN STAFF MANAGEMENT
    # ============================================================

    staff_page.open_staff_management()

    # ============================================================
    # OPEN ADD STAFF FORM
    # ============================================================

    staff_page.open_add_staff_form()

    # ============================================================
    # POSITIVE TEST DATA
    # ============================================================
    #
    # IMPORTANT:
    # These values should not already exist in the application.
    #
    # ============================================================

    staff_name = "Playwright Positive Agent"

    staff_email = (
        "playwright.positive.agent.2026@gmail.com"
    )

    staff_password = "1234567"

    staff_phone = "9876543210"

    staff_skills = "Playwright Testing"

    # ============================================================
    # ENTER BASIC DETAILS
    # ============================================================

    staff_page.enter_staff_basic_details(
        name=staff_name,
        email=staff_email,
        password=staff_password
    )

    print(
        f"\nStaff Name : {staff_name}"
    )

    print(
        f"Staff Email: {staff_email}"
    )

    # ============================================================
    # SELECT AGENT ROLE
    # ============================================================

    staff_page.select_agent_role()

    # ============================================================
    # SELECT DEPARTMENT
    # ============================================================

    staff_page.select_department()

    # ============================================================
    # ENTER PHONE AND SKILLS
    # ============================================================

    staff_page.enter_phone_and_skills(
        phone=staff_phone,
        skills=staff_skills
    )

    # ============================================================
    # VERIFY ADD BUTTON
    # ============================================================

    staff_page.verify_add_button_enabled()

    # ============================================================
    # CREATE STAFF
    # ============================================================

    print(
        "\nCreating new staff..."
    )

    staff_page.click_add()

    # ============================================================
    # VERIFY STAFF NAME CREATED
    # ============================================================

    expect(
        page.get_by_text(
            staff_name,
            exact=True
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        f"\nStaff name verified: {staff_name}"
    )

    # ============================================================
    # VERIFY STAFF EMAIL CREATED
    # ============================================================

    expect(
        page.get_by_text(
            staff_email,
            exact=True
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        f"Staff email verified: {staff_email}"
    )

    # ============================================================
    # FINAL RESULT
    # ============================================================

    print("\n==============================================")
    print("POSITIVE STAFF CREATION PASSED")
    print("==============================================")
    print(f"Staff Name : {staff_name}")
    print(f"Staff Email: {staff_email}")
    print(f"Staff Phone: {staff_phone}")
    print("Role       : Agent")
    print("Department : Technical Support")
    print("Result     : STAFF CREATED SUCCESSFULLY")
    print("==============================================")

# ################################################################
# ################################################################
# DUPLICATE PHONE TEST
# ################################################################
# ################################################################


def test_company_duplicate_staff_phone(
    company_login
):
    """
    Negative Test Case:

    Try to create a staff member using an
    already registered phone number.

    PROJECT REQUIREMENT:

    Duplicate phone must be reported as FAIL.

    Failure evidence must include:

    1. Clear failure reason
    2. Actual API response message
    3. Screenshot
    4. HTML pytest report
    """

    # ============================================================
    # EXISTING STAFF PHONE
    # ============================================================

    existing_phone = "9676565543"

    # ============================================================
    # TEST DATA
    # ============================================================

    attempted_staff_name = "Duplicate Phone Test Agent"

    new_email = "duplicate.phone.test.2026@gmail.com"

    password = "1234567"

    specialization = "Playwright Phone Validation"

    # ============================================================
    # COMPANY LOGIN
    # ============================================================

    page = company_login

    print("\nCompany dashboard verified through fixture.")

    # ============================================================
    # SCREENSHOT DIRECTORY
    # ============================================================

    screenshot_dir = os.path.join(
        "reports",
        "screenshots"
    )

    os.makedirs(
        screenshot_dir,
        exist_ok=True
    )

    # ============================================================
    # STAFF MANAGEMENT
    # ============================================================

    staff_page = StaffManagementPage(page)

    staff_page.open_staff_management()

    # ============================================================
    # OPEN ADD STAFF FORM
    # ============================================================

    staff_page.open_add_staff_form()

    # ============================================================
    # ENTER BASIC DETAILS
    # ============================================================

    staff_page.enter_staff_basic_details(
        name=attempted_staff_name,
        email=new_email,
        password=password
    )

    print(
        f"\nNew email entered: {new_email}"
    )

    # ============================================================
    # SELECT ROLE
    # ============================================================

    staff_page.select_agent_role()

    # ============================================================
    # SELECT DEPARTMENT
    # ============================================================

    staff_page.select_department()

    # ============================================================
    # ENTER DUPLICATE PHONE
    # ============================================================

    staff_page.enter_phone_and_skills(
        phone=existing_phone,
        skills=specialization
    )

    print(
        f"Duplicate phone entered: {existing_phone}"
    )

    # ============================================================
    # BEFORE SUBMIT SCREENSHOT
    # ============================================================

    before_path = os.path.join(
        screenshot_dir,
        "duplicate_phone_before_submit.png"
    )

    page.screenshot(
        path=before_path,
        full_page=True
    )

    print(
        f"\nBefore-submit screenshot: {before_path}"
    )

    # ============================================================
    # SUBMIT AND CAPTURE API RESPONSE
    # ============================================================

    print(
        "\nSubmitting duplicate phone..."
    )

    try:

        with page.expect_response(
            lambda response:
                response.request.method == "POST"
                and "/staff" in response.url,
            timeout=10000
        ) as response_info:

            staff_page.click_add()

        response = response_info.value

    except Exception as error:

        failure_path = os.path.join(
            screenshot_dir,
            "duplicate_phone_api_error.png"
        )

        page.screenshot(
            path=failure_path,
            full_page=True
        )

        pytest.fail(
            "DUPLICATE PHONE TEST FAILED\n"
            "Reason: Staff API response was not captured.\n"
            f"Phone: {existing_phone}\n"
            f"Screenshot: {failure_path}\n"
            f"Error: {error}"
        )

    # ============================================================
    # READ API RESPONSE
    # ============================================================

    try:

        response_data = response.json()

    except Exception as error:

        raw_response = response.text()

        failure_path = os.path.join(
            screenshot_dir,
            "duplicate_phone_invalid_response.png"
        )

        page.screenshot(
            path=failure_path,
            full_page=True
        )

        pytest.fail(
            "DUPLICATE PHONE TEST FAILED\n"
            "Reason: Staff API returned an invalid response.\n"
            f"Raw Response: {raw_response}\n"
            f"Screenshot: {failure_path}\n"
            f"Error: {error}"
        )

    # ============================================================
    # EXTRACT API VALUES
    # ============================================================

    success = response_data.get(
        "success"
    )

    message = response_data.get(
        "message",
        ""
    )

    # ============================================================
    # AFTER SUBMIT SCREENSHOT
    # ============================================================

    after_path = os.path.join(
        screenshot_dir,
        "duplicate_phone_failure.png"
    )

    page.screenshot(
        path=after_path,
        full_page=True
    )

    print(
        f"\nAfter-submit screenshot: {after_path}"
    )

    # ============================================================
    # PRINT API INFORMATION
    # ============================================================

    print("\n==============================================")
    print("DUPLICATE PHONE VALIDATION")
    print("==============================================")

    print(
        f"Status Code : {response.status}"
    )

    print(
        f"Success     : {success}"
    )

    print(
        f"Message     : {message}"
    )

    print(
        f"Phone       : {existing_phone}"
    )

    print(
        f"Screenshot  : {after_path}"
    )

    print("==============================================")

    # ============================================================
    # PROJECT RULE
    # ============================================================
    #
    # Existing / duplicate phone was intentionally supplied.
    #
    # Therefore:
    #
    # DUPLICATE PHONE = TEST FAILURE
    #
    # This is OUR PROJECT TESTING CONVENTION.
    #
    # ============================================================

    if success is False:

        pytest.fail(
            "DUPLICATE PHONE TEST FAILED\n"
            "\n"
            "Reason: Already registered phone "
            "number was provided.\n"
            "\n"
            f"Phone: {existing_phone}\n"
            f"Application Message: {message}\n"
            f"API Status Code: {response.status}\n"
            f"Screenshot: {after_path}"
        )

    # ============================================================
    # DUPLICATE PHONE WAS ACCEPTED
    # ============================================================

    if success is True:

        pytest.fail(
            "DUPLICATE PHONE TEST FAILED\n"
            "\n"
            "Reason: Application accepted an already "
            "registered phone number.\n"
            "\n"
            f"Phone: {existing_phone}\n"
            f"Application Message: {message}\n"
            f"API Status Code: {response.status}\n"
            f"Screenshot: {after_path}"
        )

    # ============================================================
    # UNKNOWN API RESPONSE
    # ============================================================

    pytest.fail(
        "DUPLICATE PHONE TEST FAILED\n"
        "\n"
        "Reason: Unexpected staff API response.\n"
        f"API Response: {response_data}\n"
        f"Screenshot: {after_path}"
    )