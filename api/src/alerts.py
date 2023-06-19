import time
from pydantic import BaseModel
from db_manager import DBManager

class Alert(BaseModel):
    type: str
    timestamp: int

class AlertManager():
    def __init__(self):
        self.db = DBManager()
        self.latest_timestamp = int(time.time())
        self.N_ALERTS_CHECK = 20

    def save_alert(self, alert: Alert):
        data = self.db.get_db() # [{timestamp: int, type: str}]
        data.append({"timestamp": alert.timestamp, "type": alert.type})
        self.db.save_to_db(data)
    
    def get_latest_alert(self):
        """
        Retrieves the latest alert from the database if it exists.
        Returns emtpy object otherwise
        Checks for last 20 alerts, in case they were not properly ordered.
        """
        data = self.db.get_db()
        # Newest alerts are appended, hence iterate 
        # database in reverse order for efficency
        alerts_checked = 0
        for ii in range(1, len(data)+1):
            alert = data[-ii]
            # If there is a timestamp newer than the latest alert
            if self.latest_timestamp < alert["timestamp"]:
                self.latest_timestamp = alert["timestamp"]
                return alert
            alerts_checked += 1
            if alerts_checked > self.N_ALERTS_CHECK:
                return {}
