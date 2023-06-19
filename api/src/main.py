# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from alerts import Alert, AlertManager
from db_manager import DBManager

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db_manager = DBManager()
alert_manager = AlertManager()

@app.get("/alerts")
async def get_alerts():
    alert = alert_manager.get_latest_alert()
    if alert:
        print(f'|-- INFO: Latest alert ({alert["timestamp"]}-{alert["type"]}) retrieved.')
    else:
        print(f'|-- INFO: No new alerts were found.')
    return alert

@app.post("/alerts")
async def save_alert(alert: Alert):
    alert_manager.save_alert(alert)
    print(f'|-- INFO: Alert: {alert.timestamp}-{alert.type} saved.')
    return f'Alert: {alert.timestamp}-{alert.type} saved.'