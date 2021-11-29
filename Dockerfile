FROM python:3.9

EXPOSE 8080

COPY ./ /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]