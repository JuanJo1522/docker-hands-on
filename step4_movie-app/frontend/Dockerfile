FROM node:22-alpine AS beeq-assets
WORKDIR /build
COPY package.json ./package.json
RUN npm install --no-audit --no-fund

FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
# The ESM entry point imports hashed JavaScript chunks from this directory.
# Copy the whole distribution so those relative imports resolve in the browser.
COPY --from=beeq-assets /build/node_modules/@beeq/core/dist/beeq/ /usr/share/nginx/html/vendor/

EXPOSE 80
