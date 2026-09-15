from playwright.sync_api import Page, expect


class CompanyTicketPage:
    """
    Page Object Model for Company-side Ticket Management.

    This Page Object supports two ticket assignment scenarios:

    1. Existing Assigned Ticket
       Agent-Kim
           ↓
       Reassign
           ↓
       John-Agent

    2. Fresh Unassigned Ticket
       Unassigned
           ↓
       Assign Agent
           ↓
       John-Agent
    """

    def __init__(self, page: Page):

        self.page = page

        # ============================================================
        # NAVIGATION LOCATORS
        # ============================================================

        self.tickets_link = page.get_by_role(
            "link",
            name="Tickets 9+",
            exact=True
        )

        # ============================================================
        # EXISTING TICKET REASSIGNMENT LOCATOR
        # ============================================================

        self.reassign_button = page.get_by_role(
            "button",
            name="Reassign",
            exact=True
        )

        # ============================================================
        # FRESH TICKET ASSIGNMENT LOCATOR
        # ============================================================

        self.assign_agent_button = page.get_by_role(
            "button",
            name="Assign Agent",
            exact=True
        )

        # ============================================================
        # ASSIGNMENT MODAL LOCATORS
        # ============================================================

        self.assign_modal_heading = page.get_by_text(
            "Assign Ticket to Agent",
            exact=True
        )

        self.choose_agent_button = page.get_by_role(
            "button",
            name="Choose an agent",
            exact=True
        )

        self.john_agent_option = page.get_by_text(
            "John-Agent",
            exact=True
        )

        self.assign_ticket_button = page.get_by_role(
            "button",
            name="Assign Ticket",
            exact=True
        )

        # ============================================================
        # LOGOUT LOCATORS
        # ============================================================

        self.profile_button = page.locator(
            "button.topbar-profile-btn"
        )

        self.sign_out_button = page.get_by_text(
            "Sign out",
            exact=True
        )

    # ================================================================
    # OPEN TICKETS
    # ================================================================

    def open_tickets(self) -> None:
        """
        Open Company Tickets page.
        """

        expect(
            self.tickets_link
        ).to_be_visible(
            timeout=10000
        )

        self.tickets_link.click()

        self.page.wait_for_load_state(
            "networkidle",
            timeout=30000
        )

        print(
            "Company Tickets page opened."
        )

    # ================================================================
    # OPEN SPECIFIC TICKET
    # ================================================================

    def open_ticket(
        self,
        ticket_number: str
    ) -> None:
        """
        Open a specific ticket using its ticket number.
        """

        ticket_link = self.page.get_by_role(
            "link",
            name=ticket_number,
            exact=True
        )

        expect(
            ticket_link
        ).to_be_visible(
            timeout=10000
        )

        ticket_link.click()

        self.page.wait_for_load_state(
            "networkidle",
            timeout=30000
        )

        print(
            f"Opened ticket: {ticket_number}"
        )

    # ================================================================
    # REASSIGN EXISTING TICKET TO JOHN-AGENT
    # ================================================================

    def reassign_ticket_to_john(self) -> None:
        """
        Reassign an already assigned ticket
        from another agent to John-Agent.

        Example:

            Agent-Kim
                ↓
            Reassign
                ↓
            Choose an agent
                ↓
            John-Agent
                ↓
            Assign Ticket
        """

        # ------------------------------------------------------------
        # 1. Verify Reassign button
        # ------------------------------------------------------------

        expect(
            self.reassign_button
        ).to_be_visible(
            timeout=10000
        )

        print(
            "\nReassign button found."
        )

        # ------------------------------------------------------------
        # 2. Click Reassign
        # ------------------------------------------------------------

        self.reassign_button.click()

        print(
            "Reassign button clicked."
        )

        # ------------------------------------------------------------
        # 3. Verify Assignment Modal
        # ------------------------------------------------------------

        expect(
            self.assign_modal_heading
        ).to_be_visible(
            timeout=10000
        )

        print(
            "Assign Ticket to Agent modal opened."
        )

        # ------------------------------------------------------------
        # 4. Open Agent Dropdown
        # ------------------------------------------------------------

        expect(
            self.choose_agent_button
        ).to_be_visible(
            timeout=5000
        )

        self.choose_agent_button.click()

        print(
            "Agent dropdown opened."
        )

        # ------------------------------------------------------------
        # 5. Select John-Agent
        # ------------------------------------------------------------

        expect(
            self.john_agent_option
        ).to_be_visible(
            timeout=5000
        )

        self.john_agent_option.click()

        print(
            "John-Agent selected."
        )

        # ------------------------------------------------------------
        # 6. Click Assign Ticket
        # ------------------------------------------------------------

        expect(
            self.assign_ticket_button
        ).to_be_visible(
            timeout=5000
        )

        self.assign_ticket_button.click()

        print(
            "Assign Ticket clicked."
        )

        # ------------------------------------------------------------
        # 7. Wait for Modal to Close
        # ------------------------------------------------------------

        expect(
            self.assign_modal_heading
        ).to_be_hidden(
            timeout=10000
        )

        print(
            "Assignment modal closed."
        )

    # ================================================================
    # ASSIGN FRESH / UNASSIGNED TICKET TO JOHN-AGENT
    # ================================================================

    def assign_new_ticket_to_john(self) -> None:
        """
        Assign a fresh/unassigned ticket directly to John-Agent.

        Business Flow:

            Unassigned Ticket
                    ↓
              Assign Agent
                    ↓
            Assignment Modal
                    ↓
             Choose an agent
                    ↓
               John-Agent
                    ↓
             Assign Ticket
                    ↓
             Modal Closed
        """

        # ------------------------------------------------------------
        # 1. Verify Assign Agent button
        # ------------------------------------------------------------

        expect(
            self.assign_agent_button
        ).to_be_visible(
            timeout=10000
        )

        print(
            "\nAssign Agent button found."
        )

        # ------------------------------------------------------------
        # 2. Click Assign Agent
        # ------------------------------------------------------------

        self.assign_agent_button.click()

        print(
            "Assign Agent button clicked."
        )

        # ------------------------------------------------------------
        # 3. Verify Assignment Modal
        # ------------------------------------------------------------

        expect(
            self.assign_modal_heading
        ).to_be_visible(
            timeout=10000
        )

        print(
            "Assign Ticket to Agent modal opened."
        )

        # ------------------------------------------------------------
        # 4. Open Agent Dropdown
        # ------------------------------------------------------------

        expect(
            self.choose_agent_button
        ).to_be_visible(
            timeout=5000
        )

        self.choose_agent_button.click()

        print(
            "Agent dropdown opened."
        )

        # ------------------------------------------------------------
        # 5. Select John-Agent
        # ------------------------------------------------------------

        expect(
            self.john_agent_option
        ).to_be_visible(
            timeout=5000
        )

        self.john_agent_option.click()

        print(
            "John-Agent selected."
        )

        # ------------------------------------------------------------
        # 6. Click Assign Ticket
        # ------------------------------------------------------------

        expect(
            self.assign_ticket_button
        ).to_be_visible(
            timeout=5000
        )

        self.assign_ticket_button.click()

        print(
            "Assign Ticket clicked."
        )

        # ------------------------------------------------------------
        # 7. Wait for Assignment Modal to Close
        # ------------------------------------------------------------

        expect(
            self.assign_modal_heading
        ).to_be_hidden(
            timeout=10000
        )

        print(
            "Assignment modal closed."
        )

    # ================================================================
    # VERIFY JOHN-AGENT ASSIGNED
    # ================================================================

    def verify_john_agent_assigned(self) -> None:
        """
        Verify that John-Agent is displayed
        after ticket assignment/reassignment.
        """

        john_agent = self.page.get_by_text(
            "John-Agent",
            exact=True
        ).last

        expect(
            john_agent
        ).to_be_visible(
            timeout=10000
        )

        print(
            "John-Agent assignment verified."
        )

    # ================================================================
    # LOGOUT
    # ================================================================

    def logout(self) -> None:
        """
        Logout Company user.
        """

        # ------------------------------------------------------------
        # 1. Verify Profile Button
        # ------------------------------------------------------------

        expect(
            self.profile_button
        ).to_be_visible(
            timeout=10000
        )

        # ------------------------------------------------------------
        # 2. Open Profile Menu
        # ------------------------------------------------------------

        self.profile_button.click()

        # ------------------------------------------------------------
        # 3. Verify Sign Out
        # ------------------------------------------------------------

        expect(
            self.sign_out_button
        ).to_be_visible(
            timeout=5000
        )

        # ------------------------------------------------------------
        # 4. Click Sign Out
        # ------------------------------------------------------------

        self.sign_out_button.click()

        # ------------------------------------------------------------
        # 5. Verify Login Page
        # ------------------------------------------------------------

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
            "Company logout verified."
        )