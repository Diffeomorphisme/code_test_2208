FROM python:3

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./setup.py /app/setup.py

RUN pip3 install -e .
RUN pip3 install -r requirements.txt

EXPOSE 5000
COPY . .
ENTRYPOINT ["python"]
CMD ["./src/main.py" ]