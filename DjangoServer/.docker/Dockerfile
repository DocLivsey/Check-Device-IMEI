FROM --platform=$BUILDPLATFORM python:3.7-alpine AS builder

WORKDIR /app

COPY ../requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY .. /app

RUN python3 manage.py migrate

ENTRYPOINT ["python3"]
EXPOSE 8000
CMD ["manage.py", "runserver", "0.0.0.0:8000"]