FROM python:3.12

RUN mkdir /terrea

WORKDIR /terrea

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /terrea/docker/*.sh