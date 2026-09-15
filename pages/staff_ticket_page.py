from playwright.sync_api import Page, expect


class StaffTicketPage:
    """
    Page Object Model for Agent / Staff Ticket handling.

    Responsibilities:

    1. Open Agent My Tickets
    2. Find required ticket
    3. Click View for that ticket
    4. Verify ticket details
    5. Update ticket status
    6. Resolve ticket
    7. Verify resolved status
    8. Return to Dashboard
    9. Logout Agent
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self, page: Page):

        self.page = page

        # ========================================================
        # AGENT NAVIGATION
        # ========================================================

        self.my_tickets_link = page.get_by_role(
            "link",
            name="My Tickets",
            exact=True
        )

        self.dashboard_link = page.get_by_role(
            "link",
            name="Dashboard",
            exact=True
        )

        # ========================================================
        # STATUS UPDATE
        # ========================================================

        self.update_status_button = page.get_by_role(
            "button",
            name="Update Status",
            exact=True
        )

        self.assigned_status_button = page.get_by_role(
            "button",
            name="Assigned",
            exact=True
        )

        self.resolved_status_option = page.get_by_role(
            "button",
            name="Resolved",
            exact=True
        )

        self.status_reason_field = page.get_by_role(
            "textbox",
            name="Reason for status change…"
        )

        # ========================================================
        # PROFILE / LOGOUT
        # ========================================================

        self.profile_button = page.locator(
            "button.topbar-profile-btn"
        )

        self.sign_out_button = page.get_by_role(
            "button",
            name="Sign out",
            exact=True
        )

    # ============================================================
    # OPEN MY TICKETS
    # ============================================================

    def open_my_tickets(self) -> None:
        """
        Opens Agent My Tickets page.
        """

        expect(
            self.my_tickets_link
        ).to_be_visible(
            timeout=10000
        )

        self.my_tickets_link.click()

        # --------------------------------------------------------
        # Verify My Tickets page
        # --------------------------------------------------------

        expect(
            self.page.get_by_role(
                "heading",
                name="My Tickets",
                exact=True
            )
        ).to_be_visible(
            timeout=10000
        )

        print()
        print("Agent My Tickets page opened.")

    # ============================================================
    # OPEN SPECIFIC TICKET
    # ============================================================

    def open_ticket(
        self,
        ticket_number: str
    ) -> None:
        """
        Finds the required ticket row in My Tickets
        and clicks the View button from that same row.

        Example:

        TCS-000014 | SSD Issue | resolved | View
        """

        # --------------------------------------------------------
        # 1. Locate ticket row
        # --------------------------------------------------------

        ticket_row = self.page.get_by_role(
            "row"
        ).filter(
            has_text=ticket_number
        )

        # --------------------------------------------------------
        # 2. Verify ticket row
        # --------------------------------------------------------

        expect(
            ticket_row
        ).to_be_visible(
            timeout=10000
        )

        print(
            f"Ticket row found: {ticket_number}"
        )

        # --------------------------------------------------------
        # 3. Find View button inside same ticket row
        # --------------------------------------------------------

        view_button = ticket_row.get_by_role(
            "button",
            name="View",
            exact=True
        )

        expect(
            view_button
        ).to_be_visible(
            timeout=10000
        )

        print(
            f"View button found for: {ticket_number}"
        )

        # --------------------------------------------------------
        # 4. Click View
        # --------------------------------------------------------

        view_button.click()

        print(
            f"View clicked for ticket: {ticket_number}"
        )

        # --------------------------------------------------------
        # 5. Wait until ticket detail content appears
        # --------------------------------------------------------

        expect(
            self.page.get_by_text(
                ticket_number,
                exact=False
            ).first
        ).to_be_visible(
            timeout=10000
        )

        print(
            f"Opened Agent Ticket: {ticket_number}"
        )

    # ============================================================
    # VERIFY TICKET DETAILS
    # ============================================================

    def verify_ticket_details(
        self,
        ticket_number: str,
        ticket_description: str
    ) -> None:
        """
        Verifies ticket number and ticket subject
        after opening the ticket.
        """

        # --------------------------------------------------------
        # Verify Ticket Number
        # --------------------------------------------------------

        expect(
            self.page.get_by_text(
                ticket_number,
                exact=False
            ).first
        ).to_be_visible(
            timeout=10000
        )

        print(
            f"Ticket number verified: {ticket_number}"
        )

        # --------------------------------------------------------
        # Verify Ticket Description / Subject
        # --------------------------------------------------------

        expect(
            self.page.get_by_text(
                ticket_description,
                exact=True
            ).first
        ).to_be_visible(
            timeout=10000
        )

        print(
            f"Ticket description verified: {ticket_description}"
        )

    # ============================================================
    # RESOLVE TICKET
    # ============================================================

    def resolve_ticket(
        self,
        reason: str
    ) -> None:
        """
        Changes the ticket status from Assigned
        to Resolved and enters the status-change reason.
        """

        # --------------------------------------------------------
        # 1. Click Update Status
        # --------------------------------------------------------

        expect(
            self.update_status_button
        ).to_be_visible(
            timeout=10000
        )

        self.update_status_button.click()

        print(
            "Update Status opened."
        )

        # --------------------------------------------------------
        # 2. Verify current Assigned status button
        # --------------------------------------------------------

        expect(
            self.assigned_status_button
        ).to_be_visible(
            timeout=5000
        )

        # --------------------------------------------------------
        # 3. Open status dropdown
        # --------------------------------------------------------

        self.assigned_status_button.click()

        print(
            "Status dropdown opened."
        )

        # --------------------------------------------------------
        # 4. Select Resolved
        # --------------------------------------------------------

        expect(
            self.resolved_status_option
        ).to_be_visible(
            timeout=5000
        )

        self.resolved_status_option.click()

        print(
            "Resolved status selected."
        )

        # --------------------------------------------------------
        # 5. Enter resolution reason
        # --------------------------------------------------------

        expect(
            self.status_reason_field
        ).to_be_visible(
            timeout=5000
        )

        self.status_reason_field.fill(
            reason
        )

        print(
            f"Resolution reason entered: {reason}"
        )

        # --------------------------------------------------------
        # 6. Locate final Update Status submit button
        # --------------------------------------------------------

        submit_button = self.page.locator(
            "button"
        ).filter(
            has_text="Update Status"
        ).last

        expect(
            submit_button
        ).to_be_visible(
            timeout=5000
        )

        expect(
            submit_button
        ).to_be_enabled(
            timeout=5000
        )

        # --------------------------------------------------------
        # 7. Submit status update
        # --------------------------------------------------------

        submit_button.click()

        print(
            "Ticket status update submitted."
        )

    # ============================================================
    # VERIFY RESOLVED STATUS
    # ============================================================

    def verify_resolved_status(self) -> None:
        """
        Verifies Resolved status after updating ticket.
        """

        resolved_status = self.page.get_by_text(
            "resolved",
            exact=True
        ).first

        expect(
            resolved_status
        ).to_be_visible(
            timeout=10000
        )

        print(
            "Ticket status verified: Resolved"
        )

    # ============================================================
    # OPEN DASHBOARD
    # ============================================================

    def open_dashboard(self) -> None:
        """
        Returns to Agent Dashboard.
        """

        expect(
            self.dashboard_link
        ).to_be_visible(
            timeout=10000
        )

        self.dashboard_link.click()

        expect(
            self.page.get_by_text(
                "John-Agent",
                exact=False
            ).first
        ).to_be_visible(
            timeout=10000
        )

        print(
            "Agent Dashboard opened."
        )

    # ============================================================
    # LOGOUT
    # ============================================================

    def logout(self) -> None:
        """
        Logs out the Agent account.
        """

        # --------------------------------------------------------
        # Open profile menu
        # --------------------------------------------------------

        expect(
            self.profile_button
        ).to_be_visible(
            timeout=10000
        )

        self.profile_button.click()

        # --------------------------------------------------------
        # Click Sign out
        # --------------------------------------------------------

        expect(
            self.sign_out_button
        ).to_be_visible(
            timeout=5000
        )

        self.sign_out_button.click()

        # --------------------------------------------------------
        # Verify Login page
        # --------------------------------------------------------

        self.page.wait_for_url(
            "**/tcs/login",
            timeout=10000
        )

        expect(
            self.page.get_by_role(
                "heading",
                name="WELCOME BACK"
            )
        ).to_be_visible(
            timeout=10000
        )

        print(
            "Agent logout verified."
        )