# Dockerfile
FROM python:3.10-slim-buster

LABEL maintainer="poorya189@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY ./requirements.txt .

# RUN pip install -i https://mirror-pypi.runflare.com/simple --upgrade pip \
#     && pip install -i https://mirror-pypi.runflare.com/simple --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY ./core .

# RUN python manage.py migrate

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# terminal command: docker build -t django-app .
# terminal command checking to succeeding to build image : docker images
# terminal command: docker run -p 8000:8000 django-app
# check in browser: http://127.0.0.1:8000/