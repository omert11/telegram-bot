#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Telegram Bot Panel Başlatılıyor...${NC}"

touch bot.db
touch bot.log

if [ ! -f .env ]; then
    echo -e "${GREEN}.env dosyası oluşturuluyor...${NC}"
    cat > .env << 'EOL'
ADMIN_PASSWORD=your_password
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
PHONE_NUMBER=your_phone_number
SOURCE_CHANNELS=["channel1", "channel2"]
TARGET_CHANNEL=target_channel
ADD_FEE=20
GEMINI_API_KEY=your_gemini_api_key
IS_ACTIVE=false
INTERVAL_MINUTES=60
EOL
fi

chmod 666 bot.db bot.log .env

echo -e "${GREEN}Docker container'ları başlatılıyor...${NC}"
docker compose up --build -d

echo -e "${GREEN}Container durumları:${NC}"
docker compose ps

echo -e "${YELLOW}Başlatma işlemi tamamlandı!${NC}"
echo -e "${GREEN}Uygulamaya http://localhost adresinden erişebilirsiniz.${NC}" 