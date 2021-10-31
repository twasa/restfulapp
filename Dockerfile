FROM python:3.9.7-slim-bullseye as builder
ADD . /opt
ARG git_tag
ARG git_commit
ENV GIT_TAG=$git_tag
ENV GIT_COMMIT=$git_commit
WORKDIR /opt
RUN apt-get update && \  
    # apt-get install -y build-essential && \
    pip install poetry==1.1.11 && \
    poetry install --no-dev --no-root

FROM python:3.9.7-slim-bullseye
ARG git_tag
ARG git_commit
ENV GIT_TAG=$git_tag
ENV GIT_COMMIT=$git_commit
COPY --from=builder /opt /opt
COPY ./entrypoint.sh /opt
WORKDIR /opt
RUN chmod +x /opt/entrypoint.sh && \
    pip install poetry==1.1.11
ENTRYPOINT [ "/opt/entrypoint.sh" ]
