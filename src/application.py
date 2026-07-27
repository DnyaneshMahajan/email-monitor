from src.config.paths import verify_project_structure
from src.providers.gmail.client import GmailClient
from src.providers.gmail.parser import GmailParser

from src.formatters.email_console_formatter import (
    EmailConsoleFormatter,
)

class Application:

    def run(self):
        print("=" * 60)
        print("Email Monitor")
        print("=" * 60)

        verify_project_structure()

        print("\nAuthenticatin with Gmail...")
        client = GmailClient()
        print("Authentication successful.")

        print("\nFetching latest emails...")
        messages = client.list_latest_messages()
        total = len(messages)

        for index, item in enumerate(messages, start=1):
            raw_message = client.get_message(item["id"])
            email = GmailParser.parse(raw_message)

            print(
                EmailConsoleFormatter.format(
                    email=email,
                    index=index,
                    total=total,
                )
            )