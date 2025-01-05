# Telegram Bot Control Panel

Telegram kanalları arasında mesaj aktarımı yapan ve fiyat güncellemesi yapabilen bir bot kontrol paneli.

## 🚀 Özellikler

- **Mesaj Aktarımı**: Belirlenen kaynak kanallardan hedef kanala otomatik mesaj aktarımı
- **Fiyat Güncelleme**: Mesajlardaki fiyatları otomatik güncelleme ve komisyon ekleme
- **Kontrol Paneli**: Kullanıcı dostu web arayüzü ile kolay yönetim
- **Güvenlik**: Admin şifresi ve Telegram hesap doğrulaması
- **İzleme**: Bot çalışma durumu ve geçmiş kayıtları takibi
- **Otomasyon**: Belirli aralıklarla otomatik çalışma

## 🛠️ Teknolojiler

### Backend
- FastAPI (REST API)
- SQLite (Veritabanı)
- Telethon (Telegram API)
- Python-dotenv (Çevre değişkenleri)
- Pydantic (Veri doğrulama)

### Frontend
- React
- TailwindCSS
- SweetAlert2

## 📋 Gereksinimler

- Python 3.11+
- Node.js 18+
- Docker (opsiyonel)

## ⚙️ Kurulum

### Docker ile Kurulum

1. Projeyi klonlayın:

```bash
git clone https://github.com/username/telegram-bot-panel.git
cd telegram-bot-panel
```

2. .env dosyasını oluşturun:

```env
ADMIN_PASSWORD=your_password
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
PHONE_NUMBER=your_phone_number
SOURCE_CHANNELS=["channel1", "channel2"]
TARGET_CHANNEL=target_channel
ADD_FEE=20
GEMINI_API_KEY=your_gemini_api_key
IS_ACTIVE=true
INTERVAL_MINUTES=60
```

3. Docker compose ile başlatın:

```bash
docker compose up -d
```


## 📱 Kullanım

1. Web tarayıcısında `http://localhost` adresine gidin
2. Admin şifresi ile giriş yapın
3. Telegram hesabınızla bot girişi yapın
4. Kaynak ve hedef kanalları yapılandırın
5. Bot durumunu aktif edin
6. Çalışma geçmişini takip edin

## ⚠️ Önemli Notlar

- Telegram API bilgilerini [my.telegram.org](https://my.telegram.org) adresinden alabilirsiniz
- Bot aktif edilmeden önce tüm ayarların doğru yapılandırıldığından emin olun
- Kaynak kanalların public olması gerekiyor
- Hedef kanalda bot admin olmalıdır
- Gemini API keyi için [Google Cloud Console](https://console.cloud.google.com/) adresinden bir API key oluşturun ve bu değeri .env dosyanıza ekleyin

## 🔧 Yapılandırma

Temel yapılandırma seçenekleri:

| Seçenek | Açıklama | Varsayılan |
|---------|----------|------------|
| `ADMIN_PASSWORD` | Kontrol paneli şifresi | - |
| `API_ID` | Telegram API ID | - |
| `API_HASH` | Telegram API Hash | - |
| `SOURCE_CHANNELS` | Kaynak kanal listesi | `[]` |
| `TARGET_CHANNEL` | Hedef kanal | - |
| `ADD_FEE` | Eklenecek komisyon | `0` |
| `INTERVAL_MINUTES` | Çalışma aralığı (dakika) | `60` |


## 🙏 Teşekkürler

- [Telethon](https://github.com/LonamiWebs/Telethon)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [TailwindCSS](https://tailwindcss.com/)