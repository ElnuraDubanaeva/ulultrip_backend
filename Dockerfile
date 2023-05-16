FROM python:3.10

RUN mkdir -p /home/app

WORKDIR /home/app/

COPY . /home/app/

COPY requirements.txt /home/app/

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver"]
