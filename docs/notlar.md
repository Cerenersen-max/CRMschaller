# El Yazısı Notlardan Kod Eşleştirmesi

Bu belge, defter sayfalarındaki notların hangi kod dosyasına karşılık geldiğini özetler.

## Ortaklık / Yatırımcı Takibi
- "PARTNER - Ore Chase - Techstars süreci yapıldı fizda inceleme ile devam edecek, dosyalar yüklenecek"
- "KWORKS (Stratejik ortaklıklar)", "Türk Telekom Ventures (bulut sistem desteği veri tabanı sunumu)", "Sabancı (yatırımcı sunumu genel değerlendirme)"
- "Lojistik dosyası oluşturuldu, bankalara mail iletildi en uygun görüşme yapılacak"

→ `app/models/investor.py`, `app/routers/investors.py`
→ `app/models/logistics.py`, `app/routers/logistics.py`

## Envanter Şablonu
- "Envanter Şablonu → SPOFF analizi, SIA|RPO|ETO → Veri modeli/Sözleşme API, Dock, Faz-1"

→ `app/models/inventory.py`, `app/routers/inventory.py`

## Banka Statemleri
- "Nordea/Open Banking API → anlık SEPA ödemeleri, Hesap bilgisi statemleri"
- "İş Bankası // Kuveyt Türk (Arap Emirates) ← FX oran entegrasyonu"

→ `app/models/bank.py`, `app/services/bank_integration.py`, `app/routers/banks.py`

## MASTER DOCUMENT
- "Admin Panel sistemine bankaları eklediğimiz bir panel yönetim sistemi oluşturuyoruz."
- "CSV/Excel export, muhasebe API entegrasyonu"
- "Her gün sistem raporlaması gün sonu otomatik"

→ `app/routers/admin.py`, `app/services/accounting_export.py`, `app/services/report_scheduler.py`, `app/routers/reports.py`

## 4-) Telegram Bot
- "/status, /logs, /scale up, /deploy prod gibi komutlar ile yönetim"
- "Bot → Python telegram bot kütüphanesi, K8s API'ye bağlanır"

→ `app/bot/telegram_bot.py`, `app/bot/k8s_client.py`

Not: "Fluent toplayıcı → ngrok / AWS S3 / GCP-BQ / Azure LA" ve "Veri tabanına Servbay
eklentisi" notları altyapı/log toplama konfigürasyonuna işaret ediyor; bu repo
kapsamında kod tarafı `app/mcp/observability.py` (syslog + IntegrationLog) ile
karşılanıyor. Fluent Bit/Fluentd toplayıcının hangi sink'e (S3/BigQuery/Azure Log
Analytics) yönlendirileceği; canlı altyapı kurulurken `infra/` altına eklenmelidir.

## MCP Server İçin
- "Dosya ve bağlantılarım... modelcontextprotocol.io/docs, docs.mapbox.com"
- "Devkit mcp Server → Preview GeoJSON and convert coordinates"
- "ARDINDAN sistemli mimari: İşleme Katmanı, Karar/Orkestrasyon Katmanı, Yedek
  bağlantı katmanı, Gözlem & Log katmanı"

→ `app/mcp/file_connector.py` (dosya/bağlantı katmanı)
→ `app/mcp/decision_layer.py` (karar/orkestrasyon katmanı)
→ `app/mcp/cache_layer.py` (yedek bağlantı katmanı)
→ `app/mcp/observability.py` (gözlem & log katmanı)
→ `app/mcp/tools/geojson_tool.py` (GeoJSON preview + koordinat dönüşümü)
→ `app/mcp/server.py` (stdio JSON-RPC giriş noktası; resmi MCP Python SDK'ya
  geçiş için not içerir)

## Açık / sonraki adımlar
- Banka API kimlik bilgileri (.env) girilmeden `bank_integration.py`
  istemcileri "dry-run" modda çalışır — gerçek IBAN/erişim bilgileri
  eklendiğinde otomatik olarak canlıya geçer.
- Muhasebe API entegrasyonu (`ACCOUNTING_API_URL`) tanımlı değilse export
  endpoint'i sadece kaç kaydın gönderileceğini raporlar (dry-run).
- Telegram bot K8s cluster dışında (yerel geliştirmede) `K8sClient.connected =
  False` döner ve komutlar bilgilendirici mesaj verir.
