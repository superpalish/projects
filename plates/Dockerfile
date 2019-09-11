FROM python:3.5
ENV LANG C.UTF-8
ENV PYTHONIOENCODING UTF-8

RUN set -ex \
    && apt-get update && apt-get install -y \
	nginx \
	python-psycopg2\
	supervisor \
    python3-lxml \
    python3-pil \
    sed \
    postgresql-client

RUN mkdir -p /plates/deploy/logs
RUN mkdir -p /plates/plates-project/logs
RUN mkdir -p /plates/static
RUN mkdir -p /plates/uploads

WORKDIR /plates

COPY conf/requirements.pip /plates/conf/
RUN pip install -r conf/requirements.pip

COPY scripts/ /plates/scripts/
RUN chmod -R 755 /plates/scripts/

COPY scripts/supervisord.conf /etc/supervisor/conf.d/

COPY . /plates/plates-project/

# nginx settings
RUN rm -f /etc/nginx/sites-enabled/default
COPY conf/nginx-plates.conf /etc/nginx/conf.d/

# change settings file
RUN rm -f /plates/plates-project/settings.py
COPY conf/settings.py /plates/plates-project/plates/

EXPOSE 8000
EXPOSE 80

ENTRYPOINT ["/plates/scripts/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-n"]
