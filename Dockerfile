FROM python:3.12

WORKDIR /source

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ci_cd/deploy/command.sh
RUN chmod +x ci_cd/tests/command.sh
