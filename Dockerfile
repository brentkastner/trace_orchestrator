FROM python:3.9
ADD . /src
WORKDIR /src
COPY /src/ /src/

EXPOSE 3000

# install apt system dependencies
RUN apt-get update && apt-get install -y sqlite3 && pip install --upgrade pip==23.1.2

RUN pip install -r requirements.txt

CMD [ "gunicorn", "--bind", "0.0.0.0:3000", "--workers", "4", "app:app"]