from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import datetime

app = FastAPI(title="Memory Navigator Vendor API", version="1.0.0")

# --- Pydantic Models ---

class Location(BaseModel):
    lat: float
    lon: float
    accuracy: float

class Vitals(BaseModel):
    heart_rate: int
    steps: int

class TelemetryRecord(BaseModel):
    timestamp: datetime
    location: Location
    vitals: Vitals
    battery_level: int

class TelemetryPayload(BaseModel):
    device_id: str
    records: List[TelemetryRecord]

class EventDetails(BaseModel):
    lat: float
    lon: float
    description: str

class EventPayload(BaseModel):
    device_id: str
    timestamp: datetime
    event_type: Literal["FALL_DETECTED", "SOS_BUTTON", "DOOR_OPEN", "GEO_EXIT"]
    details: EventDetails

# --- Endpoints ---

@app.post("/api/v1/ingestion/telemetry")
async def ingest_telemetry(payload: TelemetryPayload):
    """
    Ingest telemetry data from hardware devices.
    """
    # In a real app, we would save this to a database.
    # For MVP, we just validate and print.
    print(f"Data Received: {payload.model_dump_json()}")
    return {"status": "success"}

@app.post("/api/v1/ingestion/events")
async def ingest_event(payload: EventPayload):
    """
    Ingest critical events from hardware devices.
    """
    # In a real app, we would trigger immediate alerts.
    # For MVP, we just validate and print.
    print(f"Data Received: {payload.model_dump_json()}")
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
