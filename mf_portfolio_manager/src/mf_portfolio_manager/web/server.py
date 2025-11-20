from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from mf_portfolio_manager.crew import MutualFundCrew

logger = logging.getLogger("mf_portfolio_manager.web")
logging.basicConfig(level=logging.INFO)

STATIC_DIR = Path(__file__).resolve().parent / "static"


class HistoryEntry(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., description="Latest user message.")
    fund_category: str = "Large Cap"
    scheme_codes: Optional[str] = Field(
        default=None, description="Comma separated scheme codes, if any."
    )
    scheme_code: Optional[str] = None
    monthly_sip: float = 10000
    investment_months: int = 60
    holding_months: int = 60
    lumpsum_amount: float = 100000
    purchase_nav: float = 45.50
    current_nav: float = 68.75
    holding_years: int = 3
    risk_profile: str = "Moderate"
    investment_horizon: int = 7
    investment_type: str = "SIP"
    monthly_budget: float = 15000
    lumpsum_budget: float = 0
    fund_categories: str = "Large Cap, Mid Cap"
    investment_goal: Optional[str] = None
    history: List[HistoryEntry] = Field(default_factory=list)

    def to_inputs(self) -> dict[str, Any]:
        inputs = {
            "fund_category": self.fund_category,
            "scheme_codes": self.scheme_codes or self.scheme_code or "",
            "scheme_code": self.scheme_code or (self.scheme_codes or "").split(",")[0].strip(),
            "monthly_sip": self.monthly_sip,
            "investment_months": self.investment_months,
            "holding_months": self.holding_months,
            "lumpsum_amount": self.lumpsum_amount,
            "purchase_nav": self.purchase_nav,
            "current_nav": self.current_nav,
            "holding_years": self.holding_years,
            "risk_profile": self.risk_profile,
            "investment_horizon": self.investment_horizon,
            "investment_type": self.investment_type,
            "monthly_budget": self.monthly_budget,
            "lumpsum_budget": self.lumpsum_budget,
            "fund_categories": self.fund_categories,
            "investment_goal": self.investment_goal or self.message,
            "user_prompt": self.message,
            "chat_history": [
                f"{entry.role}: {entry.content}" for entry in self.history
            ],
        }
        return inputs


class ChatResponse(BaseModel):
    reply: str
    inputs: dict[str, Any]


app = FastAPI(title="Mutual Fund Portfolio Manager Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def index() -> FileResponse:
    if not STATIC_DIR.exists():
        raise HTTPException(status_code=404, detail="Static UI not found.")
    return FileResponse(STATIC_DIR / "index.html")


async def _run_crew(inputs: dict[str, Any]) -> str:
    def _kickoff() -> str:
        logger.info("Starting crew run with inputs: %s", inputs)
        crew = MutualFundCrew().crew()
        result = crew.kickoff(inputs=inputs)
        logger.info("Crew completed.")
        return str(result)

    return await run_in_threadpool(_kickoff)


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    try:
        inputs = payload.to_inputs()
        reply = await _run_crew(inputs)
        return ChatResponse(reply=reply, inputs=inputs)
    except Exception as exc:  # pragma: no cover - surfaced to UI
        logger.exception("Crew run failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

