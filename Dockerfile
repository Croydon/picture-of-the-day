FROM python:3.14-slim

COPY . /app
WORKDIR /app

RUN pip install -U pip \
    && pip install -U .

CMD ["picture-of-the-day", "run"]
