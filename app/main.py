"""CRMschaller FastAPI giris noktasi.

Kapsam (el yazisi notlardan): yatirimci/partner takibi, envanter (SIA/RPO/ETO),
lojistik dosyalari, banka ekstresi entegrasyonu (Nordea/Is Bankasi/Kuveyt Turk),
admin panel (export + muhasebe entegrasyonu) ve gunluk otomatik sistem raporu.
MCP server ve Telegram bot ayri giris noktalari olarak calisir (bkz. app/mcp,
app/bot).
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import admin, banks, inventory, investors, logistics, meetings, reports
from app.services.report_scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(title="CRMschaller", version="0.1.0", lifespan=lifespan)

app.include_router(investors.router)
app.include_router(inventory.router)
app.include_router(logistics.router)
app.include_router(banks.router)
app.include_router(admin.router)
app.include_router(reports.router)
app.include_router(meetings.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
