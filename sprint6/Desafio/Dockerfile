FROM python:3.10-slim

WORKDIR /app

COPY sprint6.py /app/sprint6.py

RUN pip install boto3

ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV AWS_SESSION_TOKEN=""

ENTRYPOINT ["python", "sprint6.py"]