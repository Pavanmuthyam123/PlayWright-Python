from playwright.sync_api import Page, expect


class TicketPage:
    """Page Object Model for Customer Ticket creation."""

    def __init__(self, page: Page):
        self.page = page

        # ============================================================
        # Locators
        # ============================================================

        # New Ticket button
        self.new_ticket_button = page.get_by_text(
            "New Ticket",
            exact=True
        )

        # Ticket type
        self.general_support_option = page.get_by_text(
            "General Support Request",
            exact=True
        )

        # Ticket description
        self.description_field = page.get_by_role(
            "textbox",
            name="Tell us what you need help"
        )

        # Priority dropdown
        self.medium_priority_button = page.get_by_role(
            "button",
            name="Medium",
            exact=True
        )

        # High option inside priority dropdown
        self.high_priority_option = page.get_by_text(
            "High",
            exact=True
        )

        # Create Ticket submit button
        self.create_ticket_button = page.locator(
            'button[type="submit"]'
        ).filter(
            has_text="Create Ticket"
        )

    # ============================================================
    # New Ticket
    # ============================================================

    def click_new_ticket(self) -> None:
        """Open Create Support Ticket window."""
        self.new_ticket_button.click()

    # ============================================================
    # Ticket Type
    # ============================================================

    def select_ticket_type(self) -> None:
        """Select General Support Request."""
        self.general_support_option.click()

    # ============================================================
    # Description
    # ============================================================

    def enter_description(self, description: str) -> None:
        """Enter ticket issue description."""
        self.description_field.fill(description)

    # ============================================================
    # Priority
    # ============================================================

    def select_priority(self, priority: str) -> None:
        """
        Select ticket priority.

        Medium:
            Click Medium dropdown.

        High:
            Click Medium dropdown first,
            then select High option.
        """

        if priority.lower() == "medium":

            self.medium_priority_button.click()

        elif priority.lower() == "high":

            self.medium_priority_button.click()
            self.high_priority_option.click()

        else:

            raise ValueError(
                f"Unsupported priority: {priority}"
            )

    # ============================================================
    # Create Ticket
    # ============================================================

    def create_ticket(self) -> None:
        """Submit the Create Support Ticket form."""

        self.create_ticket_button.scroll_into_view_if_needed()

        self.create_ticket_button.click()

        # Wait until ticket form disappears
        expect(
            self.description_field
        ).not_to_be_visible(
            timeout=10000
        )

    # ============================================================
    # Get Generated Ticket Number
    # ============================================================

    def get_ticket_number(
        self,
        ticket_description: str
    ) -> str:
        """
        Get the latest generated ticket number
        from My Tickets.

        The newest ticket appears first in the ticket table.
        """

        # Find all rows containing the ticket description.
        ticket_rows = self.page.get_by_role(
            "row"
        ).filter(
            has_text=ticket_description
        )

        # At least one matching ticket should exist.
        expect(
            ticket_rows.first
        ).to_be_visible(
            timeout=10000
        )

        # The newest ticket is the first matching row.
        latest_ticket_row = ticket_rows.first

        # Get the ticket number link from that row.
        ticket_link = latest_ticket_row.get_by_role(
            "link"
        ).first

        expect(
            ticket_link
        ).to_be_visible(
            timeout=10000
        )

        # Read generated ticket number.
        ticket_number = ticket_link.inner_text().strip()

        # Basic validation.
        expect(
            ticket_link
        ).to_have_text(
            ticket_number
        )

        print(
            f"\nGenerated Ticket Number: {ticket_number}"
        )

        return ticket_number