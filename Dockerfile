FROM ubuntu:17.10

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git
RUN apt-get install -y zip

# update pip
RUN python3.6 -m pip install --upgrade pip==9.0.3
RUN python3.6 -m pip install wheel virtualenv
RUN cd /usr/local/bin && ln -s /usr/bin/python3 python

# Install Postgres 9.X

ENV PG_VERSION 9.6
ENV PG_BASE /var/lib/postgresql
ENV PG_DATA ${PG_BASE}/${PG_VERSION}/main
ENV PG_CONFIG_DIR /etc/postgresql/${PG_VERSION}/main
ENV PG_CONFIG_FILE ${PG_CONFIG_DIR}/postgresql.conf
ENV PG_BINDIR /usr/lib/postgresql/${PG_VERSION}/bin

RUN apt-get install -y postgresql-$PG_VERSION

RUN echo "host all  all    0.0.0.0/0  trust" >> $PG_CONFIG_DIR/pg_hba.conf \
      && echo "host all  all    ::/0  trust" >> $PG_CONFIG_DIR/pg_hba.conf \
      && echo "listen_addresses='*'" >> $PG_CONFIG_FILE

COPY docker-entrypoint.sh /usr/local/bin/
RUN ln -s usr/local/bin/docker-entrypoint.sh /
RUN ["chmod", "u+x", "/usr/local/bin/docker-entrypoint.sh"]
USER postgres

# Not sure whats going on here - Ran into some strange docker error - maybe Mac specific?
# ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 5432
