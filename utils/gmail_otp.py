import os
import base64
import re
import time
import ssl

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


# ============================================================
# GMAIL SERVICE
# ============================================================

def get_gmail_service():
    """
    Create Gmail API service.
    """

    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    token_path = os.path.join(
        base_dir,
        "token.json"
    )

    creds = Credentials.from_authorized_user_file(
        token_path,
        SCOPES
    )

    service = build(
        "gmail",
        "v1",
        credentials=creds,
        cache_discovery=False
    )

    return service


# ============================================================
# GMAIL API REQUEST WITH RETRY
# ============================================================

def execute_with_retry(
    request,
    retries=3
):
    """
    Execute Gmail API request with retry.
    """

    for attempt in range(
        1,
        retries + 1
    ):

        try:

            return request.execute(
                num_retries=3
            )

        except (
            ConnectionResetError,
            TimeoutError,
            ssl.SSLError,
            OSError
        ) as e:

            print(
                f"Gmail connection error "
                f"(attempt {attempt}/{retries}): {e}"
            )

            if attempt == retries:
                raise

            wait_time = attempt * 2

            print(
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(
                wait_time
            )


# ============================================================
# DECODE EMAIL BODY
# ============================================================

def decode_body(data):
    """
    Decode Gmail Base64URL encoded body.
    """

    if not data:
        return ""

    try:

        decoded = base64.urlsafe_b64decode(
            data + "=" * (-len(data) % 4)
        )

        return decoded.decode(
            "utf-8",
            errors="ignore"
        )

    except Exception as e:

        print(
            f"Body decode error: {e}"
        )

        return ""


# ============================================================
# GET EMAIL BODY
# ============================================================

def get_email_body(message):
    """
    Extract email body from Gmail message.
    """

    payload = message.get(
        "payload",
        {}
    )

    # --------------------------------------------------------
    # Normal email
    # --------------------------------------------------------

    body_data = (
        payload
        .get("body", {})
        .get("data")
    )

    if body_data:

        return decode_body(
            body_data
        )

    # --------------------------------------------------------
    # Multipart email
    # --------------------------------------------------------

    parts = payload.get(
        "parts",
        []
    )

    for part in parts:

        part_body = (
            part
            .get("body", {})
            .get("data")
        )

        if part_body:

            return decode_body(
                part_body
            )

        nested_parts = part.get(
            "parts",
            []
        )

        for nested in nested_parts:

            nested_body = (
                nested
                .get("body", {})
                .get("data")
            )

            if nested_body:

                return decode_body(
                    nested_body
                )

    return ""


# ============================================================
# GET FULL EMAIL
# ============================================================

def get_full_message(
    message_id,
    retries=3
):
    """
    Get complete Gmail message.
    """

    for attempt in range(
        1,
        retries + 1
    ):

        try:

            print(
                f"Reading Gmail message "
                f"(attempt {attempt}/{retries})..."
            )

            service = get_gmail_service()

            request = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id=message_id,
                    format="full"
                )
            )

            return execute_with_retry(
                request
            )

        except (
            ConnectionResetError,
            TimeoutError,
            ssl.SSLError,
            OSError
        ) as e:

            print(
                f"Gmail read error: {e}"
            )

            if attempt == retries:
                raise

            time.sleep(
                attempt * 2
            )


# ============================================================
# FIND OTP
# ============================================================

def find_otp_in_message(
    message
):
    """
    Extract 6-digit OTP from email body.
    """

    body = get_email_body(
        message
    )

    if not body:

        return None

    match = re.search(
        r"\b\d{6}\b",
        body
    )

    if match:

        return match.group()

    return None


# ============================================================
# GET OTP FOR SPECIFIC EMAIL
# ============================================================

def get_code_for_email(
    subject,
    email,
    timeout=45
):
    """
    Find OTP using:
        - exact email recipient
        - exact email subject
        - latest matching email

    This is used by the E2E test because every run
    creates a unique Gmail plus-address.
    """

    print()
    print("=" * 70)
    print("GMAIL OTP SEARCH")
    print("=" * 70)

    print(
        f"To      : {email}"
    )

    print(
        f"Subject : {subject}"
    )

    print("=" * 70)

    start_time = time.time()

    while (
        time.time() - start_time
        < timeout
    ):

        try:

            service = get_gmail_service()

            # ------------------------------------------------
            # Search exact recipient + subject
            # ------------------------------------------------

            query = (
                f'to:"{email}" '
                f'subject:"{subject}"'
            )

            print(
                f"\nGmail query: {query}"
            )

            response = execute_with_retry(
                service.users()
                .messages()
                .list(
                    userId="me",
                    q=query,
                    maxResults=20
                )
            )

            messages = response.get(
                "messages",
                []
            )

            print(
                f"Matching emails found: "
                f"{len(messages)}"
            )

            if messages:

                email_data = []

                # --------------------------------------------
                # Read all matching emails
                # --------------------------------------------

                for msg in messages:

                    try:

                        message = get_full_message(
                            msg["id"]
                        )

                        internal_date = int(
                            message.get(
                                "internalDate",
                                0
                            )
                        )

                        email_data.append(
                            (
                                internal_date,
                                message
                            )
                        )

                    except Exception as e:

                        print(
                            f"Could not read "
                            f"{msg['id']}: {e}"
                        )

                # --------------------------------------------
                # Sort newest first
                # --------------------------------------------

                email_data.sort(
                    key=lambda item: item[0],
                    reverse=True
                )

                # --------------------------------------------
                # Take newest matching email
                # --------------------------------------------

                for internal_date, message in email_data:

                    print(
                        f"Checking email with "
                        f"internalDate: {internal_date}"
                    )

                    code = find_otp_in_message(
                        message
                    )

                    if code:

                        print()
                        print(
                            f"OTP FOUND: {code}"
                        )
                        print()

                        return code

        except Exception as e:

            print(
                f"Gmail search error: {e}"
            )

        print(
            "OTP not available yet. "
            "Checking again..."
        )

        time.sleep(2)

    raise Exception(
        f"'{subject}' email for "
        f"'{email}' was not found within "
        f"{timeout} seconds."
    )


# ============================================================
# REGISTRATION OTP
# ============================================================

def get_registration_otp(
    email,
    timeout=45
):
    """
    Get registration OTP for the exact test email.
    """

    return get_code_for_email(
        subject="Registration Verification Code",
        email=email,
        timeout=timeout
    )


# ============================================================
# PASSWORD RESET CODE
# ============================================================

def get_reset_code(
    email,
    timeout=45
):
    """
    Get password reset OTP for the exact test email.
    """

    return get_code_for_email(
        subject="Password Reset Verification Code",
        email=email,
        timeout=timeout
    )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def get_latest_otp(
    timeout=45
):
    """
    Old registration OTP function.
    Kept so existing standalone tests do not break.

    This searches by subject only and takes the newest
    matching registration email.
    """

    print()
    print(
        "Using legacy get_latest_otp()"
    )

    start_time = time.time()

    while (
        time.time() - start_time
        < timeout
    ):

        try:

            service = get_gmail_service()

            response = execute_with_retry(
                service.users()
                .messages()
                .list(
                    userId="me",
                    q='subject:"Registration Verification Code"',
                    maxResults=20
                )
            )

            messages = response.get(
                "messages",
                []
            )

            email_data = []

            for msg in messages:

                try:

                    message = get_full_message(
                        msg["id"]
                    )

                    internal_date = int(
                        message.get(
                            "internalDate",
                            0
                        )
                    )

                    email_data.append(
                        (
                            internal_date,
                            message
                        )
                    )

                except Exception as e:

                    print(
                        f"Could not read message: {e}"
                    )

            email_data.sort(
                key=lambda item: item[0],
                reverse=True
            )

            for _, message in email_data:

                code = find_otp_in_message(
                    message
                )

                if code:

                    print(
                        f"Registration OTP found: "
                        f"{code}"
                    )

                    return code

        except Exception as e:

            print(
                f"Gmail error: {e}"
            )

        time.sleep(2)

    raise Exception(
        "Registration OTP was not received."
    )