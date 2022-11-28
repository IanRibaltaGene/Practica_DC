FROM python:3.9.14-slim
RUN mkdir script
WORKDIR script
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD subscribe.py subscribe.py
ADD reciver.py reciver.py
ADD script.sh script.sh
CMD ["./script.sh"]
