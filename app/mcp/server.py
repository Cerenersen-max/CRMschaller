"""Not: 'MCP Server icin - Dosya ve baglantilarim / Siteden devam edecek:
modelcontextprotocol.io/docs, docs.mapbox.com / Devkit mcp Server -> Preview
GeoJSON and convert coordinates / ARDINDAN sistemli mimari: Isleme Katmani,
Karar/Orkestrasyon Katmani, Yedek baglanti katmani, Gozlem & Log katmani'.

Bu modul, notlardaki mimariyi (dosya/baglanti -> karar/orkestrasyon -> yedek
baglanti -> gozlem&log) yalin bir stdio JSON-RPC dongusu olarak calistirir.
Resmi Model Context Protocol Python SDK'sina (bkz. modelcontextprotocol.io/docs,
`pip install mcp`) gecis yapmak icin `dispatch()` cagrilarini SDK'nin
`@server.call_tool()` handler'ina baglamaniz yeterlidir; katman mimarisi
(decision/cache/observability) degismeden kullanilabilir.
"""
from __future__ import annotations

import json
import sys
from typing import Any

from app.mcp.decision_layer import decision_layer
from app.mcp.observability import observability


def handle_request(request: dict[str, Any]) -> dict[str, Any]:
    method = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")

    if method == "tools/list":
        result: Any = {"tools": decision_layer.available_tools()}
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        try:
            result = {"output": decision_layer.dispatch(tool_name, **arguments)}
        except Exception as exc:  # noqa: BLE001
            return {"id": request_id, "error": str(exc)}
    else:
        return {"id": request_id, "error": f"Bilinmeyen method: {method}"}

    return {"id": request_id, "result": result}


def serve_stdio() -> None:
    """Satir satir JSON-RPC istegi okuyup stdout'a yanit yazan basit dongu."""
    observability.log("mcp.server", "MCP server (stdio) baslatildi")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError as exc:
            print(json.dumps({"error": f"Gecersiz JSON: {exc}"}), flush=True)
            continue

        response = handle_request(request)
        print(json.dumps(response), flush=True)


if __name__ == "__main__":
    serve_stdio()
