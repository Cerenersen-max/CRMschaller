"""Not: 'Karar/Orkestrasyon Katmani'. Hangi aracin cagrilacagina karar verir,
cagriyi yedek baglanti katmanindan gecirir ve gozlem katmanina loglar."""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from app.mcp.cache_layer import backup_connection_layer
from app.mcp.file_connector import FileConnector
from app.mcp.observability import observability
from app.mcp.tools.geojson_tool import convert_coordinates, preview_geojson


class DecisionLayer:
    """Kayitli araclari (tools) yonetir ve cagrilari orkestre eder."""

    def __init__(self, file_connector: FileConnector | None = None) -> None:
        self.file_connector = file_connector or FileConnector()
        self._tools: dict[str, Callable[..., Any]] = {
            "geojson.preview": preview_geojson,
            "geojson.convert_coordinates": convert_coordinates,
            "files.list": self.file_connector.list_files,
            "files.read": self.file_connector.read_file,
        }

    def available_tools(self) -> list[str]:
        return sorted(self._tools)

    def dispatch(self, tool_name: str, **kwargs: Any) -> Any:
        if tool_name not in self._tools:
            observability.log(
                "mcp.decision_layer", f"Bilinmeyen tool cagrisi: {tool_name}", level="ERROR"
            )
            raise KeyError(f"Bilinmeyen tool: {tool_name}")

        observability.log("mcp.decision_layer", f"Tool cagriliyor: {tool_name}({kwargs})")
        result = backup_connection_layer.call(tool_name, lambda: self._tools[tool_name](**kwargs))
        observability.log("mcp.decision_layer", f"Tool tamamlandi: {tool_name}")
        return result


decision_layer = DecisionLayer()
