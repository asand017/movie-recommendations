# Use the official Node.js image from the Docker Hub
FROM node:22

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and yarn.lock files into the container
COPY package.json package-lock.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Build the React app for production
RUN npm run build

# Expose port 3000 to the outside world
EXPOSE 3000

# # Expose the port the app runs on
# EXPOSE 80

# # Command to run the application
# CMD ["nginx", "-g", "daemon off;"]

# # Command to run next.js app
# CMD ["npm", "start"]

# Command to run next.js app
CMD ["npm", "run", "dev"]