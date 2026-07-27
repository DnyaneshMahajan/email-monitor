from enum import StrEnum

class ProcessingStatus(StrEnum):

    NEW = "NEW"
    SUMMARIZED = "SUMMARIZED"
    RULES_EVALUATED = "RULES_EVALUATED"
    NOTIFIED = "NOTIFIED"
    FAILED = "FAILED"
    