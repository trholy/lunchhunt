FROM python:3.10-slim AS builder

# Install dependencies as root
RUN apt-get update && apt-get install -y \
    curl \
    bash \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Set timezone to Europe/Berlin
RUN ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime && \
    echo "Europe/Berlin" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

# Create a non-root user
RUN useradd --create-home --shell /bin/bash lunchhunt

# Install Miniconda into the user's home directory
RUN curl -sSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /home/lunchhunt/miniconda && \
    rm /tmp/miniconda.sh && \
    chown -R lunchhunt:lunchhunt /home/lunchhunt

# Set environment variables
ENV PATH=/home/lunchhunt/miniconda/bin:$PATH

# Copy the entrypoint script and make it executable
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Switch to non-root user
USER lunchhunt

# Set working directory
WORKDIR /home/lunchhunt/app

# Copy project files (after switching to user)
COPY --chown=lunchhunt:lunchhunt . .

# Create and activate Conda environment
RUN conda create --name lunchhunt python=3.10 -y && \
    echo "source activate lunchhunt" >> /home/lunchhunt/.bashrc

# Use the created environment
ENV PATH=/home/lunchhunt/miniconda/envs/lunchhunt/bin:$PATH

# Install package
RUN pip install --no-cache-dir /home/lunchhunt/app/.

# Expose port
EXPOSE 8050

USER root

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Use CMD to pass the app's command (lunchhunt-web) as an argument to the entrypoint
CMD ["lunchhunt-web"]
