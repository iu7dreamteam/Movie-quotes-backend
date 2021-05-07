FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
WORKDIR /code/src
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
# RUN python3 manage.py runserver
EXPOSE 5432 8000