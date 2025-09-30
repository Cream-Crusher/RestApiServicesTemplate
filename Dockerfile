FROM python:3.13 AS compile-image

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD ["python", "__main__.py", "--server"]
