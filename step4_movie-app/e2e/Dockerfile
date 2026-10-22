FROM mcr.microsoft.com/playwright:v1.52.0-noble
WORKDIR /tests
COPY package.json ./package.json
RUN npm install --no-save @playwright/test@1.52.0
COPY playwright.config.js ./playwright.config.js
COPY movie-app.spec.js ./movie-app.spec.js
CMD ["npx", "playwright", "test"]
