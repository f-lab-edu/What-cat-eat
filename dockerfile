FROM python:3.10

WORKDIR /What-cat-eat

COPY ./requirements.txt ./requirements.txt

RUN pip install --default-timeout=300 --no-cache-dir --upgrade -r ./requirements.txt

COPY ./ ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]