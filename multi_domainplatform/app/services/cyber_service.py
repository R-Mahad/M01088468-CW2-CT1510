import pandas as pd
from app.data.incidents import get_all_incidents
from app.models.security_incident import SecurityIncident

class CyberService:
    def __init__(self, conn):
        self.conn = conn

    def incidents_df(self) -> pd.DataFrame:
        return get_all_incidents(self.conn)

    def incidents(self) -> list[SecurityIncident]:
        df = self.incidents_df()
        if df.empty:
            return []
        return [
            SecurityIncident(
                id=int(r["id"]),
                title=str(r["title"]),
                severity=str(r["severity"]),
                status=str(r["status"]),
                date=str(r["date"]),
                reported_by=r.get("reported_by", None),
            )
            for _, r in df.iterrows()
        ]
