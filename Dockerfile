FROM python:3.13-slim

# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies using uv
RUN uv install

WORKDIR /app

COPY . .


ENTRYPOINT ["uv", "run", "main.py"]
