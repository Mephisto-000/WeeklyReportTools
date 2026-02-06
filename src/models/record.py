from dataclasses import dataclass
from datetime import date

@dataclass
class WorkRecord:
    """Represents a single daily work record."""
    date: date
    project_name: str
    summary: str
    details: str

    def to_dict(self) -> dict:
        """Converts record to dictionary for storage."""
        return {
            "Date": self.date.isoformat(),
            "Project": self.project_name,
            "Summary": self.summary,
            "Details": self.details
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WorkRecord":
        """Creates record from dictionary (e.g. from Excel row)."""
        return cls(
            date=date.fromisoformat(str(data["Date"]).split("T")[0]), # Handle potential datetime strings
            project_name=str(data["Project"]),
            summary=str(data["Summary"]),
            details=str(data["Details"])
        )
