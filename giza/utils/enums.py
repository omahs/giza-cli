from enum import StrEnum


class VersionStatus(StrEnum):
    COMPLETED: str = "COMPLETED"
    FAILED: str = "FAILED"
    STARTING: str = "STARTING"
    UPLOADED: str = "UPLOADED"
    PROCESSING: str = "PROCESSING"


class JobStatus(StrEnum):
    COMPLETED: str = "COMPLETED"
    FAILED: str = "FAILED"
    STARTING: str = "STARTING"
    PROCESSING: str = "PROCESSING"


class JobSize(StrEnum):
    S: str = "S"
    M: str = "M"
    L: str = "L"
    XL: str = "XL"


class Framework(StrEnum):
    CAIRO: str = "CAIRO"
