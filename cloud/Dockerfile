FROM python:3.9.14-slim
RUN mkdir cloud-service
WORKDIR cloud-service
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD subscribe.py subscribe.py
ADD reciver.py reciver.py
CMD python3 -u subscribe.py & python3 -u reciver.py
