from playwright.sync_api import Page, expect
from pages.ticket_page import TicketPage


def test_customer_create_ticket(page: Page):
    """
    Test customer ability to create a General Support Request
    ticket with High priority.
    """

    # ============================================================
    # 1. Open Customer Login Page
    # ============================================================

    page.goto(
        "https://www.ticksupport.com/tcs/login"
    )

    # ============================================================
    # 2. Verify Login Page
    # ============================================================

    expect(
        page.get_by_role(
            "heading",
            name="WELCOME BACK"
        )
    ).to_be_visible()

    # ============================================================
    # 3. Enter Customer Email
    # ============================================================

    page.locator(
        'input[type="email"]'
    ).fill(
        "muthyampavanraj333@gmail.com"
    )

    # ============================================================
    # 4. Enter Customer Password
    # ============================================================

    page.locator(
        'input[type="password"]'
    ).fill(
        "1234567"
    )

    # ============================================================
    # 5. Click Sign In
    # ============================================================

    page.get_by_role(
        "button",
        name="Sign In"
    ).click()

    # ============================================================
    # 6. Verify Customer Dashboard
    # ============================================================
    # Verify that login successfully reached the customer portal.
    # We avoid depending only on one exact URL.

    expect(
        page.get_by_text(
            "Welcome to Tcs support portal"
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        "\nCustomer dashboard URL:",
        page.url
    )

    # ============================================================
    # 7. Initialize Ticket Page Object
    # ============================================================
    # TicketPage contains locators and actions for
    # the Customer Create Ticket module.

    ticket_page = TicketPage(page)

    # ============================================================
    # 8. Open New Ticket
    # ============================================================

    ticket_page.click_new_ticket()

    # ============================================================
    # 9. Select Ticket Type
    # ============================================================

    ticket_page.select_ticket_type()

    # ============================================================
    # 10. Enter Ticket Description
    # ============================================================

    ticket_description = "SSD Issue"

    ticket_page.enter_description(
        ticket_description
    )

    # ============================================================
    # 11. Select High Priority
    # ============================================================

    ticket_page.select_priority(
        "High"
    )

    # ============================================================
    # 12. Submit Ticket
    # ============================================================

    ticket_page.create_ticket()

    # ============================================================
    # 12a. Verify Ticket Creation Success
    # ============================================================
    # After successful submission, the ticket form should
    # no longer be visible.

    expect(
        ticket_page.description_field
    ).not_to_be_visible(
        timeout=10000
    )

    # ============================================================
    # 12b. Check for Error Messages
    # ============================================================
    # Check whether any error alert is displayed after
    # ticket submission.

    error_alerts = page.locator(
        "[role='alert'], .alert-danger, .error"
    )

    error_count = error_alerts.count()

    if error_count > 0:
        print(
            f"\nWARNING: Found {error_count} error alert(s) "
            "after ticket creation"
        )

        for i in range(error_count):
            error_text = error_alerts.nth(i).text_content()

            print(
                f"   Error {i + 1}: {error_text}"
            )

    else:
        print(
            "\nNo error alerts found after ticket creation."
        )

    # ============================================================
    # 13. Navigate to My Tickets
    # ============================================================

    page.goto(
        "https://www.ticksupport.com/tcs/my/tickets"
    )

    # ============================================================
    # 13a. Wait for Tickets Page to Load
    # ============================================================
    # The Tickets page loads ticket data asynchronously.

    page.locator(
        "text=Loading"
    ).wait_for(
        state="hidden",
        timeout=30000
    )

    page.wait_for_load_state(
        "networkidle",
        timeout=30000
    )

    # ============================================================
    # 14. Verify Created Ticket
    # ============================================================
    # Verify that the newly created ticket description
    # is displayed in My Tickets.

    expect(
        page.get_by_text(
            ticket_description,
            exact=True
        ).first
    ).to_be_visible(
        timeout=10000
    )

    print(
        f"\nTicket created successfully: {ticket_description}"
    )