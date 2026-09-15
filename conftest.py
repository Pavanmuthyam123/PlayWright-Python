import os
import base64

import pytest


# ================================================================
# PYTEST CONFIGURATION
# ================================================================

def pytest_configure(config):
    """
    Create report directories before test execution.
    """

    os.makedirs(
        "reports",
        exist_ok=True
    )

    os.makedirs(
        "reports/screenshots",
        exist_ok=True
    )


# ================================================================
# REUSABLE COMPANY LOGIN FIXTURE
# ================================================================

@pytest.fixture
def company_login(page):
    """
    Reusable Company Login fixture.

    Any test that needs Company Login can use:

        def test_example(company_login):
            page = company_login

    This avoids repeating Company Login code
    in every test.
    """

    # ------------------------------------------------------------
    # Company Login Details
    # ------------------------------------------------------------

    company_email = "pavanrajmuthyam@gmail.com"
    company_password = "1234567"

    login_url = "https://www.ticksupport.com/tcs/login"
    dashboard_url = "https://www.ticksupport.com/tcs/dashboard"

    # ------------------------------------------------------------
    # 1. Open Company Login
    # ------------------------------------------------------------

    page.goto(
        login_url
    )

    # ------------------------------------------------------------
    # 2. Verify Login Page
    # ------------------------------------------------------------

    page.get_by_role(
        "heading",
        name="WELCOME BACK"
    ).wait_for(
        state="visible",
        timeout=10000
    )

    # ------------------------------------------------------------
    # 3. Enter Company Email
    # ------------------------------------------------------------

    page.locator(
        'input[type="email"]'
    ).fill(
        company_email
    )

    # ------------------------------------------------------------
    # 4. Enter Company Password
    # ------------------------------------------------------------

    page.locator(
        'input[type="password"]'
    ).fill(
        company_password
    )

    # ------------------------------------------------------------
    # 5. Click Sign In
    # ------------------------------------------------------------

    page.get_by_role(
        "button",
        name="Sign In",
        exact=True
    ).click()

    # ------------------------------------------------------------
    # 6. Verify Company Dashboard
    # ------------------------------------------------------------

    page.wait_for_url(
        dashboard_url,
        timeout=10000
    )

    page.get_by_text(
        "Company Super Admin",
        exact=True
    ).wait_for(
        state="visible",
        timeout=10000
    )

    print()
    print("==============================================")
    print("COMPANY LOGIN SUCCESSFUL")
    print("==============================================")
    print(f"Dashboard: {page.url}")
    print("==============================================")

    # ------------------------------------------------------------
    # 7. Return Playwright Page
    # ------------------------------------------------------------

    return page


# ================================================================
# REUSABLE AGENT LOGIN FIXTURE
# ================================================================

@pytest.fixture
def agent_login(page):
    """
    Reusable Agent Login fixture.

    Any test that needs Agent Login can use:

        def test_example(agent_login):
            page = agent_login

    This avoids repeating Agent Login code
    in every Agent test.
    """

    # ------------------------------------------------------------
    # Agent Login Details
    # ------------------------------------------------------------

    agent_email = "johnagent@gmail.com"
    agent_password = "1234567"

    login_url = "https://www.ticksupport.com/tcs/login"

    agent_dashboard_url = (
        "https://www.ticksupport.com/tcs/agent/dashboard"
    )

    # ------------------------------------------------------------
    # 1. Open Login Page
    # ------------------------------------------------------------

    page.goto(
        login_url
    )

    # ------------------------------------------------------------
    # 2. Verify Login Page
    # ------------------------------------------------------------

    page.get_by_role(
        "heading",
        name="WELCOME BACK"
    ).wait_for(
        state="visible",
        timeout=10000
    )

    # ------------------------------------------------------------
    # 3. Enter Agent Email
    # ------------------------------------------------------------

    page.locator(
        'input[type="email"]'
    ).fill(
        agent_email
    )

    # ------------------------------------------------------------
    # 4. Enter Agent Password
    # ------------------------------------------------------------

    page.locator(
        'input[type="password"]'
    ).fill(
        agent_password
    )

    # ------------------------------------------------------------
    # 5. Click Sign In
    # ------------------------------------------------------------

    page.get_by_role(
        "button",
        name="Sign In",
        exact=True
    ).click()

    # ------------------------------------------------------------
    # 6. Verify Agent Dashboard
    # ------------------------------------------------------------

    page.wait_for_url(
        agent_dashboard_url,
        timeout=10000
    )

    page.get_by_text(
        "John-Agent",
        exact=False
    ).first.wait_for(
        state="visible",
        timeout=10000
    )

    # ------------------------------------------------------------
    # 7. Print Login Information
    # ------------------------------------------------------------

    print()
    print("==============================================")
    print("AGENT LOGIN SUCCESSFUL")
    print("==============================================")
    print(f"Dashboard: {page.url}")
    print("Agent: John-Agent")
    print("==============================================")

    # ------------------------------------------------------------
    # 8. Return Playwright Page
    # ------------------------------------------------------------

    return page


# ================================================================
# REUSABLE CUSTOMER LOGIN FIXTURE
# ================================================================

@pytest.fixture
def customer_login(page):
    """
    Reusable Customer Login fixture.

    Any test that needs Customer Login can use:

        def test_example(customer_login):
            page = customer_login

    This avoids repeating Customer Login code
    in every Customer test.
    """

    # ------------------------------------------------------------
    # Customer Login Details
    # ------------------------------------------------------------

    customer_email = "muthyampavanraj333@gmail.com"
    customer_password = "1234567"

    login_url = "https://www.ticksupport.com/tcs/login"

    customer_dashboard_url = (
        "https://www.ticksupport.com/tcs/my/dashboard"
    )

    # ------------------------------------------------------------
    # 1. Open Login Page
    # ------------------------------------------------------------

    page.goto(
        login_url
    )

    # ------------------------------------------------------------
    # 2. Verify Login Page
    # ------------------------------------------------------------

    page.get_by_role(
        "heading",
        name="WELCOME BACK"
    ).wait_for(
        state="visible",
        timeout=10000
    )

    # ------------------------------------------------------------
    # 3. Enter Customer Email
    # ------------------------------------------------------------

    page.locator(
        'input[type="email"]'
    ).fill(
        customer_email
    )

    # ------------------------------------------------------------
    # 4. Enter Customer Password
    # ------------------------------------------------------------

    page.locator(
        'input[type="password"]'
    ).fill(
        customer_password
    )

    # ------------------------------------------------------------
    # 5. Click Sign In
    # ------------------------------------------------------------

    page.get_by_role(
        "button",
        name="Sign In",
        exact=True
    ).click()

    # ------------------------------------------------------------
    # 6. Verify Customer Dashboard
    # ------------------------------------------------------------

    page.wait_for_url(
        customer_dashboard_url,
        timeout=10000
    )

    page.get_by_text(
        "Welcome to Tcs support portal",
        exact=True
    ).wait_for(
        state="visible",
        timeout=10000
    )

    # ------------------------------------------------------------
    # 7. Print Login Information
    # ------------------------------------------------------------

    print()
    print("==============================================")
    print("CUSTOMER LOGIN SUCCESSFUL")
    print("==============================================")
    print(f"Dashboard: {page.url}")
    print("Customer: Muthyam Pavan")
    print("==============================================")

    # ------------------------------------------------------------
    # 8. Return Playwright Page
    # ------------------------------------------------------------

    return page


# ================================================================
# FAILURE SCREENSHOT + HTML REPORT
# ================================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshot and attach current URL
    when a test fails.
    """

    outcome = yield
    report = outcome.get_result()

    # ============================================================
    # Only process actual test execution failures
    # ============================================================

    if report.when == "call" and report.failed:

        # ========================================================
        # Get Playwright page fixture
        # ========================================================

        page = item.funcargs.get("page")

        if page:

            # ====================================================
            # 1. Capture Current Page URL
            # ====================================================

            current_url = page.url

            # ====================================================
            # 2. Take Failure Screenshot
            # ====================================================

            screenshot_path = os.path.join(
                "reports",
                "screenshots",
                f"{item.name}-failure.png"
            )

            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            # ====================================================
            # 3. Get pytest-html Plugin
            # ====================================================

            pytest_html = (
                item.config
                .pluginmanager
                .getplugin("html")
            )

            if (
                pytest_html
                and os.path.exists(screenshot_path)
            ):

                extra = getattr(
                    report,
                    "extras",
                    []
                )

                # =================================================
                # 4. Attach Current URL
                # =================================================

                extra.append(
                    pytest_html.extras.url(
                        current_url,
                        name="Failure Page URL"
                    )
                )

                # =================================================
                # 5. Read Screenshot
                # =================================================

                with open(
                    screenshot_path,
                    "rb"
                ) as image_file:

                    image_data = image_file.read()

                # =================================================
                # 6. Convert Screenshot to Base64
                # =================================================

                image_base64 = base64.b64encode(
                    image_data
                ).decode(
                    "utf-8"
                )

                # =================================================
                # 7. Embed Screenshot in HTML Report
                # =================================================

                extra.append(
                    pytest_html.extras.image(
                        image_base64,
                        mime_type="image/png"
                    )
                )

                report.extras = extra