FROM buildpack-deps:stretch

ENV PYTHON_VERSION 3.6.4
ENV PREFIX https://www.python.org/ftp/python
ENV LANG C.UTF-8
ENV GPG_KEY 0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
        tcl \
        tk \
        dpkg-dev \
        tcl-dev \
        tk-dev
RUN wget -O python.tar.xz "$PREFIX/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz"
RUN wget -O python.tar.xz.asc "$PREFIX/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc"
RUN export GNUPGHOME="$(mktemp -d)" && \
        gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "$GPG_KEY" && \
        gpg --batch --verify python.tar.xz.asc python.tar.xz
RUN mkdir -p /usr/src/python
RUN tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz

WORKDIR /usr/src/python

RUN gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)"
RUN ./configure \
        --build="$gnuArch" \
        --enable-loadable-sqlite-extensions \
        --enable-shared \
        --prefix=/opt/custom-python/
RUN make -j
RUN make install
RUN ldconfig /opt/custom-python/lib
RUN /opt/custom-python/bin/python3 -m pip install twisted

FROM debian:stretch
COPY --from=0 /opt/custom-python /opt/custom-python
RUN apt-get update
RUN apt-get install libffi6 \
        libssl1.1 && \
        ldconfig /opt/custom-python/lib
ENTRYPOINT ["/opt/custom-python/bin/python3", "-m", "twisted", "web"]