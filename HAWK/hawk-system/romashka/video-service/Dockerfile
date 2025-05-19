FROM python:3.12-slim

WORKDIR /module

COPY . . 

RUN pip install -r ./config/requirements.txt

CMD [ "python", "start.py" ]