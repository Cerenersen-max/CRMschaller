"""Not: 'Banka Statemleri - Nordea/Open Banking API -> anlik SEPA odemeleri, Hesap bilgisi
statemleri - Is Bankasi // Kuveyt Turk (Arap Emirates) <- FX oran entegrasyonu'.

Her banka saglayicisi icin ortak bir arayuz (BankClient) tanimlanir; gercek API
kimlik bilgileri .env uzerinden saglanmadigi surece client'lar 'stub' modda
calisip ornek/bos veri doner. Gercek entegrasyon icin ilgili _fetch_* metodunu
saglayicinin resmi API dokumaniyla doldurmaniz yeterlidir.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

import httpx

from app.config import Settings, get_settings


@dataclass
class RawStatementLine:
    external_ref: str
    amount: float
    currency: str
    description: str
    booked_at: datetime
    fx_rate: float | None = None


class BankClient(ABC):
    """Tum banka saglayicilari icin ortak sozlesme."""

    provider_name: str

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()

    @abstractmethod
    def fetch_statement(self, iban: str) -> list[RawStatementLine]:
        """Verilen IBAN icin hesap ekstresi satirlarini doner."""

    def is_configured(self) -> bool:
        return True


class NordeaOpenBankingClient(BankClient):
    """Nordea / Open Banking API -> anlik SEPA odemeleri."""

    provider_name = "nordea"

    def is_configured(self) -> bool:
        return bool(self.settings.nordea_client_id and self.settings.nordea_client_secret)

    def fetch_statement(self, iban: str) -> list[RawStatementLine]:
        if not self.is_configured():
            # Kimlik bilgileri girilmeden gercek cagri yapilmaz; bos liste doner.
            return []
        # NOT: Gercek entegrasyon icin Nordea Open Banking OAuth2 akisi ve
        # /v3/accounts/{iban}/transactions endpoint'i kullanilir.
        with httpx.Client(base_url=self.settings.nordea_api_base_url, timeout=10) as client:
            response = client.get(
                f"/v3/accounts/{iban}/transactions",
                headers={"Authorization": f"Bearer {self._get_token(client)}"},
            )
            response.raise_for_status()
            data = response.json()
        return [
            RawStatementLine(
                external_ref=tx.get("id", ""),
                amount=float(tx.get("amount", 0)),
                currency=tx.get("currency", "EUR"),
                description=tx.get("message", ""),
                booked_at=datetime.fromisoformat(tx["bookingDate"]),
            )
            for tx in data.get("transactions", [])
        ]

    def _get_token(self, client: httpx.Client) -> str:
        token_response = client.post(
            "/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.settings.nordea_client_id,
                "client_secret": self.settings.nordea_client_secret,
            },
        )
        token_response.raise_for_status()
        return token_response.json()["access_token"]


class IsBankasiClient(BankClient):
    """Is Bankasi hesap ekstresi entegrasyonu."""

    provider_name = "isbank"

    def is_configured(self) -> bool:
        return bool(self.settings.isbank_api_key and self.settings.isbank_api_base_url)

    def fetch_statement(self, iban: str) -> list[RawStatementLine]:
        if not self.is_configured():
            return []
        with httpx.Client(base_url=self.settings.isbank_api_base_url, timeout=10) as client:
            response = client.get(
                f"/accounts/{iban}/statement",
                headers={"X-Api-Key": self.settings.isbank_api_key},
            )
            response.raise_for_status()
            data = response.json()
        return [
            RawStatementLine(
                external_ref=tx.get("referenceNo", ""),
                amount=float(tx.get("amount", 0)),
                currency=tx.get("currency", "TRY"),
                description=tx.get("description", ""),
                booked_at=datetime.fromisoformat(tx["date"]),
            )
            for tx in data.get("items", [])
        ]


class KuveytTurkClient(BankClient):
    """Kuveyt Turk (Arap Emirates baglantili) hesap ekstresi + FX oran entegrasyonu."""

    provider_name = "kuveytturk"

    def is_configured(self) -> bool:
        return bool(self.settings.kuveytturk_api_key and self.settings.kuveytturk_api_base_url)

    def fetch_statement(self, iban: str) -> list[RawStatementLine]:
        if not self.is_configured():
            return []
        with httpx.Client(base_url=self.settings.kuveytturk_api_base_url, timeout=10) as client:
            response = client.get(
                f"/api/accounts/{iban}/movements",
                headers={"Authorization": f"Bearer {self.settings.kuveytturk_api_key}"},
            )
            response.raise_for_status()
            data = response.json()
        fx_rates = fetch_fx_rates(base_currency="TRY")
        return [
            RawStatementLine(
                external_ref=tx.get("id", ""),
                amount=float(tx.get("amount", 0)),
                currency=tx.get("currency", "TRY"),
                description=tx.get("description", ""),
                booked_at=datetime.fromisoformat(tx["valueDate"]),
                fx_rate=fx_rates.get(tx.get("currency", "TRY")),
            )
            for tx in data.get("movements", [])
        ]


def fetch_fx_rates(base_currency: str = "EUR") -> dict[str, float]:
    """FX oran entegrasyonu - farkli para birimlerindeki islemleri karsilastirmak icin."""
    settings = get_settings()
    try:
        with httpx.Client(timeout=10) as client:
            response = client.get(settings.fx_rate_api_url, params={"base": base_currency})
            response.raise_for_status()
            return response.json().get("rates", {})
    except httpx.HTTPError:
        return {}


PROVIDER_CLIENTS: dict[str, type[BankClient]] = {
    NordeaOpenBankingClient.provider_name: NordeaOpenBankingClient,
    IsBankasiClient.provider_name: IsBankasiClient,
    KuveytTurkClient.provider_name: KuveytTurkClient,
}


def get_bank_client(provider: str) -> BankClient:
    client_cls = PROVIDER_CLIENTS.get(provider)
    if not client_cls:
        raise ValueError(f"Bilinmeyen banka saglayicisi: {provider}")
    return client_cls()
