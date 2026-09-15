from playwright.sync_api import Page, expect


class CustomerTicketVerificationPage:
    """
    Page Object Model for Customer Ticket Verification.

    Responsibilities:

    1. Open My Tickets
    2. Open a specific ticket
    3. Verify ticket details
    4. Verify resolved status
    5. Open Rate Support
    6. Select rating
    7. Enter feedback
    8. Submit rating
    9. Logout
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self, page: Page):

        self.page = page

        # ========================================================
        # CUSTOMER NAVIGATION
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
        # RATING
        # ========================================================

        self.rate_support_button = page.get_by_role(
            "button",
            name="Rate Support",
            exact=True
        )

        self.star_button = page.get_by_role(
            "button",
            name="★"
        )

        self.feedback_field = page.get_by_role(
            "textbox",
            name="Tell us about your experience…"
        )

        self.submit_rating_button = page.get_by_role(
            "button",
            name="⭐ Submit Rating",
            exact=True
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
        Opens Customer My Tickets page.
        """

        expect(
            self.my_tickets_link
        ).to_be_visible(
            timeout=10000
        )

        self.my_tickets_link.click()

        expect(
            self.page.get_by_role(
                "heading",
                name="My Tickets",
                exact=True
            )
        ).to_be_visible(
            timeout=10000
        )

        print(
            "\nCustomer My Tickets page opened."
        )

    # ============================================================
    # OPEN SPECIFIC TICKET
    # ============================================================

    def open_ticket(
        self,
        ticket_number: str
    ) -> None:
        """
        Opens the requested customer ticket.
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

        print(
            f"Customer ticket opened: {ticket_number}"
        )

    # ============================================================
    # VERIFY TICKET
    # ============================================================

    def verify_ticket(
        self,
        ticket_number: str,
        ticket_description: str
    ) -> None:
        """
        Verifies ticket number and description.
        """

        expect(
            self.page.get_by_text(
                ticket_number,
                exact=False
            ).first
        ).to_be_visible(
            timeout=10000
        )

        expect(
            self.page.get_by_text(
                ticket_description,
                exact=True
            ).first
        ).to_be_visible(
            timeout=10000
        )

        print(
            f"Ticket verified: {ticket_number}"
        )

        print(
            f"Description verified: {ticket_description}"
        )

    # ============================================================
    # VERIFY RESOLVED STATUS
    # ============================================================

    def verify_resolved_status(self) -> None:
        """
        Verifies that the customer's ticket is resolved.
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
            "Customer verified ticket status: Resolved"
        )

    # ============================================================
    # OPEN RATE SUPPORT
    # ============================================================

    def open_rate_support(self) -> None:
        """
        Opens the Rate Support section.
        """

        expect(
            self.rate_support_button
        ).to_be_visible(
            timeout=10000
        )

        self.rate_support_button.click()

        print(
            "Rate Support opened."
        )

    # ============================================================
    # SELECT RATING
    # ============================================================

    def select_rating(
        self,
        rating: int
    ) -> None:
        """
        Selects customer rating.

        Example:
        rating=5 means five-star rating.
        """

        if rating < 1 or rating > 5:
            raise ValueError(
                "Rating must be between 1 and 5."
            )

        star = self.star_button.nth(
            rating - 1
        )

        expect(
            star
        ).to_be_visible(
            timeout=5000
        )

        star.click()

        print(
            f"Customer rating selected: {rating}/5"
        )

    # ============================================================
    # ENTER FEEDBACK
    # ============================================================

    def enter_feedback(
        self,
        feedback: str
    ) -> None:
        """
        Enters customer feedback.
        """

        expect(
            self.feedback_field
        ).to_be_visible(
            timeout=5000
        )

        self.feedback_field.fill(
            feedback
        )

        print(
            f"Customer feedback entered: {feedback}"
        )

    # ============================================================
    # SUBMIT RATING
    # ============================================================

    def submit_rating(self) -> None:
        """
        Submits customer rating and feedback.
        """

        expect(
            self.submit_rating_button
        ).to_be_visible(
            timeout=5000
        )

        expect(
            self.submit_rating_button
        ).to_be_enabled(
            timeout=5000
        )

        self.submit_rating_button.click()

        print(
            "Customer rating submitted."
        )

    # ============================================================
    # LOGOUT
    # ============================================================

    def logout(self) -> None:
        """
        Logs out the Customer account.
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
            "Customer logout verified."
        )