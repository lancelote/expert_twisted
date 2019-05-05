FROM python:3
RUN python -m venv /opt/venv-python
RUN /opt/venv-python/bin/pip install pex wheel
RUN mkdir /opt/wheels /opt/pex
RUN /opt/venv-python/bin/pip wheel --wheel-dir /opt/wheels Twisted
RUN /opt/venv-python/bin/pex --find-links /opt/wheels --no-index Twisted -m twisted -o /opt/pex/twisted.pex

FROM python:3-slim
COPY --from=0 /opt/pex /opt/pex
ENTRYPOINT ["/opt/pex/twisted.pex", "web"]