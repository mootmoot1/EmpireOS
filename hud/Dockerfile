FROM node:20-alpine
WORKDIR /app
# Copy manifest first for cached installs
COPY hud/package.json hud/package-lock.json* ./
RUN npm install --legacy-peer-deps
# Copy the HUD app source
COPY hud/. .
EXPOSE 3000
CMD ["npm","run","dev"]
