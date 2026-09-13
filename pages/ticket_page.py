from playwright.sync_api import Page


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

            # Open priority dropdown
            self.medium_priority_button.click()

            # Select High from dropdown
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

        # Make sure submit button is visible
        self.create_ticket_button.scroll_into_view_if_needed()

        # Click submit button
        self.create_ticket_button.click()
