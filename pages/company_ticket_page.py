from playwright.sync_api import Page, expect


class CompanyTicketPage:
    """
    Page Object Model for Company-side Ticket Management.

    Current Business Flow:
        Company Login
            ↓
        Company Dashboard
            ↓
        Tickets
            ↓
        Open Existing Ticket
            ↓
        Verify Agent-Kim
            ↓
        Reassign
            ↓
        Choose an Agent
            ↓
        Select John-Agent
            ↓
        Assign Ticket
            ↓
        Verify John-Agent
            ↓
        Logout
    """

    def __init__(self, page: Page):

        self.page = page

        # ============================================================
        # Navigation Locators
        # ============================================================

        self.tickets_link = page.get_by_role(
            "link",
            name="Tickets 9+",
            exact=True
        )

        # ============================================================
        # Ticket Reassignment Locators
        # ============================================================

        self.reassign_button = page.get_by_role(
            "button",
            name="Reassign",
            exact=True
        )

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
        # Logout Locators
        # ============================================================

        self.profile_button = page.locator(
            "button.topbar-profile-btn"
        )

        self.sign_out_button = page.get_by_text(
            "Sign out",
            exact=True
        )

    # ================================================================
    # Open Tickets
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

    # ================================================================
    # Open Specific Ticket
    # ================================================================

    def open_ticket(self, ticket_number: str) -> None:
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

    # ================================================================
    # Reassign Ticket to John-Agent
    # ================================================================

    def reassign_ticket_to_john(self) -> None:
        """
        Reassign the ticket from Agent-Kim to John-Agent.
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
    # Verify New Agent
    # ================================================================

    def verify_john_agent_assigned(self) -> None:
        """
        Verify that John-Agent is displayed after reassignment.
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
    # Logout
    # ================================================================

    def logout(self) -> None:
        """
        Logout Company user.
        """

        expect(
            self.profile_button
        ).to_be_visible(
            timeout=10000
        )

        self.profile_button.click()

        expect(
            self.sign_out_button
        ).to_be_visible(
            timeout=5000
        )

        self.sign_out_button.click()

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