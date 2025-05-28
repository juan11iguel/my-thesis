FROM texlive/texlive:latest

USER root

# Install additional packages
RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
        fonts-liberation \
        xclip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*