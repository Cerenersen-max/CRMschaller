"""Not: 'Yedek baglanti katmani'. Bir arac cagrisi basarisiz oldugunda son
basarili sonucu donen basit bir in-memory yedek/cache katmani."""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from app.mcp.observability import observability


class BackupConnectionLayer:
    """Tool cagrilarini sarmalayip son basarili sonucu 'yedek' olarak saklar."""

    def __init__(self) -> None:
        self._last_good: dict[str, Any] = {}

    def call(self, key: str, fn: Callable[[], Any]) -> Any:
        try:
            result = fn()
            self._last_good[key] = result
            return result
        except Exception as exc:  # noqa: BLE001 - yedek katman kasitli olarak genis yakalar
            observability.log(
                "mcp.cache_layer",
                f"'{key}' cagrisi basarisiz oldu ({exc}); yedek sonuc kullaniliyor.",
                level="WARNING",
            )
            if key in self._last_good:
                return self._last_good[key]
            raise


backup_connection_layer = BackupConnectionLayer()
