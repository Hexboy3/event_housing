# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:slim

EXPOSE 5000



ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV="development"

RUN apt-get update \ 
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2


COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /event_housing
COPY . /event_housing

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /event_housing
USER appuser


CMD ["flask", "run", "--host", "0.0.0.0"]
