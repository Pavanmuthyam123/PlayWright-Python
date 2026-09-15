from playwright.sync_api import expect

from pages.customer_ticket_verification_page import (
    CustomerTicketVerificationPage
)


TICKET_NUMBER = "TCS-000038"
TICKET_DESCRIPTION = "Fresh Assignment Test 1789484663"

RATING = 5

FEEDBACK = (
    "Thanks for John-Agent. "
    "The ticket was resolved successfully."
)


def test_customer_verify_resolved_ticket(customer_login):
    """
    Customer Ticket Verification.

    Existing Ticket
        ↓
    Customer My Tickets
        ↓
    Open TCS-000038
        ↓
    Verify Ticket Details
        ↓
    Verify Status = Resolved
        ↓
    Rate 5/5
        ↓
    Enter Feedback
        ↓
    Submit Rating
        ↓
    Logout
    """

    page = customer_login

    print(
        "\n=============================================="
    )
    print(
        "CUSTOMER TICKET VERIFICATION"
    )
    print(
        "=============================================="
    )

    # ------------------------------------------------------------
    # 1. CUSTOMER LOGIN
    # ------------------------------------------------------------

    expect(
        page
    ).to_have_url(
        "https://www.ticksupport.com/tcs/my/dashboard",
        timeout=10000
    )

    print(
        "\nCustomer login successful."
    )

    # ------------------------------------------------------------
    # 2. CUSTOMER TICKET PAGE
    # ------------------------------------------------------------

    customer_ticket_page = (
        CustomerTicketVerificationPage(page)
    )

    customer_ticket_page.open_my_tickets()

    print(
        "Customer My Tickets page opened."
    )

    # ------------------------------------------------------------
    # 3. OPEN SAME TICKET
    # ------------------------------------------------------------

    customer_ticket_page.open_ticket(
        TICKET_NUMBER
    )

    print(
        f"Customer ticket opened: {TICKET_NUMBER}"
    )

    # ------------------------------------------------------------
    # 4. VERIFY TICKET DETAILS
    # ------------------------------------------------------------

    customer_ticket_page.verify_ticket(
        TICKET_NUMBER,
        TICKET_DESCRIPTION
    )

    print(
        f"Ticket verified: {TICKET_NUMBER}"
    )

    print(
        f"Description verified: {TICKET_DESCRIPTION}"
    )

    # ------------------------------------------------------------
    # 5. VERIFY RESOLVED STATUS
    # ------------------------------------------------------------

    customer_ticket_page.verify_resolved_status()

    print(
        "Customer verified ticket status: Resolved"
    )

    # ------------------------------------------------------------
    # 6. OPEN RATE SUPPORT
    # ------------------------------------------------------------

    customer_ticket_page.open_rate_support()

    print(
        "Rate Support opened."
    )

    # ------------------------------------------------------------
    # 7. SELECT RATING
    # ------------------------------------------------------------

    customer_ticket_page.select_rating(
        RATING
    )

    print(
        f"Customer rating selected: {RATING}/5"
    )

    # ------------------------------------------------------------
    # 8. ENTER FEEDBACK
    # ------------------------------------------------------------

    customer_ticket_page.enter_feedback(
        FEEDBACK
    )

    print(
        f"Customer feedback entered: {FEEDBACK}"
    )

    # ------------------------------------------------------------
    # 9. SUBMIT RATING
    # ------------------------------------------------------------

    customer_ticket_page.submit_rating()

    print(
        "Customer rating submitted."
    )

    # ------------------------------------------------------------
    # 10. LOGOUT
    # ------------------------------------------------------------

    customer_ticket_page.logout()

    print(
        "Customer logout verified."
    )

    # ------------------------------------------------------------
    # FINAL RESULT
    # ------------------------------------------------------------

    print(
        "\n=============================================="
    )
    print(
        "CUSTOMER TICKET VERIFICATION PASSED"
    )
    print(
        "=============================================="
    )
    print(
        f"Ticket      : {TICKET_NUMBER}"
    )
    print(
        f"Description : {TICKET_DESCRIPTION}"
    )
    print(
        "Status      : Resolved"
    )
    print(
        f"Rating      : {RATING}/5"
    )
    print(
        f"Feedback    : {FEEDBACK}"
    )
    print(
        "Result      : PASS"
    )
    print(
        "=============================================="
    )