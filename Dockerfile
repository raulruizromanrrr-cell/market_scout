FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . /app

# Expose the default port for Hugging Face Spaces
EXPOSE 7860

# Run the proxy server
CMD ["python", "proxy.py"]
