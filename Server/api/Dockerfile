FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /code

ENV SECRET_KEY=$SECRET_KEY
ENV DB_HOST=$DB_HOST
ENV DB_USER=$DB_USER
ENV DB_PASSWORD=$DB_PASSWORD

ENV DB_SERVICE_HOST=${DB_SERVICE_HOST:db}
ENV DB_SERVICE_PORT=${DB_SERVICE_PORT:-5432}

#RUN /usr/local/bin/python -m pip install --upgrade pip
RUN /usr/local/bin/python3 -m pip install --upgrade pip

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

