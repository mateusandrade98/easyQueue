FROM python:3.9
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . /app
CMD ["docker", "run", "--name", "my-redis", "-p", "6379:6379", "-d", "redis"]
CMD ["python", "-u", "run.py"]
#CMD ["python", "-u", "worker.py"]