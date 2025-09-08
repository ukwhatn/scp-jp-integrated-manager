FROM python:3.11-slim

ENV PYTHONPATH "${PYTHONPATH}:/user_modules"

WORKDIR /app

COPY script/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY db/requirements.txt /db_requirements.txt
RUN pip install -r /db_requirements.txt

WORKDIR /app/src

CMD ["python", "main.py"]
