# Use node:22-alpine as the base image
FROM node:22-alpine

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package.json package-lock.json ./

# Run npm install to install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Build the Next.js application using npm run build
RUN npm run build

# Delete the .env file if it exists
RUN if [ -f .env ]; then rm .env; fi

# Expose port 3000
EXPOSE 3000

# Set the command to run the application using npm start
CMD ["npm", "start"]
