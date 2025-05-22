# Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Copia só o requirements primeiro (para cache funcionar melhor)
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante da aplicação
COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
