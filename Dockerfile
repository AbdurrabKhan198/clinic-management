# Use the official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    DJANGO_SETTINGS_MODULE=crm.settings

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create and set the working directory
WORKDIR /app

# Create a non-root user
RUN groupadd -r django && useradd -r -g django django

# Copy requirements and install Python dependencies first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional production dependencies
RUN pip install --no-cache-dir \
    gunicorn==21.2.0 \
    whitenoise==6.6.0

# Copy project files
COPY . .

# Create directories for static files and media
RUN mkdir -p /app/static /app/media

# Collect static files
RUN python manage.py collectstatic --noinput

# Change ownership of the app directory to django user
RUN chown -R django:django /app

# Switch to non-root user
USER django

# Expose the port that the app runs on
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/admin/login/ || exit 1

# Run the application with gunicorn
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 crm.wsgi:application 