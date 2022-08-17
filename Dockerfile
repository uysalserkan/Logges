#Dockerfile , Image , Container 

FROM python:3.9

ADD main.py .

RUN pip install requirements.txt

CMD ["python", "./main.py"]

