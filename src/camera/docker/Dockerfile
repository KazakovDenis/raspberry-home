FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements/ ./requirements/
RUN pip install --no-cache-dir -r requirements/prod.txt

COPY . .

CMD [ "./docker/entrypoint.sh" ]
