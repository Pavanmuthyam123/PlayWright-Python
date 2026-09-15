from playwright.sync_api import Page, expect

from pages.ticket_page import TicketPage
from pages.company_ticket_page import CompanyTicketPage
from pages.staff_ticket_page import StaffTicketPage
from pages.customer_ticket_verification_page import (
    CustomerTicketVerificationPage
)


# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "https://www.ticksupport.com"


# ============================================================
# CUSTOMER CREDENTIALS
# ============================================================

CUSTOMER_EMAIL = "muthyampavanraj333@gmail.com"
CUSTOMER_PASSWORD = "1234567"


# ============================================================
# COMPANY CREDENTIALS
# ============================================================

COMPANY_EMAIL = "pavanrajmuthyam@gmail.com"
COMPANY_PASSWORD = "1234567"


# ============================================================
# AGENT CREDENTIALS
# ============================================================

AGENT_EMAIL = "johnagent@gmail.com"
AGENT_PASSWORD = "1234567"


# ============================================================
# TICKET DATA
# ============================================================

TICKET_DESCRIPTION = "SSD Issue"
TICKET_PRIORITY = "High"

AGENT_NAME = "John-Agent"

RESOLUTION_REASON = "Ticket Completed"


# ============================================================
# CUSTOMER VERIFICATION DATA
# ============================================================

CUSTOMER_RATING = 5

CUSTOMER_FEEDBACK = (
    "Thanks for John-Agent. "
    "The ticket was resolved successfully."
)


# ============================================================
# CUSTOMER LOGIN
# ============================================================

def customer_login(page: Page) -> None:
    """
    Login as customer.
    """

    page.goto(
        f"{BASE_URL}/tcs/login"
    )

    expect(
        page.get_by_role(
            "heading",
            name="WELCOME BACK"
        )
    ).to_be_visible(
        timeout=10000
    )

    page.locator(
        'input[type="email"]'
    ).fill(
        CUSTOMER_EMAIL
    )

    page.locator(
        'input[type="password"]'
    ).fill(
        CUSTOMER_PASSWORD
    )

    page.get_by_role(
        "button",
        name="Sign In",
        exact=True
    ).click()

    expect(
        page.get_by_text(
            "Welcome to Tcs support portal",
            exact=True
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        "Customer login successful."
    )


# ============================================================
# COMPANY LOGIN
# ============================================================

def company_login(page: Page) -> None:
    """
    Login as company administrator.

    After customer logout, CI may already be on
    the login page. Therefore, avoid unnecessary
    second navigation to the same URL.
    """

    if not page.url.endswith("/tcs/login"):

        page.goto(
            f"{BASE_URL}/tcs/login",
            wait_until="domcontentloaded",
            timeout=30000
        )

    expect(
        page.get_by_role(
            "heading",
            name="WELCOME BACK"
        )
    ).to_be_visible(
        timeout=10000
    )

    page.locator(
        'input[type="email"]'
    ).fill(
        COMPANY_EMAIL
    )

    page.locator(
        'input[type="password"]'
    ).fill(
        COMPANY_PASSWORD
    )

    page.get_by_role(
        "button",
        name="Sign In",
        exact=True
    ).click()

    expect(
        page.get_by_text(
            "Company Super Admin",
            exact=True
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        "Company login successful."
    )


# ============================================================
# AGENT LOGIN
# ============================================================

def agent_login(page: Page) -> None:
    """
    Login as support agent.

    After company logout, CI may already be on
    the login page. Therefore, avoid unnecessary
    second navigation to the same URL.
    """

    if not page.url.endswith("/tcs/login"):

        page.goto(
            f"{BASE_URL}/tcs/login",
            wait_until="domcontentloaded",
            timeout=30000
        )

    expect(
        page.get_by_role(
            "heading",
            name="WELCOME BACK"
        )
    ).to_be_visible(
        timeout=10000
    )

    page.locator(
        'input[type="email"]'
    ).fill(
        AGENT_EMAIL
    )

    page.locator(
        'input[type="password"]'
    ).fill(
        AGENT_PASSWORD
    )

    page.get_by_role(
        "button",
        name="Sign In",
        exact=True
    ).click()

    expect(
        page.get_by_text(
            AGENT_NAME,
            exact=False
        ).first
    ).to_be_visible(
        timeout=10000
    )

    print(
        "Agent login successful."
    )


# ============================================================
# LOGOUT
# ============================================================

def logout(page: Page) -> None:
    """
    Logout current user.
    """

    profile_button = page.locator(
        "button.topbar-profile-btn"
    )

    expect(
        profile_button
    ).to_be_visible(
        timeout=10000
    )

    profile_button.click()

    sign_out_button = page.get_by_text(
        "Sign out",
        exact=True
    )

    expect(
        sign_out_button
    ).to_be_visible(
        timeout=5000
    )

    sign_out_button.click()

    page.wait_for_url(
        "**/tcs/login",
        timeout=10000
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
        "Logout successful."
    )


# ============================================================
# COMPLETE TICKET E2E
# ============================================================

def test_complete_ticket_e2e(page: Page):
    """
    Complete ticket lifecycle:

    Customer
        ↓
    Create Ticket
        ↓
    Company
        ↓
    Assign Ticket to John-Agent
        ↓
    Agent
        ↓
    Resolve Ticket
        ↓
    Customer
        ↓
    Verify Resolved Ticket
        ↓
    Submit Rating and Feedback
    """

    # ========================================================
    # STAGE 1
    # CUSTOMER CREATES TICKET
    # ========================================================

    print(
        "\n=============================================="
    )

    print(
        "STAGE 1 - CUSTOMER CREATES TICKET"
    )

    print(
        "=============================================="
    )

    # --------------------------------------------------------
    # Customer Login
    # --------------------------------------------------------

    customer_login(
        page
    )

    # --------------------------------------------------------
    # Create Ticket
    # --------------------------------------------------------

    ticket_page = TicketPage(
        page
    )

    ticket_page.click_new_ticket()

    ticket_page.select_ticket_type()

    ticket_page.enter_description(
        TICKET_DESCRIPTION
    )

    ticket_page.select_priority(
        TICKET_PRIORITY
    )

    ticket_page.create_ticket()

    print(
        "\nCustomer ticket created."
    )

    # --------------------------------------------------------
    # Open My Tickets
    # --------------------------------------------------------

    page.goto(
        f"{BASE_URL}/tcs/my/tickets"
    )

    # Wait until loading disappears
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

    # --------------------------------------------------------
    # Verify Ticket Description
    # --------------------------------------------------------

    expect(
        page.get_by_text(
            TICKET_DESCRIPTION,
            exact=True
        ).first
    ).to_be_visible(
        timeout=10000
    )

    # --------------------------------------------------------
    # Get Dynamic Ticket Number
    # --------------------------------------------------------

    ticket_number = ticket_page.get_ticket_number(
        TICKET_DESCRIPTION
    )

    print(
        f"\nGenerated Ticket Number: {ticket_number}"
    )

    print(
        f"Created Ticket: {ticket_number}"
    )

    # --------------------------------------------------------
    # Customer Logout
    # --------------------------------------------------------

    logout(
        page
    )


    # ========================================================
    # STAGE 2
    # COMPANY ASSIGNS TICKET
    # ========================================================

    print(
        "\n=============================================="
    )

    print(
        "STAGE 2 - COMPANY ASSIGNS TICKET"
    )

    print(
        "=============================================="
    )

    # --------------------------------------------------------
    # Company Login
    # --------------------------------------------------------

    company_login(
        page
    )

    # --------------------------------------------------------
    # Company Ticket Page
    # --------------------------------------------------------

    company_ticket_page = CompanyTicketPage(
        page
    )

    company_ticket_page.open_tickets()

    print(
        "Company Tickets page opened."
    )

    # --------------------------------------------------------
    # Open Same Dynamic Ticket
    # --------------------------------------------------------

    company_ticket_page.open_ticket(
        ticket_number
    )

    print(
        f"Opened ticket: {ticket_number}"
    )

    # --------------------------------------------------------
    # Verify Ticket Number
    # --------------------------------------------------------

    expect(
        page.get_by_text(
            ticket_number,
            exact=False
        ).first
    ).to_be_visible(
        timeout=10000
    )

    # --------------------------------------------------------
    # Verify Ticket Description
    # --------------------------------------------------------

    expect(
        page.get_by_text(
            TICKET_DESCRIPTION,
            exact=True
        ).first
    ).to_be_visible(
        timeout=10000
    )

    print(
        f"Ticket verified: {ticket_number}"
    )

    print(
        f"Description verified: {TICKET_DESCRIPTION}"
    )

    # --------------------------------------------------------
    # Verify Initial Assignment
    # --------------------------------------------------------

    assigned_to_label = page.get_by_text(
        "Assigned To",
        exact=True
    )

    expect(
        assigned_to_label
    ).to_be_visible(
        timeout=10000
    )

    assigned_to_row = assigned_to_label.locator(
        "xpath=.."
    )

    expect(
        assigned_to_row.get_by_text(
            "Unassigned",
            exact=True
        )
    ).to_be_visible(
        timeout=10000
    )

    print(
        f"{ticket_number} is currently Unassigned."
    )

    # --------------------------------------------------------
    # Assign Ticket to John-Agent
    # --------------------------------------------------------

    company_ticket_page.assign_new_ticket_to_john()

    print(
        f"Ticket assigned to {AGENT_NAME}."
    )

    # --------------------------------------------------------
    # Verify Assignment
    # --------------------------------------------------------

    company_ticket_page.verify_john_agent_assigned()

    print(
        f"Assignment verified: {AGENT_NAME}"
    )

    # --------------------------------------------------------
    # Company Logout
    # --------------------------------------------------------

    company_ticket_page.logout()

    print(
        "Company logout verified."
    )


    # ========================================================
    # STAGE 3
    # AGENT RESOLVES TICKET
    # ========================================================

    print(
        "\n=============================================="
    )

    print(
        "STAGE 3 - AGENT RESOLVES TICKET"
    )

    print(
        "=============================================="
    )

    # --------------------------------------------------------
    # Agent Login
    # --------------------------------------------------------

    agent_login(
        page
    )

    # --------------------------------------------------------
    # Staff Ticket Page
    # --------------------------------------------------------

    staff_ticket_page = StaffTicketPage(
        page
    )

    # --------------------------------------------------------
    # Open My Tickets
    # --------------------------------------------------------

    staff_ticket_page.open_my_tickets()

    print(
        "Agent My Tickets page opened."
    )

    # --------------------------------------------------------
    # Open Same Dynamic Ticket
    # --------------------------------------------------------

    staff_ticket_page.open_ticket(
        ticket_number
    )

    print(
        f"Opened Agent Ticket: {ticket_number}"
    )

    # --------------------------------------------------------
    # Verify Ticket Details
    # --------------------------------------------------------

    staff_ticket_page.verify_ticket_details(
        ticket_number=ticket_number,
        ticket_description=TICKET_DESCRIPTION
    )

    print(
        f"Ticket details verified: {ticket_number}"
    )

    # --------------------------------------------------------
    # Resolve Ticket
    # --------------------------------------------------------

    staff_ticket_page.resolve_ticket(
        reason=RESOLUTION_REASON
    )

    print(
        f"Resolution reason entered: {RESOLUTION_REASON}"
    )

    # --------------------------------------------------------
    # Verify Resolved Status
    # --------------------------------------------------------

    staff_ticket_page.verify_resolved_status()

    print(
        f"Ticket status verified: Resolved"
    )

    # --------------------------------------------------------
    # Agent Logout
    # --------------------------------------------------------

    logout(
        page
    )

    print(
        "Agent logout verified."
    )


    # ========================================================
    # STAGE 4
    # CUSTOMER VERIFIES AND RATES
    # ========================================================

    print(
        "\n=============================================="
    )

    print(
        "STAGE 4 - CUSTOMER VERIFIES AND RATES"
    )

    print(
        "=============================================="
    )

    # --------------------------------------------------------
    # Customer Login Again
    # --------------------------------------------------------

    customer_login(
        page
    )

    # --------------------------------------------------------
    # Customer Ticket Verification Page
    # --------------------------------------------------------

    customer_ticket_page = (
        CustomerTicketVerificationPage(
            page
        )
    )

    # --------------------------------------------------------
    # Open My Tickets
    # --------------------------------------------------------

    customer_ticket_page.open_my_tickets()

    print(
        "Customer My Tickets page opened."
    )

    # --------------------------------------------------------
    # Open Same Dynamic Ticket
    # --------------------------------------------------------

    customer_ticket_page.open_ticket(
        ticket_number
    )

    print(
        f"Customer ticket opened: {ticket_number}"
    )

    # --------------------------------------------------------
    # Verify Ticket
    # --------------------------------------------------------

    customer_ticket_page.verify_ticket(
        ticket_number=ticket_number,
        ticket_description=TICKET_DESCRIPTION
    )

    print(
        f"Ticket verified: {ticket_number}"
    )

    print(
        f"Description verified: {TICKET_DESCRIPTION}"
    )

    # --------------------------------------------------------
    # Verify Resolved Status
    # --------------------------------------------------------

    customer_ticket_page.verify_resolved_status()

    print(
        "Customer verified ticket status: Resolved"
    )

    # --------------------------------------------------------
    # Open Rate Support
    # --------------------------------------------------------

    customer_ticket_page.open_rate_support()

    print(
        "Rate Support opened."
    )

    # --------------------------------------------------------
    # Select Rating
    # --------------------------------------------------------

    customer_ticket_page.select_rating(
        CUSTOMER_RATING
    )

    print(
        f"Customer rating selected: "
        f"{CUSTOMER_RATING}/5"
    )

    # --------------------------------------------------------
    # Enter Feedback
    # --------------------------------------------------------

    customer_ticket_page.enter_feedback(
        CUSTOMER_FEEDBACK
    )

    print(
        f"Customer feedback entered: "
        f"{CUSTOMER_FEEDBACK}"
    )

    # --------------------------------------------------------
    # Submit Rating
    # --------------------------------------------------------

    customer_ticket_page.submit_rating()

    print(
        "Customer rating submitted."
    )

    # --------------------------------------------------------
    # Final Customer Logout
    # --------------------------------------------------------

    logout(
        page
    )

    print(
        "Customer logout verified."
    )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    print(
        "\n=================================================="
    )

    print(
        "COMPLETE TICKET E2E PASSED"
    )

    print(
        "=================================================="
    )

    print(
        f"Ticket      : {ticket_number}"
    )

    print(
        f"Description : {TICKET_DESCRIPTION}"
    )

    print(
        f"Assigned To : {AGENT_NAME}"
    )

    print(
        "Status      : Resolved"
    )

    print(
        f"Rating      : {CUSTOMER_RATING}/5"
    )

    print(
        f"Feedback    : {CUSTOMER_FEEDBACK}"
    )

    print(
        "Result      : PASS"
    )

    print(
        "=================================================="
    )