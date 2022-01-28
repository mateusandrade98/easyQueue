FROM python:3.9
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . /app
#CMD ["python","-u","run.py"]
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["python", "-u", "worker.py"]