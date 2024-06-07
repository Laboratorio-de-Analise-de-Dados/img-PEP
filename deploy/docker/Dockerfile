FROM python:3.7

LABEL maintainer="Guilherme F Silveira"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common

COPY ./requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8502

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# ENTRYPOINT ["streamlit", "hello", "--server.port=8502", "--server.address=0.0.0.0"]
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8502", "--server.address=0.0.0.0"]