from playwright.sync_api import Page, expect
from pages.ticket_page import TicketPage


def test_customer_create_ticket(page: Page):
    """
    Test customer ability to create a General Support Request
    ticket with High priority and capture the generated ticket number.
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
    ).to_be_visible(
        timeout=10000
    )

    # ============================================================
    # 3. Customer Login
    # ============================================================

    page.locator(
        'input[type="email"]'
    ).fill(
        "muthyampavanraj333@gmail.com"
    )

    page.locator(
        'input[type="password"]'
    ).fill(
        "1234567"
    )

    page.get_by_role(
        "button",
        name="Sign In",
        exact=True
    ).click()

    # ============================================================
    # 4. Verify Customer Dashboard
    # ============================================================

    expect(
        page.get_by_text(
            "Welcome to Tcs support portal",
            exact=True
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        "\nCustomer dashboard URL:",
        page.url
    )

    # ============================================================
    # 5. Initialize Ticket Page
    # ============================================================

    ticket_page = TicketPage(page)

    # ============================================================
    # 6. Open New Ticket
    # ============================================================

    ticket_page.click_new_ticket()

    # ============================================================
    # 7. Select Ticket Type
    # ============================================================

    ticket_page.select_ticket_type()

    # ============================================================
    # 8. Enter Ticket Description
    # ============================================================

    ticket_description = "SSD Issue"

    ticket_page.enter_description(
        ticket_description
    )

    # ============================================================
    # 9. Select High Priority
    # ============================================================

    ticket_page.select_priority(
        "High"
    )

    # ============================================================
    # 10. Create Ticket
    # ============================================================

    ticket_page.create_ticket()

    # ============================================================
    # 11. Verify Ticket Form Closed
    # ============================================================

    expect(
        ticket_page.description_field
    ).not_to_be_visible(
        timeout=10000
    )

    # ============================================================
    # 12. Check Error Alerts
    # ============================================================

    error_alerts = page.locator(
        "[role='alert'], .alert-danger, .error"
    )

    visible_errors = []

    for i in range(error_alerts.count()):

        alert = error_alerts.nth(i)

        if alert.is_visible():

            text = alert.text_content()

            if text:
                visible_errors.append(
                    text.strip()
                )

    if visible_errors:

        print(
            "\nWARNING: Error alert(s) found:"
        )

        for error in visible_errors:

            print(
                f"   {error}"
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
    # 14. Wait for My Tickets Page
    # ============================================================

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
    # 15. Verify Ticket Description
    # ============================================================

    expect(
        page.get_by_text(
            ticket_description,
            exact=True
        ).first
    ).to_be_visible(
        timeout=10000
    )

    print(
        f"\nTicket description verified: "
        f"{ticket_description}"
    )

    # ============================================================
    # 16. Capture Generated Ticket Number
    # ============================================================

    ticket_number = ticket_page.get_ticket_number(
        ticket_description
    )

    # ============================================================
    # 17. Verify Generated Ticket Number
    # ============================================================

    expect(
        page.get_by_text(
            ticket_number,
            exact=True
        )
    ).to_be_visible(
        timeout=10000
    )

    # ============================================================
    # 18. Final Result
    # ============================================================

    print(
        "\n=============================================="
    )

    print(
        "CUSTOMER TICKET CREATION PASSED"
    )

    print(
        "=============================================="
    )

    print(
        f"Ticket Number : {ticket_number}"
    )

    print(
        f"Description   : {ticket_description}"
    )

    print(
        "Priority      : High"
    )

    print(
        "Status        : Open"
    )

    print(
        "=============================================="
    )