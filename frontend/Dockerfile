# Geliştirme (Build) aşaması
FROM node:18-alpine AS build-stage

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
# Sizin Nginx proxynize uyum sağlamak için boş bırakıyoruz
# Böylece /api... şeklindeki istekler Nginx'e (dolayısıyla backend'e) gidecek.
ENV VITE_API_URL="" 
RUN npm run build

# Üretim (Production) aşaması - Nginx
FROM nginx:alpine

# Derlenen dosyaları nginx'e taşıyın
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Özel Nginx konfigürasyonunu kopyalayın
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
