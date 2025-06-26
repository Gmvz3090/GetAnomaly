FROM python:3.9-slim

WORKDIR /app

RUN pip install fastapi[standard] pymongo pandas pyarrow  

COPY . . 

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

