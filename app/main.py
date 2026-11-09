import os
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field
from .planner import basic_exit_prices

VERSION = os.getenv("APP_VERSION", "1.0.0")
app = FastAPI(title="NCAP Exit Preview", version=VERSION,
              description="Stateless lab demo using placeholder percentage-based calculations.")

class PreviewRequest(BaseModel):
    direction: Literal["LONG", "SHORT"]
    signal_price: float = Field(gt=0, allow_inf_nan=False)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {"version": VERSION, "service": "ncap-exit-preview", "mode": "demo"}

@app.post("/preview")
def preview(payload: PreviewRequest):
    stop, tp1, tp2 = basic_exit_prices(payload.direction, payload.signal_price)
    return {"direction": payload.direction, "entry": payload.signal_price,
            "stop": stop, "tp1": tp1, "tp2": tp2,
            "version": VERSION, "mode": "demo"}

