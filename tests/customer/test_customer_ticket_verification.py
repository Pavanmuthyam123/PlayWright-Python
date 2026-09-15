from pages.customer_ticket_verification_page import (
    CustomerTicketVerificationPage
)


# ================================================================
# TEST DATA
# ================================================================

TICKET_NUMBER = "TCS-000015"

TICKET_DESCRIPTION = "SSD Issue"

EXPECTED_STATUS = "resolved"

CUSTOMER_RATING = 5

CUSTOMER_FEEDBACK = (
    "Thanks for John-Agent. "
    "The ticket was resolved successfully."
)


# ================================================================
# CUSTOMER TICKET VERIFICATION TEST
# ================================================================

def test_customer_verify_resolved_ticket(
    customer_login
):
    """
    Positive End-to-End Test Case:

    Customer logs in,
    opens My Tickets,
    opens the resolved ticket,
    verifies ticket details,
    verifies resolved status,
    rates the support,
    enters feedback,
    and submits the rating.

    Expected Result:

    Customer should successfully verify the resolved
    ticket and submit a support rating.
    """

    # ============================================================
    # CUSTOMER LOGIN
    # ============================================================
    #
    # Login is handled by the reusable
    # customer_login fixture from conftest.py.
    #
    # ============================================================

    page = customer_login

    print()
    print(
        "Customer dashboard verified through fixture."
    )

    # ============================================================
    # CREATE CUSTOMER PAGE OBJECT
    # ============================================================

    customer_ticket_page = (
        CustomerTicketVerificationPage(page)
    )

    # ============================================================
    # OPEN MY TICKETS
    # ============================================================

    customer_ticket_page.open_my_tickets()

    # ============================================================
    # OPEN REQUIRED TICKET
    # ============================================================

    customer_ticket_page.open_ticket(
        TICKET_NUMBER
    )

    # ============================================================
    # VERIFY TICKET DETAILS
    # ============================================================

    customer_ticket_page.verify_ticket(
        ticket_number=TICKET_NUMBER,
        ticket_description=TICKET_DESCRIPTION
    )

    # ============================================================
    # VERIFY RESOLVED STATUS
    # ============================================================

    customer_ticket_page.verify_resolved_status()

    # ============================================================
    # OPEN RATE SUPPORT
    # ============================================================

    customer_ticket_page.open_rate_support()

    # ============================================================
    # SELECT 5 STAR RATING
    # ============================================================

    customer_ticket_page.select_rating(
        CUSTOMER_RATING
    )

    # ============================================================
    # ENTER CUSTOMER FEEDBACK
    # ============================================================

    customer_ticket_page.enter_feedback(
        CUSTOMER_FEEDBACK
    )

    # ============================================================
    # SUBMIT RATING
    # ============================================================

    customer_ticket_page.submit_rating()

    # ============================================================
    # FINAL RESULT
    # ============================================================

    print()
    print(
        "=============================================="
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
        f"Status      : {EXPECTED_STATUS.title()}"
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
        "=============================================="
    )