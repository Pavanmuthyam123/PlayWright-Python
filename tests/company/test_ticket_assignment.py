from playwright.sync_api import Page, expect

from pages.company_ticket_page import CompanyTicketPage


def test_company_reassign_ticket_to_john(page: Page):
    """
    Company-side Ticket Reassignment Test.

    Business Scenario:

        TCS-000014
            ↓
        Currently assigned to Agent-Kim
            ↓
        Click Reassign
            ↓
        Choose an agent
            ↓
        Select John-Agent
            ↓
        Assign Ticket
            ↓
        Verify John-Agent
            ↓
        Logout
    """

    # ============================================================
    # TEST DATA
    # ============================================================

    # Existing ticket used for the current business scenario.
    ticket_number = "TCS-000014"

    # Ticket description.
    ticket_description = "SSD Issue"

    # Current assigned agent.
    current_agent = "Agent-Kim"

    # New assigned agent.
    new_agent = "John-Agent"

    # ============================================================
    # 1. Open Company Login Page
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
    # 3. Enter Company Email
    # ============================================================

    page.locator(
        'input[type="email"]'
    ).fill(
        "pavanrajmuthyam@gmail.com"
    )

    # ============================================================
    # 4. Enter Company Password
    # ============================================================

    page.locator(
        'input[type="password"]'
    ).fill(
        "1234567"
    )

    # ============================================================
    # 5. Sign In
    # ============================================================

    page.get_by_role(
        "button",
        name="Sign In",
        exact=True
    ).click()

    # ============================================================
    # 6. Verify Company Dashboard
    # ============================================================

    expect(
        page
    ).to_have_url(
        "https://www.ticksupport.com/tcs/dashboard",
        timeout=10000
    )

    expect(
        page.get_by_text(
            "Company Super Admin",
            exact=True
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        "\nCompany Dashboard opened successfully."
    )

    # ============================================================
    # 7. Initialize Company Ticket Page Object
    # ============================================================

    company_ticket_page = CompanyTicketPage(
        page
    )

    # ============================================================
    # 8. Open Tickets
    # ============================================================

    company_ticket_page.open_tickets()

    print(
        "\nCompany Tickets page opened."
    )

    # ============================================================
    # 9. Open Existing Ticket
    # ============================================================

    company_ticket_page.open_ticket(
        ticket_number
    )

    print(
        f"\nOpened Ticket: {ticket_number}"
    )

    # ============================================================
    # 10. Verify Ticket Number
    # ============================================================

    # IMPORTANT:
    # TCS-000014 is normal text on the page,
    # NOT a heading.
    # Use .first to avoid strict mode violation
    # (multiple elements match).
    expect(
        page.get_by_text(
            ticket_number,
            exact=False
        ).first
    ).to_be_visible(
        timeout=10000
    )

    # ============================================================
    # 11. Verify Ticket Title
    # ============================================================

    # "SSD Issue" is the actual H1 heading.
    expect(
        page.get_by_role(
            "heading",
            name=ticket_description,
            exact=True
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        f"Ticket detail verified: {ticket_number}"
    )

    # ============================================================
    # 12. Verify Current Assigned Agent
    # ============================================================

    # Use .first to avoid strict mode if multiple matches
    expect(
        page.get_by_text(
            current_agent,
            exact=True
        ).first
    ).to_be_visible(
        timeout=10000
    )

    print(
        f"Current agent verified: {current_agent}"
    )

    # ============================================================
    # 14. Reassign Ticket to John-Agent
    # ============================================================

    company_ticket_page.reassign_ticket_to_john()

    print(
        f"\nTicket reassignment completed to {new_agent}."
    )

    # ============================================================
    # 15. Verify New Assigned Agent
    # ============================================================

    company_ticket_page.verify_john_agent_assigned()

    print(
        f"New assigned agent verified: {new_agent}"
    )

    # ============================================================
    # 16. Logout
    # ============================================================

    company_ticket_page.logout()

    # ============================================================
    # FINAL RESULT
    # ============================================================

    print(
        "\n=============================================="
    )

    print(
        "COMPANY TICKET REASSIGNMENT COMPLETED"
    )

    print(
        f"Ticket : {ticket_number}"
    )

    print(
        f"From   : {current_agent}"
    )

    print(
        f"To     : {new_agent}"
    )

    print(
        "=============================================="
    )