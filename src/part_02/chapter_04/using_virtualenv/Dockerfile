FROM python:3
RUN python -m venv /opt/venv-python
RUN /opt/venv-python/bin/pip install Twisted

FROM python:3-slim
COPY --from=0 /opt/venv-python /opt/venv-python
ENTRYPOINT ["/opt/venv-python/bin/python", "-m", "twisted", "web"]