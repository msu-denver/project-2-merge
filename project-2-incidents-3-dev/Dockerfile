FROM python:3.9-slim-buster

WORKDIR /project-2-incidents-3

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
WORKDIR /project-2-incidents-3/src

# Set the environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV PYTHONPATH=/project-2-incidents-3/src

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
