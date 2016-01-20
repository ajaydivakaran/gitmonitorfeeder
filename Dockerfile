FROM python:3.4.4
RUN mkdir workspace
COPY requirements.pip workspace/requirements.pip
RUN pip install -r workspace/requirements.pip
COPY repo_scan workspace/repo_scan
COPY start.sh workspace/
WORKDIR /workspace
CMD ["./start.sh"]