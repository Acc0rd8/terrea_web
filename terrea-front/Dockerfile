# Official Node.js
FROM node:16 AS build

# Create work directory
RUN mkdir /web

# Redirect in work directory
WORKDIR /web

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all files
COPY . .

# Run project
RUN npm run build

# Nginx
FROM nginx:alpine

# Copy from previoues step
COPY --from=build /web/build /usr/share/nginx/html

# Copy Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Open port 80
EXPOSE 80

# start Nginx
CMD ["nginx", "-g", "daemon off;"]