FROM python:3.7

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/app

ENTRYPOINT ["python3", "/code/app/consume.py"]
##CMD ["10","200"]