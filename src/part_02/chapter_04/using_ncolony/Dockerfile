FROM python:3
RUN python3 -m venv /application/env
RUN /application/env/bin/pip install ncolony
RUN mkdir /application/config /application/messages
RUN /application/env/bin/python -m ncolony \
    --config /application/config \
    --messages /application/messages \
    ctl \
    --cmd /application/env/bin/python \
    --arg=-m \
    --arg=twisted \
    --arg=web

FROM python:3-slim
COPY --from=0 /application/ /application/
ENTRYPOINT ["/application/env/bin/python", \
            "-m", \
            "twisted", \
            "ncolony", \
            "--config", "/application/config", \
            "--messages", "/application/messages"]