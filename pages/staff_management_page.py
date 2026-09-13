from playwright.sync_api import Page, expect


class StaffManagementPage:
    """
    Page Object Model for Company -> Staff & Agents management.
    """

    def __init__(self, page: Page):

        self.page = page

        # =========================================================
        # STAFF MANAGEMENT
        # =========================================================

        self.staff_agents_link = page.get_by_role(
            "link",
            name="Staff & Agents",
            exact=True
        )

        self.add_staff_button = page.get_by_text(
            "Add Staff",
            exact=True
        )

        # =========================================================
        # ADD STAFF FORM
        # =========================================================

        self.name_field = page.get_by_role(
            "textbox",
            name="John Doe"
        )

        self.email_field = page.get_by_role(
            "textbox",
            name="john@example.com"
        )

        self.password_field = page.get_by_role(
            "textbox",
            name="Min 6 characters"
        )

        self.phone_field = page.get_by_role(
            "textbox",
            name="9876543210 (starts with 6,7,8,9)"
        )

        self.skills_field = page.get_by_role(
            "textbox",
            name="e.g. AC Repair, Electrical, Plumbing"
        )

        # =========================================================
        # ROLE
        # =========================================================

        self.role_button = page.get_by_role(
            "button",
            name="Agent",
            exact=True
        )

        self.agent_role_option = page.get_by_role(
            "button",
            name="Agent Handles assigned tickets only",
            exact=True
        )

        # =========================================================
        # DEPARTMENT
        # =========================================================

        self.department_button = page.get_by_role(
            "button",
            name="Select Departments…",
            exact=True
        )

        self.technical_support_option = page.get_by_role(
            "button",
            name="Technical Support",
            exact=True
        )

        # =========================================================
        # ADD BUTTON
        # =========================================================

        self.add_button = page.get_by_role(
            "button",
            name="Add",
            exact=True
        )

    # =============================================================
    # OPEN STAFF MANAGEMENT
    # =============================================================

    def open_staff_management(self):

        expect(
            self.staff_agents_link
        ).to_be_visible(timeout=10000)

        self.staff_agents_link.click()

        self.page.wait_for_load_state(
            "networkidle",
            timeout=30000
        )

        print("\nStaff & Agents page opened.")

    # =============================================================
    # OPEN ADD STAFF
    # =============================================================

    def open_add_staff_form(self):

        expect(
            self.add_staff_button
        ).to_be_visible(timeout=10000)

        self.add_staff_button.click()

        expect(
            self.name_field
        ).to_be_visible(timeout=10000)

        print("Add Staff form opened.")

    # =============================================================
    # BASIC DETAILS
    # =============================================================

    def enter_staff_basic_details(
        self,
        name,
        email,
        password
    ):

        self.name_field.fill(name)

        self.email_field.fill(email)

        self.password_field.fill(password)

        print("Staff basic details entered.")

    # =============================================================
    # ROLE
    # =============================================================

    def select_agent_role(self):

        self.role_button.click()

        expect(
            self.agent_role_option
        ).to_be_visible(timeout=5000)

        self.agent_role_option.click()

        print("Agent role selected.")

    # =============================================================
    # DEPARTMENT
    # =============================================================

    def select_department(self):

        self.department_button.click()

        expect(
            self.technical_support_option
        ).to_be_visible(timeout=5000)

        self.technical_support_option.click()

        print("Technical Support department selected.")

    # =============================================================
    # PHONE + SPECIALIZATION
    # =============================================================

    def enter_phone_and_skills(
        self,
        phone,
        skills
    ):

        self.phone_field.fill(phone)

        self.skills_field.fill(skills)

        print(f"Phone entered: {phone}")
        print(f"Specialization entered: {skills}")

    # =============================================================
    # ADD BUTTON
    # =============================================================

    def verify_add_button_enabled(self):

        expect(
            self.add_button
        ).to_be_visible(timeout=5000)

        expect(
            self.add_button
        ).to_be_enabled(timeout=5000)

        print("Add button is enabled.")

    def click_add(self):

        self.verify_add_button_enabled()

        self.add_button.click()

        print("Add button clicked.")

    # =============================================================
    # VERIFY EXISTING STAFF
    # =============================================================

    def verify_existing_staff(
        self,
        staff_name,
        staff_email
    ):

        staff = self.page.get_by_text(
            staff_name,
            exact=True
        ).first

        expect(
            staff
        ).to_be_visible(timeout=10000)

        print(
            f"Existing staff verified: {staff_name}"
        )

        email = self.page.get_by_text(
            staff_email,
            exact=True
        ).first

        expect(
            email
        ).to_be_visible(timeout=10000)

        print(
            f"Existing staff email verified: {staff_email}"
        )