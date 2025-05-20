FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements-slim.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-slim.txt

# Copy project files
COPY . .

# Create app user for security
RUN groupadd -r rnaapp && useradd -r -g rnaapp rnaapp \
    && chown -R rnaapp:rnaapp /app

# Create necessary directories
RUN mkdir -p /app/media/figures /app/static /app/logs /app/backups
RUN mkdir -p /app/backups/postgres /app/backups/weaviate /app/backups/media

# Copy and set permissions for entrypoint script
COPY --chown=rnaapp:rnaapp docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# Set proper ownership and switch to non-root user
USER rnaapp

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
ENTRYPOINT ["/app/docker-entrypoint.sh"]