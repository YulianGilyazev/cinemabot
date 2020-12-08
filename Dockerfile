FROM python:3

COPY . /

RUN pip install -r requirements.txt

ENTRYPOINT ["bash", "run.sh"]