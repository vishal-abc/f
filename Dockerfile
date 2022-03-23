FROM python:3.8-slim-buster
WORKDIR /demo.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "demo.py"]