FROM python:3.11-slim

WORKDIR /app

COPY src src
COPY pyproject.toml .
COPY README.md .  
RUN pip install .
COPY api/requirements.txt .
RUN pip install -r requirements.txt

COPY api api

# This is only acceptable for a demo / prototype
# In production, you want a proper model retrieval strategy
COPY models models

CMD fastapi run --host 0.0.0.0 api/webapi.py --port $PORT