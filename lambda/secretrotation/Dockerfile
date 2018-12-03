FROM amazonlinux:2017.03
RUN yum update -y && yum install -y zip
RUN yum install -y wget
RUN yum install -y gcc python27-devel openssl openssl-devel
RUN yum install -y flex bison perl

RUN pwd
RUN ls -la

WORKDIR /build
RUN wget https://ftp.postgresql.org/pub/source/v9.4.3/postgresql-9.4.3.tar.gz
RUN wget http://initd.org/psycopg/tarballs/PSYCOPG-2-6/psycopg2-2.6.1.tar.gz
RUN tar xvf postgresql-9.4.3.tar.gz
RUN tar xvf psycopg2-2.6.1.tar.gz

WORKDIR /build/postgresql-9.4.3
RUN ./configure --prefix /build/postgresql-9.4.3/src --with-openssl --without-readline --without-zlib --prefix /usr/local/pgsql-9.4.3
RUN make
RUN make install

WORKDIR /build/psycopg2-2.6.1
ADD setup.cfg /build/psycopg2-2.6.1
RUN  python setup.py build

WORKDIR /build
ADD src/lambda_function.py /build
RUN cp -r psycopg2-2.6.1/build/lib.linux-x86_64-2.7/psycopg2 .
RUN zip -r redshift_password_rotation.zip lambda_function.py
RUN zip -r redshift_password_rotation.zip psycopg2
