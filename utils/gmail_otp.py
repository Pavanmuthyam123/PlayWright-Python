import os
import base64
import re
import time
import ssl

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


# ============================================================
# GMAIL SERVICE
# ============================================================

def get_gmail_service():
    """
    Create Gmail API service using token.json.
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

    if not os.path.exists(token_path):
        raise FileNotFoundError(
            f"Gmail token file not found: {token_path}"
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
    Execute Gmail API request with retry support.
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
    Decode Gmail Base64URL encoded email body.
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

    Supports:
    - Normal email
    - Multipart email
    - Nested multipart email
    """

    payload = message.get(
        "payload",
        {}
    )

    # --------------------------------------------------------
    # Normal email body
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
    # Recursive multipart body
    # --------------------------------------------------------

    def extract_from_parts(parts):

        for part in parts:

            part_body = (
                part
                .get("body", {})
                .get("data")
            )

            if part_body:

                decoded = decode_body(
                    part_body
                )

                if decoded:
                    return decoded

            nested_parts = part.get(
                "parts",
                []
            )

            if nested_parts:

                nested_result = extract_from_parts(
                    nested_parts
                )

                if nested_result:
                    return nested_result

        return ""

    parts = payload.get(
        "parts",
        []
    )

    if parts:

        return extract_from_parts(
            parts
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
# FIND OTP IN EMAIL
# ============================================================

def find_otp_in_message(
    message
):
    """
    Extract a 6-digit OTP from email body.
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
    timeout=45,
    after_timestamp=None
):
    """
    Find OTP using:

    - Exact recipient email
    - Exact subject
    - Latest matching email
    - Optional after_timestamp filter

    after_timestamp:
        Gmail internalDate in milliseconds.

        If provided, emails received before or at this
        timestamp are ignored.

    This is important for password reset because Gmail
    may contain an old valid-looking OTP.
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

    if after_timestamp is not None:

        print(
            f"After   : {after_timestamp}"
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

                        # ----------------------------------------
                        # IMPORTANT:
                        # Ignore old OTP emails
                        # ----------------------------------------

                        if (
                            after_timestamp is not None
                            and internal_date <= after_timestamp
                        ):

                            print(
                                "Ignoring old email: "
                                f"{internal_date}"
                            )

                            continue

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
                # Find OTP
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
                            f"FRESH OTP FOUND: {code}"
                        )
                        print()

                        return code

        except Exception as e:

            print(
                f"Gmail search error: {e}"
            )

        print(
            "Fresh OTP not available yet. "
            "Checking again..."
        )

        time.sleep(2)

    raise Exception(
        f"Fresh '{subject}' email for "
        f"'{email}' was not found within "
        f"{timeout} seconds."
    )


# ============================================================
# REGISTRATION OTP
# ============================================================

def get_registration_otp(
    email,
    timeout=45,
    after_timestamp=None
):
    """
    Get registration OTP for exact test email.

    Existing tests can continue using this function.
    """

    return get_code_for_email(
        subject="Registration Verification Code",
        email=email,
        timeout=timeout,
        after_timestamp=after_timestamp
    )


# ============================================================
# PASSWORD RESET CODE
# ============================================================

def get_reset_code(
    email,
    timeout=45,
    after_timestamp=None
):
    """
    Get fresh password reset OTP for exact test email.

    IMPORTANT:
    after_timestamp prevents an old reset OTP from being
    selected.
    """

    return get_code_for_email(
        subject="Password Reset Verification Code",
        email=email,
        timeout=timeout,
        after_timestamp=after_timestamp
    )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def get_latest_otp(
    timeout=45,
    after_timestamp=None
):
    """
    Legacy registration OTP function.

    Kept so existing registration tests do not break.

    Searches registration emails by subject only.
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

            print(
                f"Registration emails found: "
                f"{len(messages)}"
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

                    # ----------------------------------------
                    # Ignore old registration emails if
                    # after_timestamp is supplied
                    # ----------------------------------------

                    if (
                        after_timestamp is not None
                        and internal_date <= after_timestamp
                    ):

                        print(
                            "Ignoring old registration email: "
                            f"{internal_date}"
                        )

                        continue

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