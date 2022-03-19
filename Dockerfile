FROM python:3.8-slim-buster
WORKDIR /demo.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 1001
COPY . .
CMD ["python3", "demo.py"]