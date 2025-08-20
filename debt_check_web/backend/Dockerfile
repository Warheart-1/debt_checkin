FROM python:3.13-slim-bookworm
LABEL authors="aselebran"
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin:$PATH"

COPY requirements.txt .

RUN uv pip install --system -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host","0.0.0.0","--port","8000"]