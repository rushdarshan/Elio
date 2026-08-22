# ELIO — Next.js cockpit + Python 9-stage DAG (single container)
# Render Docker: builds Node + Python in one image, no extra services.
FROM node:20-bullseye

ENV PYTHONUNBUFFERED=1
ENV NEXT_TELEMETRY_DISABLED=1

WORKDIR /app

# System deps (python3 already in bullseye, ensure pip)
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*

# Python deps — ponytail: only what pipeline imports (pandas/pydantic/openpyxl)
COPY unihack_catalog ./unihack_catalog
COPY scripts ./scripts
COPY data ./data
# Install minimal Python deps (no requirements.txt in repo)
RUN pip3 install --no-cache-dir pandas pydantic openpyxl

# Node deps + build
COPY elio-frontend/package.json elio-frontend/package-lock.json* ./elio-frontend/
RUN cd elio-frontend && npm install

COPY elio-frontend ./elio-frontend
# Copy repo-level files needed at runtime (artifacts for demo data)
COPY artifacts ./artifacts
COPY app.py ./app.py

RUN cd elio-frontend && npm run build

# Runtime
WORKDIR /app/elio-frontend
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

# Next reads PORT, cockpit's api/run spawns python3 ../scripts/run_pipeline_cli.py
CMD ["npm", "start"]
