FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

# Declare build arg BEFORE copying source so it overrides .env
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
