FROM python:latest

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update
RUN apt-get install -y supervisor
COPY ./supervisor.conf /etc/supervisor/conf.d/supervisord.conf

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . ./

RUN chmod +x ./start.sh
CMD ["./start.sh"]