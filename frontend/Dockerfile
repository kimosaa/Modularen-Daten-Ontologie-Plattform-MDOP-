# Multi-stage build for MDOP Frontend
FROM node:18-alpine as base

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Development
CMD ["npm", "run", "dev", "--", "--host"]
