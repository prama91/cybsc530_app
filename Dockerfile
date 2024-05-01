# syntax=docker/dockerfile:1

FROM python:3.12.3-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Expose port 5000 for the Flask application
EXPOSE 5000

CMD [ "python3", "app.py", "--host=0.0.0.0", "--port=5000"]