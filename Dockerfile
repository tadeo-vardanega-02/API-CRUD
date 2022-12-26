FROM python:3.8-alpine

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /home/app/

COPY . /home/app/

RUN pip3 install -r requirements.txt

CMD ["uvicorn" ,"main:app", "--host", "0.0.0.0", "--port", "5000"] 