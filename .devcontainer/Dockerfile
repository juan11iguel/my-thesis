FROM texlive/texlive:latest

USER root

# Install additional packages
RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
        fonts-liberation \
        xclip \
        pdf2svg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python
# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.7.9 /uv /bin/uv
RUN uv --version