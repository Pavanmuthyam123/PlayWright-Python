from playwright.sync_api import Page, expect

from pages.company_ticket_page import CompanyTicketPage


# ================================================================
# EXISTING TEST
# COMPANY TICKET REASSIGNMENT
# ================================================================

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

    ticket_number = "TCS-000014"

    ticket_description = "SSD Issue"

    current_agent = "Agent-Kim"

    new_agent = "John-Agent"

    # ============================================================
    # 1. OPEN COMPANY LOGIN PAGE
    # ============================================================

    page.goto(
        "https://www.ticksupport.com/tcs/login"
    )

    # ============================================================
    # 2. VERIFY LOGIN PAGE
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
    # 3. ENTER COMPANY EMAIL
    # ============================================================

    page.locator(
        'input[type="email"]'
    ).fill(
        "pavanrajmuthyam@gmail.com"
    )

    # ============================================================
    # 4. ENTER COMPANY PASSWORD
    # ============================================================

    page.locator(
        'input[type="password"]'
    ).fill(
        "1234567"
    )

    # ============================================================
    # 5. SIGN IN
    # ============================================================

    page.get_by_role(
        "button",
        name="Sign In",
        exact=True
    ).click()

    # ============================================================
    # 6. VERIFY COMPANY DASHBOARD
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
    # 7. INITIALIZE COMPANY TICKET PAGE OBJECT
    # ============================================================

    company_ticket_page = CompanyTicketPage(
        page
    )

    # ============================================================
    # 8. OPEN TICKETS
    # ============================================================

    company_ticket_page.open_tickets()

    print(
        "\nCompany Tickets page opened."
    )

    # ============================================================
    # 9. OPEN EXISTING TICKET
    # ============================================================

    company_ticket_page.open_ticket(
        ticket_number
    )

    print(
        f"\nOpened Ticket: {ticket_number}"
    )

    # ============================================================
    # 10. VERIFY TICKET NUMBER
    # ============================================================

    expect(
        page.get_by_text(
            ticket_number,
            exact=False
        ).first
    ).to_be_visible(
        timeout=10000
    )

    # ============================================================
    # 11. VERIFY TICKET TITLE
    # ============================================================

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
    # 12. VERIFY CURRENT ASSIGNED AGENT
    # ============================================================

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
    # 13. REASSIGN TICKET TO JOHN-AGENT
    # ============================================================

    company_ticket_page.reassign_ticket_to_john()

    print(
        f"\nTicket reassignment completed to {new_agent}."
    )

    # ============================================================
    # 14. VERIFY NEW ASSIGNED AGENT
    # ============================================================

    company_ticket_page.verify_john_agent_assigned()

    print(
        f"New assigned agent verified: {new_agent}"
    )

    # ============================================================
    # 15. LOGOUT
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


# ================================================================
# NEW TEST
# COMPANY FRESH TICKET ASSIGNMENT
# ================================================================

def test_company_assign_new_ticket_to_john(
    company_login
):
    """
    Company-side Fresh Ticket Assignment Test.

    Business Scenario:

        TCS-000015
            ↓
        Status = Open
            ↓
        Assigned To = Unassigned
            ↓
        Click Assign Agent
            ↓
        Choose John-Agent
            ↓
        Click Assign Ticket
            ↓
        Verify John-Agent
    """

    # ============================================================
    # TEST DATA
    # ============================================================

    ticket_number = "TCS-000015"

    ticket_description = "SSD Issue"

    new_agent = "John-Agent"

    # ============================================================
    # 1. COMPANY LOGIN
    # ============================================================
    #
    # Reusable company_login fixture handles:
    #
    # Login page
    # Email
    # Password
    # Sign In
    # Dashboard verification
    #
    # ============================================================

    page = company_login

    print(
        "\nCompany dashboard verified through fixture."
    )

    # ============================================================
    # 2. CREATE COMPANY TICKET PAGE OBJECT
    # ============================================================

    company_ticket_page = CompanyTicketPage(
        page
    )

    # ============================================================
    # 3. OPEN TICKETS
    # ============================================================

    company_ticket_page.open_tickets()

    print(
        "\nCompany Tickets page opened."
    )

    # ============================================================
    # 4. OPEN FRESH TICKET
    # ============================================================

    company_ticket_page.open_ticket(
        ticket_number
    )

    print(
        f"\nOpened fresh ticket: {ticket_number}"
    )

    # ============================================================
    # 5. VERIFY TICKET NUMBER
    # ============================================================

    expect(
        page.get_by_text(
            ticket_number,
            exact=False
        ).first
    ).to_be_visible(
        timeout=10000
    )

    print(
        f"Ticket number verified: {ticket_number}"
    )

    # ============================================================
    # 6. VERIFY TICKET DESCRIPTION
    # ============================================================

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
        f"Ticket description verified: {ticket_description}"
    )

    # ============================================================
    # 7. VERIFY TICKET IS CURRENTLY UNASSIGNED
    # ============================================================

    expect(
        page.get_by_text(
            "Unassigned",
            exact=True
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        "Current assignment verified: Unassigned"
    )

    # ============================================================
    # 8. ASSIGN FRESH TICKET TO JOHN-AGENT
    # ============================================================

    company_ticket_page.assign_new_ticket_to_john()

    print(
        f"\nFresh ticket assigned to {new_agent}."
    )

    # ============================================================
    # 9. VERIFY JOHN-AGENT ASSIGNMENT
    # ============================================================

    company_ticket_page.verify_john_agent_assigned()

    print(
        f"New assigned agent verified: {new_agent}"
    )

    # ============================================================
    # FINAL RESULT
    # ============================================================

    print(
        "\n=============================================="
    )

    print(
        "FRESH TICKET ASSIGNMENT PASSED"
    )

    print(
        f"Ticket : {ticket_number}"
    )

    print(
        "Status : Open"
    )

    print(
        f"Assigned To : {new_agent}"
    )

    print(
        "Result : PASS"
    )

    print(
        "=============================================="
    )