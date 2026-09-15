from playwright.sync_api import Page, expect

from pages.company_ticket_page import CompanyTicketPage


# ================================================================
# TEST DATA
# ================================================================

COMPANY_EMAIL = "pavanrajmuthyam@gmail.com"
COMPANY_PASSWORD = "1234567"

AGENT_NAME = "John-Agent"

# Already existing ticket
TICKET_NUMBER = "TCS-000038"
TICKET_DESCRIPTION = "Fresh Assignment Test 1789484663"


# ================================================================
# COMPANY LOGIN
# ================================================================

def login_company(page: Page) -> None:

    page.goto(
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

    # Enter email
    page.locator(
        'input[type="email"]'
    ).fill(
        COMPANY_EMAIL
    )

    # Enter password
    page.locator(
        'input[type="password"]'
    ).fill(
        COMPANY_PASSWORD
    )

    # Click Sign In
    page.get_by_role(
        "button",
        name="Sign In",
        exact=True
    ).click()

    # Verify Company Dashboard
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
        "\nCompany login successful."
    )


# ================================================================
# COMPANY TICKET ASSIGNMENT
# ================================================================

def test_company_assign_new_ticket_to_john(
    page: Page
):
    """
    Company Ticket Assignment.

    Existing Ticket
            ↓
    Company Login
            ↓
    Open Tickets
            ↓
    Open Ticket
            ↓
    Assign Agent
            ↓
    John-Agent
            ↓
    Verify John-Agent
            ↓
    Company Logout
    """

    # ============================================================
    # 1. COMPANY LOGIN
    # ============================================================

    login_company(page)

    # ============================================================
    # 2. CREATE COMPANY PAGE OBJECT
    # ============================================================

    company_ticket_page = CompanyTicketPage(
        page
    )

    # ============================================================
    # 3. OPEN COMPANY TICKETS
    # ============================================================

    company_ticket_page.open_tickets()

    print(
        "Company Tickets page opened."
    )

    # ============================================================
    # 4. OPEN EXISTING TICKET
    # ============================================================

    company_ticket_page.open_ticket(
        TICKET_NUMBER
    )

    print(
        f"Opened ticket: {TICKET_NUMBER}"
    )

    # ============================================================
    # 5. VERIFY TICKET NUMBER
    # ============================================================

    expect(
        page.get_by_text(
            TICKET_NUMBER,
            exact=False
        ).first
    ).to_be_visible(
        timeout=10000
    )

    # ============================================================
    # 6. VERIFY TICKET DESCRIPTION
    # ============================================================

    expect(
        page.get_by_role(
            "heading",
            name=TICKET_DESCRIPTION,
            exact=True
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        f"Ticket verified: {TICKET_NUMBER}"
    )

    # ============================================================
    # 7. ASSIGN JOHN-AGENT
    # ============================================================

    company_ticket_page.assign_new_ticket_to_john()

    print(
        f"Ticket assigned to {AGENT_NAME}."
    )

    # ============================================================
    # 8. VERIFY JOHN-AGENT
    # ============================================================

    company_ticket_page.verify_john_agent_assigned()

    print(
        f"Assignment verified: {AGENT_NAME}"
    )

    # ============================================================
    # 9. LOGOUT COMPANY
    # ============================================================

    company_ticket_page.logout()

    # ============================================================
    # FINAL RESULT
    # ============================================================

    print(
        "\n=============================================="
    )

    print(
        "COMPANY TICKET ASSIGNMENT PASSED"
    )

    print(
        "=============================================="
    )

    print(
        f"Ticket      : {TICKET_NUMBER}"
    )

    print(
        f"Assigned To : {AGENT_NAME}"
    )

    print(
        "Logout      : Successful"
    )

    print(
        "=============================================="
    )