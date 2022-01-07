FROM python:3.9

EXPOSE 10000

COPY ./ /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
