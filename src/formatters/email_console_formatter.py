from src.models.email import Email
from src.utils.datetime import format_datetime
from src.utils.console import wrap_text

class EmailConsoleFormatter:

    LINE_WIDTH = 100
    LABEL_WIDTH = 10
    VALUE_WIDTH = 82

    @classmethod
    def format(
        cls,
        email: Email,
        index: int,
        total: int
    ) -> str:
        
        lines = []
        lines.append(cls._header(index, total))

        lines.append(cls._field("From", email.sender))
        lines.append(cls._field("Subject", email.subject))
        lines.append(cls._field("Received", format_datetime(email.received_on)))
        lines.append(cls._field("Snippet", email.snippet))

        lines.append(cls._footer())

        return "\n".join(lines)
    
    @classmethod
    def _header(
        cls,
        index: int,
        total: int,
    ) -> str:
        
        return (
            f"\n"
            + f"{'=' * cls.LINE_WIDTH}\n"
            + "\n"
            + f"Email {index} of {total}\n"
            + "\n"
            + f"{'=' * cls.LINE_WIDTH}"
            + "\n"
        )
    
    @classmethod
    def _footer(cls) -> str:    
        return (
            "\n"
            + f"{'=' * cls.LINE_WIDTH}"
            + "\n"
        )

    @classmethod
    def _field(
        cls,
        label: str,
        value: str,
    ) -> str:
        
        wrapped = wrap_text(
            value, 
            width=cls.VALUE_WIDTH
        )

        lines = wrapped.splitlines()

        result = [
            f"{label:<{cls.LABEL_WIDTH}}: {lines[0]}"
        ]

        indent = " " * (cls.LABEL_WIDTH + 3)

        for line in lines[1:]:
            result.append(
                f"{indent}{line}"
            )
        
        return "\n".join(result)