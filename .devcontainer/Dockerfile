FROM texlive/texlive:latest

USER root

# Environment variables. uv
# ENV UV_PROJECT_ENVIRONMENT=/venvs

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
# COPY --from=ghcr.io/astral-sh/uv:0.7.9 /uv /bin/uv
# ADD https://astral.sh/uv/install.sh /uv-installer.sh
# RUN sh /uv-installer.sh && rm /uv-installer.sh
# ENV PATH="/root/.local/bin/bin/:$PATH"
# RUN uv --version

# # Set up virtual environment
# COPY ./README.md ./pyproject.toml ./uv.lock* $WORKDIR
# RUN uv sync