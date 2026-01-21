# Use a lightweight Nginx image
FROM nginx:1.25-alpine

# Set working directory
WORKDIR /usr/share/nginx/html

# Clean the default directory
RUN rm -f *

# Copy all frontend files to the Nginx web root
COPY . .

# Expose port 80 for incoming HTTP traffic
EXPOSE 80

# Nginx base image already has a CMD to start the server
