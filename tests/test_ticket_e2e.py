from playwright.sync_api import Page, expect

from pages.ticket_page import TicketPage
from pages.company_ticket_page import CompanyTicketPage
from pages.staff_ticket_page import StaffTicketPage
from pages.customer_ticket_verification_page import (
    CustomerTicketVerificationPage
)


BASE_URL = "https://www.ticksupport.com"

CUSTOMER_EMAIL = "muthyampavanraj333@gmail.com"
CUSTOMER_PASSWORD = "1234567"

COMPANY_EMAIL = "pavanrajmuthyam@gmail.com"
COMPANY_PASSWORD = "1234567"

AGENT_EMAIL = "johnagent@gmail.com"
AGENT_PASSWORD = "1234567"

TICKET_DESCRIPTION = "SSD Issue"
TICKET_PRIORITY = "High"
AGENT_NAME = "John-Agent"
RESOLUTION_REASON = "Ticket Completed"

CUSTOMER_RATING = 5
CUSTOMER_FEEDBACK = (
    "Thanks for John-Agent. "
    "The ticket was resolved successfully."
)


def customer_login(page: Page) -> None:
    """Login as customer."""

    page.goto(f"{BASE_URL}/tcs/login")

    expect(
        page.get_by_role(
            "heading",
            name="WELCOME BACK"
        )
    ).to_be_visible(timeout=10000)

    page.locator(
        'input[type="email"]'
    ).fill(CUSTOMER_EMAIL)

    page.locator(
        'input[type="password"]'
    ).fill(CUSTOMER_PASSWORD)

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
    ).to_be_visible(timeout=10000)

    print("\nCustomer login successful.")


def company_login(page: Page) -> None:
    """Login as company administrator."""

    page.goto(f"{BASE_URL}/tcs/login")

    expect(
        page.get_by_role(
            "heading",
            name="WELCOME BACK"
        )
    ).to_be_visible(timeout=10000)

    page.locator(
        'input[type="email"]'
    ).fill(COMPANY_EMAIL)

    page.locator(
        'input[type="password"]'
    ).fill(COMPANY_PASSWORD)

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
    ).to_be_visible(timeout=10000)

    print("Company login successful.")


def agent_login(page: Page) -> None:
    """Login as support agent."""

    page.goto(f"{BASE_URL}/tcs/login")

    expect(
        page.get_by_role(
            "heading",
            name="WELCOME BACK"
        )
    ).to_be_visible(timeout=10000)

    page.locator(
        'input[type="email"]'
    ).fill(AGENT_EMAIL)

    page.locator(
        'input[type="password"]'
    ).fill(AGENT_PASSWORD)

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
    ).to_be_visible(timeout=10000)

    print("Agent login successful.")


def logout(page: Page) -> None:
    """Logout current user."""

    profile_button = page.locator(
        "button.topbar-profile-btn"
    )

    expect(
        profile_button
    ).to_be_visible(timeout=10000)

    profile_button.click()

    sign_out_button = page.get_by_text(
        "Sign out",
        exact=True
    )

    expect(
        sign_out_button
    ).to_be_visible(timeout=5000)

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
    ).to_be_visible(timeout=10000)

    print("Logout successful.")


def test_complete_ticket_e2e(page: Page):
    """
    Complete ticket lifecycle:

    Customer
        → Create Ticket

    Company
        → Assign Ticket to John-Agent

    Agent
        → Resolve Ticket

    Customer
        → Verify Resolved Ticket
        → Submit Rating and Feedback
    """

    # ============================================================
    # STAGE 1 — CUSTOMER CREATES TICKET
    # ============================================================

    print(
        "\n=============================================="
    )
    print(
        "STAGE 1 - CUSTOMER CREATES TICKET"
    )
    print(
        "=============================================="
    )

    customer_login(page)

    ticket_page = TicketPage(page)

    ticket_page.click_new_ticket()

    ticket_page.select_ticket_type()

    ticket_page.enter_description(
        TICKET_DESCRIPTION
    )

    ticket_page.select_priority(
        TICKET_PRIORITY
    )

    ticket_page.create_ticket()

    # Open My Tickets
    page.goto(
        f"{BASE_URL}/tcs/my/tickets"
    )

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

    # Verify description
    expect(
        page.get_by_text(
            TICKET_DESCRIPTION,
            exact=True
        ).first
    ).to_be_visible(timeout=10000)

    # Capture generated ticket number
    ticket_number = ticket_page.get_ticket_number(
        TICKET_DESCRIPTION
    )

    print(
        f"\nCreated Ticket: {ticket_number}"
    )

    # Logout customer
    logout(page)

    # ============================================================
    # STAGE 2 — COMPANY ASSIGNS TICKET
    # ============================================================

    print(
        "\n=============================================="
    )
    print(
        "STAGE 2 - COMPANY ASSIGNS TICKET"
    )
    print(
        "=============================================="
    )

    company_login(page)

    company_ticket_page = CompanyTicketPage(page)

    company_ticket_page.open_tickets()

    company_ticket_page.open_ticket(
        ticket_number
    )

    # Verify ticket
    expect(
        page.get_by_text(
            ticket_number,
            exact=False
        ).first
    ).to_be_visible(timeout=10000)

    expect(
        page.get_by_text(
            TICKET_DESCRIPTION,
            exact=True
        ).first
    ).to_be_visible(timeout=10000)

    # Fresh ticket should be unassigned
    expect(
        page.get_by_text(
            "Unassigned",
            exact=True
        )
    ).to_be_visible(timeout=10000)

    # Assign to John-Agent
    company_ticket_page.assign_new_ticket_to_john()

    # Verify assignment
    company_ticket_page.verify_john_agent_assigned()

    print(
        f"\n{ticket_number} assigned to {AGENT_NAME}."
    )

    # Logout company
    company_ticket_page.logout()

    # ============================================================
    # STAGE 3 — AGENT RESOLVES TICKET
    # ============================================================

    print(
        "\n=============================================="
    )
    print(
        "STAGE 3 - AGENT RESOLVES TICKET"
    )
    print(
        "=============================================="
    )

    agent_login(page)

    staff_ticket_page = StaffTicketPage(page)

    staff_ticket_page.open_my_tickets()

    staff_ticket_page.open_ticket(
        ticket_number
    )

    staff_ticket_page.verify_ticket_details(
        ticket_number=ticket_number,
        ticket_description=TICKET_DESCRIPTION
    )

    # Resolve ticket
    staff_ticket_page.resolve_ticket(
        reason=RESOLUTION_REASON
    )

    # Verify resolved
    staff_ticket_page.verify_resolved_status()

    print(
        f"\n{ticket_number} resolved successfully."
    )

    # Logout agent
    logout(page)

    # ============================================================
    # STAGE 4 — CUSTOMER VERIFIES AND RATES
    # ============================================================

    print(
        "\n=============================================="
    )
    print(
        "STAGE 4 - CUSTOMER VERIFIES AND RATES"
    )
    print(
        "=============================================="
    )

    customer_login(page)

    customer_ticket_page = (
        CustomerTicketVerificationPage(page)
    )

    customer_ticket_page.open_my_tickets()

    customer_ticket_page.open_ticket(
        ticket_number
    )

    customer_ticket_page.verify_ticket(
        ticket_number=ticket_number,
        ticket_description=TICKET_DESCRIPTION
    )

    customer_ticket_page.verify_resolved_status()

    # Open rating
    customer_ticket_page.open_rate_support()

    # Submit 5-star rating
    customer_ticket_page.select_rating(
        CUSTOMER_RATING
    )

    customer_ticket_page.enter_feedback(
        CUSTOMER_FEEDBACK
    )

    customer_ticket_page.submit_rating()

    print(
        f"\n{ticket_number} rated {CUSTOMER_RATING}/5."
    )

    # ============================================================
    # FINAL RESULT
    # ============================================================

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