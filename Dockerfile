FROM python:3.13

WORKDIR /source

COPY requirements.txt .

RUN pip install uv
RUN uv pip install -r requirements.txt --system

COPY . .

RUN chmod +x ci_cd/deploy/command.sh
RUN chmod +x ci_cd/tests/command.sh
