# Use Ubuntu as base image
FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && \
    apt-get install -y \
    fortune-mod \
    cowsay \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Add cowsay to PATH
ENV PATH="/usr/games:${PATH}"

# Set working directory
WORKDIR /app

# Copy the wisecow script
COPY wisecow.sh .

# Make the script executable
RUN chmod +x wisecow.sh

# Expose port 4499
EXPOSE 4499

# Run the wisecow application
CMD ["./wisecow.sh"]
