import os
import base64

import pytest


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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshot and attach current URL
    when a test fails.
    """

    outcome = yield
    report = outcome.get_result()

    # Only process actual test execution failures
    if report.when == "call" and report.failed:

        # Get Playwright page fixture
        page = item.funcargs.get("page")

        if page:

            # -----------------------------------
            # 1. Capture current page URL
            # -----------------------------------

            current_url = page.url

            # -----------------------------------
            # 2. Take failure screenshot
            # -----------------------------------

            screenshot_path = os.path.join(
                "reports",
                "screenshots",
                f"{item.name}-failure.png"
            )

            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            # -----------------------------------
            # 3. Get pytest-html plugin
            # -----------------------------------

            pytest_html = item.config.pluginmanager.getplugin("html")

            if pytest_html and os.path.exists(screenshot_path):

                extra = getattr(
                    report,
                    "extras",
                    []
                )

                # -----------------------------------
                # 4. Attach current URL
                # -----------------------------------

                extra.append(
                    pytest_html.extras.url(
                        current_url,
                        name="Failure Page URL"
                    )
                )

                # -----------------------------------
                # 5. Read screenshot
                # -----------------------------------

                with open(
                    screenshot_path,
                    "rb"
                ) as image_file:

                    image_data = image_file.read()

                # -----------------------------------
                # 6. Convert screenshot to Base64
                # -----------------------------------

                image_base64 = base64.b64encode(
                    image_data
                ).decode("utf-8")

                # -----------------------------------
                # 7. Embed screenshot in HTML report
                # -----------------------------------

                extra.append(
                    pytest_html.extras.image(
                        image_base64,
                        mime_type="image/png"
                    )
                )

                report.extras = extra