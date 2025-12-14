class SecurityIncident:
    """Represents a cybersecurity incident in the platform."""

    def __init__(
        self,
        incident_id: int,
        title: str,
        incident_type: str,
        severity: str,
        status: str,
        date: str,
        description: str = "",
        reported_by: str | None = None,
    ):
        self.__incident_id = incident_id
        self.__title = title
        self.__incident_type = incident_type
        self.__severity = severity
        self.__status = status
        self.__date = date
        self.__description = description
        self.__reported_by = reported_by

    # ---- Getters ----
    def get_id(self) -> int:
        return self.__incident_id

    def get_title(self) -> str:
        return self.__title

    def get_incident_type(self) -> str:
        return self.__incident_type

    def get_severity(self) -> str:
        return self.__severity

    def get_status(self) -> str:
        return self.__status

    def get_date(self) -> str:
        return self.__date

    def get_description(self) -> str:
        return self.__description

    def get_reported_by(self) -> str | None:
        return self.__reported_by

    # ---- Helper methods (used in dashboards/filters) ----
    def is_high_risk(self) -> bool:
        return self.__severity in ["High", "Critical"]

    def is_open_or_in_progress(self) -> bool:
        return self.__status in ["open", "in-progress"]

    def get_severity_level(self) -> int:
        """
        Returns a number you can use for sorting/severity scoring.
        Higher number = more severe.
        """
        levels = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
        return levels.get(self.__severity, 0)

    def to_dict(self) -> dict:
        """Convenient for turning objects into a dataframe/table."""
        return {
            "id": self.__incident_id,
            "title": self.__title,
            "incident_type": self.__incident_type,
            "severity": self.__severity,
            "status": self.__status,
            "date": self.__date,
            "description": self.__description,
            "reported_by": self.__reported_by,
        }

    def __str__(self) -> str:
        return (
            f"SecurityIncident(id={self.__incident_id}, title={self.__title}, "
            f"severity={self.__severity}, status={self.__status})"
        )
