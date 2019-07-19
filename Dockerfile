FROM python:alpine3.7
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "-m", "hydrate", "run"]