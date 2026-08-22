"""Not: 'Devkit mcp Server -> Preview GeoJSON and convert coordinates'
(bkz. docs.mapbox.com). Lojistik/envanter konumlarini GeoJSON olarak
onizlemek ve koordinat sistemleri arasi donusum yapmak icin basit araclar."""
from __future__ import annotations

import math
from typing import Any

# WGS84 (EPSG:4326, lat/lon) <-> Web Mercator (EPSG:3857) donusumu; Mapbox
# tabanli haritalama akislarinda en sik ihtiyac duyulan donusumdur.
_EARTH_RADIUS = 6378137.0


def preview_geojson(features: list[dict[str, Any]]) -> dict[str, Any]:
    """Verilen ozellik listesini bir GeoJSON FeatureCollection'a sarar."""
    return {"type": "FeatureCollection", "features": features}


def convert_coordinates(
    lon: float, lat: float, to: str = "EPSG:3857"
) -> dict[str, float]:
    """WGS84 (EPSG:4326) koordinatini istenen sisteme cevirir.

    Su an sadece EPSG:3857 (Web Mercator) destekleniyor; baska bir hedef
    sistem icin pyproj gibi bir kutuphane eklenmesi onerilir.
    """
    if to != "EPSG:3857":
        raise ValueError(f"Desteklenmeyen hedef koordinat sistemi: {to}")

    x = lon * (math.pi / 180) * _EARTH_RADIUS
    y = (
        math.log(math.tan((math.pi / 4) + ((lat * (math.pi / 180)) / 2)))
        * _EARTH_RADIUS
    )
    return {"x": x, "y": y}
