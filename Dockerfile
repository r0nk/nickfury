FROM python:3

RUN pip install discord

COPY . .

CMD python3 nick_fury.py


