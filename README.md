# PlayWright Python - TickSupport Automation Framework

A professional Python automation testing framework for the TickSupport application using Playwright and Pytest.

## Project Structure

```
PlayWright-Python/
├── tests/                      # All test files
│   ├── customer/              # Customer feature tests
│   │   ├── test_customer_login.py
│   │   ├── test_customer_registration.py
│   │   └── test_customer_forgot_password.py
│   └── tickets/               # Ticket feature tests
│       └── test_customer_ticket.py
│
├── pages/                      # Page Object Models
│   ├── ticket_page.py
│   ├── login_page.py          # (To be created)
│   ├── registration_page.py   # (To be created)
│   └── dashboard_page.py      # (To be created)
│
├── utils/                      # Utilities
│   ├── gmail_otp.py           # Gmail API integration
│   └── test_data.py           # Test data loader
│
├── test_data/                  # Test data files
│   ├── users.json             # User credentials
│   └── tickets.json           # Ticket test data
│
├── config/                     # Configuration
│   └── config.py              # Environment & settings
│
├── conftest.py                # Pytest configuration & fixtures
├── pytest.ini                 # Pytest settings
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
playwright install
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Gmail API Setup (for OTP tests)

- Ensure `credentials.json` and `token.json` are in the project root
- Required for registration and password reset tests

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/customer/test_customer_login.py
```

### Run with Browser Visible

```bash
pytest -s --headed
```

### Run with Detailed Output

```bash
pytest -v -s
```

### Run HTML Report

```bash
pytest --html=reports/report.html --self-contained-html
```

## Test Data

Test data is centrally managed in `test_data/` and loaded via `utils/test_data.py`:

```python
from utils.test_data import get_customer_credentials, get_ticket_data

# Get customer credentials
user = get_customer_credentials("customer_default")
email = user["email"]
password = user["password"]

# Get ticket data
ticket = get_ticket_data("ssd_issue")
description = ticket["description"]
priority = ticket["priority"]
```

## Page Object Models

Each page has a dedicated POM class with methods for interactions:

```python
from pages.ticket_page import TicketPage

ticket_page = TicketPage(page)
ticket_page.click_new_ticket()
ticket_page.enter_description("Test Description")
ticket_page.select_priority("High")
ticket_page.create_ticket()
```

## Key Features

- ✅ Playwright for modern web automation
- ✅ Pytest for test framework
- ✅ Page Object Model pattern
- ✅ Gmail API integration for OTP extraction
- ✅ Centralized test data management
- ✅ Environment configuration
- ✅ Failure screenshots in HTML reports

## Adding New Tests

1. Create test file in appropriate folder under `tests/`
2. Use page objects from `pages/`
3. Load test data from `utils/test_data.py`
4. Follow existing test structure and naming conventions

## Troubleshooting

### Tests Timeout

- Check if application is accessible
- Increase timeout values in `config/config.py`
- Use `--headed` to see browser execution

### Gmail OTP Tests Fail

- Verify `credentials.json` and `token.json` exist
- Check Gmail API scopes are correct
- Ensure test email has Gmail access

### Import Errors

- Verify `pytest.ini` has correct `pythonpath`
- Check all files have `__init__.py` in packages

## Contributing

- Follow existing code style and structure
- Add docstrings to all methods
- Use type hints where possible
- Update this README if structure changes

## Support

For issues or questions, check:
- Test output and screenshots in `reports/`
- Conftest hooks in `conftest.py`
- Test data in `test_data/`
