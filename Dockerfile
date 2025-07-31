FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ app/
ENV FLASK_APP=app/rate_limit.py
ENV PYTHONUNBUFFERED=1
CMD ["flask", "run", "--host=0.0.0.0"]