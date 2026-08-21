# CRMschaller

CRM / operasyon backend'i: yatırımcı-partner takibi, envanter şablonu, lojistik
dosyaları, banka ekstresi entegrasyonu, admin panel (export + muhasebe
entegrasyonu), günlük otomatik sistem raporu, MCP server iskeleti ve
Kubernetes/Telegram yönetim botu.

El yazısı defter notlarının hangi dosyaya karşılık geldiğini görmek için
[`docs/notlar.md`](docs/notlar.md) dosyasına bakın.

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # gerekli API anahtarlarini doldurun
```

## API'yi çalıştırma

```bash
uvicorn app.main:app --reload
```

- `GET /health` — sağlık kontrolü
- `/investors`, `/inventory`, `/logistics`, `/meetings` — CRUD uç noktaları
- `GET /investors/{id}/outreach-email-preview` — partner için MIME e-posta önizlemesi
- `/banks/accounts`, `POST /banks/accounts/{id}/sync`, `/banks/fx-rates` — banka entegrasyonu
- `/admin/export/transactions.csv|.xlsx`, `/admin/export/accounting-sync` — admin panel
- `/reports/daily/run`, `/reports/daily/latest` — günlük sistem raporu

## Defter notlarını veritabanına işleme

Tüm sayfalardaki ortak/yatırımcı (KWORKS, Türk Telekom Ventures, Sabancı, Ore
Chase, Aston Martin) ve haftalık toplantı (GUCA) kayıtlarını tek seferde
eklemek için:

```bash
python -m scripts.seed_partners
```

## Telegram bot

```bash
python -m app.bot.telegram_bot
```

`.env` içindeki `TELEGRAM_BOT_TOKEN` ve `KUBE_CONFIG_PATH` doldurulmalı.
Komutlar: `/status`, `/logs <deployment> [tail]`, `/scale <deployment> <replicas>`,
`/deploy <deployment> <image>`.

## MCP server

```bash
python -m app.mcp.server
```

stdin üzerinden `{"id": 1, "method": "tools/list"}` gibi JSON-RPC satırları
okur; mimari katmanlar (`file_connector` → `decision_layer` → `cache_layer` →
`observability`) `app/mcp/` altında ayrı modüller olarak tutulur.

## Test

```bash
pytest
```
