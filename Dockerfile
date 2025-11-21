FROM python:3.8-slim-buster

WORKDIR /app
COPY . /app

# Fix buster apt repositories (they are archived)
RUN sed -i 's|deb.debian.org|archive.debian.org|g' /etc/apt/sources.list \
 && sed -i '/security.debian.org/d' /etc/apt/sources.list \
 && printf 'Acquire::Check-Valid-Until "false";\n' > /etc/apt/apt.conf.d/99no-check-valid-until \
 && apt-get update -o Acquire::Check-Valid-Until=false \
 && apt-get install -y --no-install-recommends awscli ffmpeg libsm6 libxext6 unzip \
 && rm -rf /var/lib/apt/lists/*

# in your Dockerfile (replace the failing RUN)
RUN pip --default-timeout=120 --retries=10 install --no-cache-dir -r requirements.txt

CMD ["python3", "application.py"]
