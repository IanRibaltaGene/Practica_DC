FROM python:3.9.14-slim
RUN mkdir script
WORKDIR script
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD publish.py publish.py
ADD data2.csv data.csv
CMD ["python3","-u","publish.py"]
