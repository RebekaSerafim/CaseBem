FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip git

WORKDIR /app

RUN git clone https://github.com/RebekaSerafim/CaseBem.git .
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]