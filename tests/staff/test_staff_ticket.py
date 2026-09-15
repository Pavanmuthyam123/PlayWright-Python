from playwright.sync_api import Page, expect

from pages.staff_ticket_page import StaffTicketPage


AGENT_EMAIL = "johnagent@gmail.com"
AGENT_PASSWORD = "1234567"

TICKET_NUMBER = "TCS-000038"
TICKET_DESCRIPTION = "Fresh Assignment Test 1789484663"

RESOLUTION_REASON = "Ticket Completed"


def login_agent(page: Page) -> None:
    page.goto("https://www.ticksupport.com/tcs/login")

    expect(
        page.get_by_role("heading", name="WELCOME BACK")
    ).to_be_visible(timeout=10000)

    page.locator('input[type="email"]').fill(AGENT_EMAIL)
    page.locator('input[type="password"]').fill(AGENT_PASSWORD)

    page.get_by_role(
        "button",
        name="Sign In",
        exact=True
    ).click()

    expect(page).to_have_url(
        "https://www.ticksupport.com/tcs/agent/dashboard",
        timeout=10000
    )

    expect(
        page.get_by_text("John-Agent", exact=True)
    ).to_be_visible(timeout=10000)

    print("\nAgent login successful.")


# ============================================================
# POSITIVE TEST
# ============================================================

def test_agent_resolve_assigned_ticket(page: Page):
    login_agent(page)

    staff_ticket_page = StaffTicketPage(page)

    staff_ticket_page.open_my_tickets()

    print("Agent My Tickets page opened.")

    staff_ticket_page.open_ticket(TICKET_NUMBER)

    print(f"Opened ticket: {TICKET_NUMBER}")

    staff_ticket_page.verify_ticket_details(
        TICKET_NUMBER,
        TICKET_DESCRIPTION
    )

    print(f"Ticket details verified: {TICKET_NUMBER}")

    staff_ticket_page.resolve_ticket(
        RESOLUTION_REASON
    )

    print("Ticket resolution submitted.")

    staff_ticket_page.verify_resolved_status()

    print("Ticket status verified: Resolved")

    staff_ticket_page.logout()

    print("\n==============================================")
    print("AGENT TICKET RESOLUTION PASSED")
    print("==============================================")
    print(f"Ticket     : {TICKET_NUMBER}")
    print("Status     : Resolved")
    print(f"Reason     : {RESOLUTION_REASON}")
    print("Logout     : Successful")
    print("==============================================")


# ============================================================
# NEGATIVE / VALIDATION TEST
# ============================================================

def test_agent_resolution_without_reason(page: Page):
    login_agent(page)

    staff_ticket_page = StaffTicketPage(page)

    staff_ticket_page.open_my_tickets()

    print("\nAgent My Tickets page opened.")

    staff_ticket_page.open_ticket(TICKET_NUMBER)

    print(f"Opened ticket: {TICKET_NUMBER}")

    staff_ticket_page.verify_ticket_details(
        TICKET_NUMBER,
        TICKET_DESCRIPTION
    )

    print(f"Ticket details verified: {TICKET_NUMBER}")

    # Open Update Status
    staff_ticket_page.update_status_button.click()

    print("Update Status opened.")

    # Open status dropdown
    staff_ticket_page.status_dropdown.click()

    print("Status dropdown opened.")

    # Select Resolved
    staff_ticket_page.resolved_option.click()

    print("Resolved status selected.")

    # Leave resolution reason EMPTY
    staff_ticket_page.resolution_reason_field.fill("")

    print("Resolution reason left empty.")

    # Try submitting
    staff_ticket_page.update_status_submit_button.click()

    print("Update Status submit attempted.")

    # --------------------------------------------------------
    # EXPECTED RESULT
    # --------------------------------------------------------
    # Ticket should NOT become Resolved when reason is empty.
    #
    # We verify that the Update Status form is still visible.
    # This means the application did not successfully submit it.
    # --------------------------------------------------------

    expect(
        staff_ticket_page.resolution_reason_field
    ).to_be_visible(timeout=5000)

    print(
        "Validation verified: resolution reason is required."
    )

    staff_ticket_page.logout()

    print("\n==============================================")
    print("AGENT RESOLUTION VALIDATION PASSED")
    print("==============================================")
    print(f"Ticket : {TICKET_NUMBER}")
    print("Scenario : Empty Resolution Reason")
    print("Expected : Ticket should not be resolved")
    print("Result   : PASS")
    print("==============================================")