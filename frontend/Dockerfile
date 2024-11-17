# Use node:22-alpine as the base image
FROM node:22-alpine

# Set the environment variables
# This is required to run the application in production mode
# Check: https://nextjs.org/docs/app/building-your-application/deploying#environment-variables
ENV NEXT_PUBLIC_LANGGRAPH_ASSISTANT_ID=agent

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

# Expose port 3000
EXPOSE 3000

# Set the command to run the application using npm start
CMD ["npm", "start"]
