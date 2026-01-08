FROM texlive/texlive:TL2024-historic

USER root

# Environment variables. uv
# ENV UV_PROJECT_ENVIRONMENT=/venvs

# Install additional packages
RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
        fonts-liberation \
        xclip \
        ghostscript \
        pdf2svg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python
# Install uv
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh
# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh
# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"
RUN uv --version

# # Set up virtual environment
# COPY ./README.md ./pyproject.toml ./uv.lock* $WORKDIR
# RUN uv sync