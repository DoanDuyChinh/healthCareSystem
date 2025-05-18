FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . /app/

# Fix permissions for entrypoint script - make sure this is effective
RUN chmod +x /app/entrypoint.sh && \
    ls -la /app/entrypoint.sh

# Default command if the entrypoint isn't executable for some reason
CMD ["bash", "-c", "chmod +x /app/entrypoint.sh && /app/entrypoint.sh"]
