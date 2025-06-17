FROM node:18-alpine as builder

WORKDIR /app

# Copie les fichiers de config et environnement
COPY package*.json ./
COPY vite.config.js ./
COPY .env .env
COPY index.html ./
COPY src ./src

RUN npm install
RUN npm run build

# Serveur nginx pour prod
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
