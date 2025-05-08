FROM python:3.10-slim AS builder

# Install dependencies as root
RUN apt-get update && apt-get install -y \
    bash \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home --shell /bin/bash lunchhunt

# Set working directory
WORKDIR /home/lunchhunt/app

# Copy the entrypoint script and make it executable
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Copy project files (after switching to user)
COPY --chown=lunchhunt:lunchhunt . .

# Install package
RUN pip install --no-cache-dir .

# Set environment variables
ENV PATH=/home/lunchhunt/app:$PATH

# Create a directory for the app to write files
RUN chown -R lunchhunt:lunchhunt /home/lunchhunt/app/

# Expose port
EXPOSE 8050

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Use CMD to pass the app's command (lunchhunt-web) as an argument to the entrypoint
CMD ["lunchhunt-web"]
