FROM python:3.13-slim

# Install uv package manager
RUN curl -fsSL https://get.uv.so | bash

WORKDIR /app

COPY . .

# Install dependencies using uv
RUN uv install


ENTRYPOINT ["uv", "run", "main.py"]
