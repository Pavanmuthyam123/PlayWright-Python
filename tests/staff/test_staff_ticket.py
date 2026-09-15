from pages.staff_ticket_page import StaffTicketPage


# ================================================================
# TEST DATA
# ================================================================

TICKET_NUMBER = "TCS-000015"

TICKET_DESCRIPTION = "SSD Issue"

RESOLUTION_REASON = "Ticket Completed"


# ================================================================
# AGENT TICKET RESOLUTION TEST
# ================================================================

def test_agent_resolve_assigned_ticket(
    agent_login
):
    """
    Positive Test Case:

    Agent logs in,
    opens assigned ticket,
    verifies ticket details,
    changes ticket status to Resolved,
    enters resolution reason,
    and verifies the final status.

    Expected Result:

    Ticket should be successfully resolved.
    """

    # ============================================================
    # AGENT LOGIN
    # ============================================================
    #
    # Login is handled by agent_login fixture
    # from conftest.py.
    #
    # ============================================================

    page = agent_login

    print()
    print(
        "Agent dashboard verified through fixture."
    )

    # ============================================================
    # CREATE STAFF TICKET PAGE OBJECT
    # ============================================================

    staff_ticket_page = StaffTicketPage(
        page
    )

    # ============================================================
    # OPEN MY TICKETS
    # ============================================================

    staff_ticket_page.open_my_tickets()

    # ============================================================
    # OPEN REQUIRED TICKET
    # ============================================================
    #
    # open_ticket() now:
    #
    # 1. Finds TCS-000014 row
    # 2. Finds View button inside same row
    # 3. Clicks View
    #
    # ============================================================

    staff_ticket_page.open_ticket(
        TICKET_NUMBER
    )

    # ============================================================
    # VERIFY TICKET DETAILS
    # ============================================================

    staff_ticket_page.verify_ticket_details(
        ticket_number=TICKET_NUMBER,
        ticket_description=TICKET_DESCRIPTION
    )

    # ============================================================
    # RESOLVE TICKET
    # ============================================================

    staff_ticket_page.resolve_ticket(
        reason=RESOLUTION_REASON
    )

    # ============================================================
    # VERIFY RESOLVED STATUS
    # ============================================================

    staff_ticket_page.verify_resolved_status()

    # ============================================================
    # FINAL RESULT
    # ============================================================

    print()
    print("==============================================")
    print("AGENT TICKET RESOLUTION PASSED")
    print("==============================================")
    print(f"Ticket      : {TICKET_NUMBER}")
    print(f"Description : {TICKET_DESCRIPTION}")
    print("Status      : Resolved")
    print(f"Reason      : {RESOLUTION_REASON}")
    print("Result      : PASS")
    print("==============================================")