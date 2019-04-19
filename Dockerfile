FROM python:3

COPY . /h4sh3m784/MonitorTool

WORKDIR /h4sh3m784/MonitorTool

RUN pip install -r requirements.txt

USER root

CMD ["./preconfig.sh"]
