from app.mcp.decision_layer import decision_layer
from app.mcp.tools.geojson_tool import convert_coordinates, preview_geojson


def test_preview_geojson():
    result = preview_geojson([{"type": "Feature", "geometry": None, "properties": {}}])
    assert result["type"] == "FeatureCollection"
    assert len(result["features"]) == 1


def test_convert_coordinates():
    result = convert_coordinates(lon=28.9784, lat=41.0082)  # Istanbul
    assert "x" in result and "y" in result


def test_decision_layer_dispatch():
    assert "geojson.preview" in decision_layer.available_tools()
    result = decision_layer.dispatch("geojson.convert_coordinates", lon=0, lat=0)
    assert result["x"] == 0.0
    assert abs(result["y"]) < 1e-6
