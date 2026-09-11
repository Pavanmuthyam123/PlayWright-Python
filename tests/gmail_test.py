import os
import base64
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CREDENTIALS_FILE = os.path.join(
    BASE_DIR,
    "credentials.json"
)

TOKEN_FILE = os.path.join(
    BASE_DIR,
    "token.json"
)


def get_gmail_service():

    creds = None

    if os.path.exists(TOKEN_FILE):

        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            creds = flow.run_local_server(
                port=0
            )

        with open(TOKEN_FILE, "w") as token:

            token.write(
                creds.to_json()
            )

    return build(
        "gmail",
        "v1",
        credentials=creds
    )


def decode_body(data):

    return base64.urlsafe_b64decode(
        data + "=" * (-len(data) % 4)
    ).decode(
        "utf-8",
        errors="ignore"
    )


def get_email_body(payload):

    body_data = payload.get(
        "body",
        {}
    ).get(
        "data"
    )

    if body_data:

        return decode_body(body_data)

    for part in payload.get("parts", []):

        if part.get("mimeType") == "text/plain":

            data = part.get(
                "body",
                {}
            ).get(
                "data"
            )

            if data:

                return decode_body(data)

        # Handle nested parts
        if part.get("parts"):

            body = get_email_body(part)

            if body:

                return body

    return ""


def get_latest_otp():

    service = get_gmail_service()

    print("Gmail API connection successful!")

    # Search TickSupport OTP emails
    messages = service.users().messages().list(
        userId="me",
        q='subject:"Registration Verification Code"',
        maxResults=10
    ).execute()

    email_list = messages.get(
        "messages",
        []
    )

    print(
        "OTP subject emails found:",
        len(email_list)
    )

    if not email_list:

        raise Exception(
            "No TickSupport OTP emails found."
        )

    latest_message = None
    latest_timestamp = 0

    # Find latest email
    for message in email_list:

        msg = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()

        timestamp = int(
            msg.get(
                "internalDate",
                "0"
            )
        )

        if timestamp > latest_timestamp:

            latest_timestamp = timestamp

            latest_message = msg

    if not latest_message:

        raise Exception(
            "Could not find latest OTP email."
        )

    # Extract body
    body = get_email_body(
        latest_message["payload"]
    )

    # Find 6-digit OTP
    otp_match = re.search(
        r"\b\d{6}\b",
        body
    )

    if not otp_match:

        raise Exception(
            "6-digit OTP not found in latest email."
        )

    otp = otp_match.group()

    print(
        "Latest OTP:",
        otp
    )

    return otp


# Test latest OTP extraction
get_latest_otp()