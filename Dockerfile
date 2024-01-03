FROM python:3.10

COPY requirements.txt .
COPY requirements_advanced.txt .

RUN pip install -r requirements.txt
RUN pip install opentelemetry-distro==0.41b0 opentelemetry-exporter-otlp==1.20.0

RUN opentelemetry-bootstrap -a install

COPY . /app
WORKDIR /app
ENV dockerrun=yes
CMD ["python3", "-u", "ChuanhuChatbot.py","2>&1", "|", "tee", "/var/log/application.log"]
