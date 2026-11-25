FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt fastapi==0.115.6 uvicorn==0.34.0
COPY export_step.py service.py ./
RUN useradd -m cad
USER cad
EXPOSE 8000
CMD ["uvicorn","service:app","--host","0.0.0.0","--port","8000"]
