FROM node:18-alpine as builder

WORKDIR /app

# Önce package.json ve package-lock.json kopyala
COPY package*.json ./
RUN npm install

# Sonra diğer dosyaları kopyala
COPY . .

# Production build al
ENV NODE_ENV=production
RUN npm run build

# Nginx ile serve et
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf 