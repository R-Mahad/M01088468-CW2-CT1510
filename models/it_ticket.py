class ITTicket:
    """Represents an IT support ticket in the IT Operations domain."""

    def __init__(self, ticket_id: int, title: str, priority: str, status: str, created_date: str):
        self.__ticket_id = ticket_id
        self.__title = title
        self.__priority = priority
        self.__status = status
        self.__created_date = created_date

    # ---- Getters ----
    def get_id(self) -> int:
        return self.__ticket_id

    def get_title(self) -> str:
        return self.__title

    def get_priority(self) -> str:
        return self.__priority

    def get_status(self) -> str:
        return self.__status

    def get_created_date(self) -> str:
        return self.__created_date

    # ---- Helper methods ----
    def is_high_priority(self) -> bool:
        return self.__priority == "High"

    def is_active(self) -> bool:
        """Active tickets are those not closed."""
        return self.__status in ["open", "in-progress"]

    def to_dict(self) -> dict:
        return {
            "id": self.__ticket_id,
            "title": self.__title,
            "priority": self.__priority,
            "status": self.__status,
            "created_date": self.__created_date,
        }

    def __str__(self) -> str:
        return (
            f"ITTicket(id={self.__ticket_id}, title={self.__title}, "
            f"priority={self.__priority}, status={self.__status})"
        )
