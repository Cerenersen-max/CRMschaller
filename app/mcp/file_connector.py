"""Not: 'Dosya ve baglantilarim - Icin mcp dosyasini, aktim icerisine biriktir
klasoru ekledim.' Bu katman MCP sunucusunun okuyabilecegi dosya/klasor
baglantilarini yonetir ('Dosya ve baglantilar katmani')."""
from __future__ import annotations

from pathlib import Path

# 'biriktir' klasoru: MCP sunucusunun uzerinde calisacagi dosyalarin toplandigi yer.
BIRIKTIR_DIR = Path(__file__).resolve().parent.parent.parent / "mcp_biriktir"


class FileConnector:
    """Dosya ve baglanti katmani: izin verilen dizinleri/dosyalari kayit altina alir."""

    def __init__(self, base_dir: Path = BIRIKTIR_DIR):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._registered_paths: set[Path] = {self.base_dir}

    def register(self, path: str | Path) -> Path:
        resolved = Path(path).resolve()
        self._registered_paths.add(resolved)
        return resolved

    def is_allowed(self, path: str | Path) -> bool:
        resolved = Path(path).resolve()
        return any(
            resolved == registered or registered in resolved.parents
            for registered in self._registered_paths
        )

    def list_files(self) -> list[str]:
        return [str(p) for p in self.base_dir.rglob("*") if p.is_file()]

    def read_file(self, path: str | Path) -> str:
        if not self.is_allowed(path):
            raise PermissionError(f"'{path}' MCP dosya baglanti katmani tarafindan izinli degil")
        return Path(path).read_text(encoding="utf-8")

    def write_file(self, filename: str, content: str) -> Path:
        target = self.base_dir / filename
        target.write_text(content, encoding="utf-8")
        return target
