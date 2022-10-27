FROM openknowledge/ckan-base:2.9

MAINTAINER Open Knowledge International <info@okfn.org>

RUN apk add tzdata

# Install utilities
RUN pip install ipdb ipdbplugin

# Install any extensions needed by your CKAN instance
# (Make sure to add the plugins to CKAN__PLUGINS in the .env file)
# TODO: pin when possible
RUN echo 'Installing extensions' && \
    # scheming
    pip install -e git+https://github.com/ckan/ckanext-scheming.git#egg=ckanext-scheming && \
    # harvest
    pip install -e git+https://github.com/ckan/ckanext-harvest.git@v1.4.0#egg=ckanext-harvest && \
    pip install -r https://raw.githubusercontent.com/ckan/ckanext-harvest/v1.1.4/pip-requirements.txt && \
    # socrata harvester
    pip install -e git+https://github.com/okfn/ckanext-socrata.git@2.0.4a#egg=ckanext-socrata && \
    pip install -r https://raw.githubusercontent.com/okfn/ckanext-socrata/2.0.4a/requirements.txt && \
    # dcat harvester
    pip install -e git+https://github.com/ckan/ckanext-dcat.git@9d41e27b#egg=ckanext-dcat && \
    pip install -r https://raw.githubusercontent.com/ckan/ckanext-dcat/v0.0.8/requirements.txt && \
    # googleanalytics
    pip install -e git+https://github.com/ckan/ckanext-googleanalytics.git#egg=ckanext-googleanalytics && \
    pip install -r https://raw.githubusercontent.com/ckan/ckanext-googleanalytics/master/requirements.txt && \
    # disqus
    pip install -e git+https://github.com/okfn/ckanext-disqus#egg=disqus && \
    # hierarchy
    pip install -e git+https://github.com/okfn/ckanext-hierarchy.git#egg=ckanext-hierarchy && \
    # showcase
    pip install -e git+https://github.com/okfn/ckanext-showcase.git#egg=ckanext-showcase && \
    # geoview
    pip install -e git+https://github.com/ckan/ckanext-geoview.git@v0.0.20#egg=ckanext-geoview && \
    # pdfview
    pip install -e git+https://github.com/okfn/ckanext-pdfview.git#egg=ckanext-pdfview  && \
    # contact
    pip install -e git+https://github.com/okfn/ckanext-contact.git@lacounts-0.1#egg=ckanext-contact


COPY . /srv/app/src/ckanext-hack4laatd

RUN apk add bind-tools
RUN dig pypi.org

# Install project extension
RUN pip install -e /srv/app/src/ckanext-hack4laatd && \
    pip install -r /srv/app/src/ckanext-lacounts/requirements.txt && \
    python3 -m textblob.download_corpora && \
    cp -r /root/nltk_data $APP_DIR

# Apply patches
COPY install/patches ${APP_DIR}/patches
RUN for d in $APP_DIR/patches/*; do \
        for f in `ls $d/*.patch | sort -g`; do \
		    cd $SRC_DIR/`basename "$d"` && echo "$0: Applying patch $f to $SRC_DIR/`basename $d`"; patch -p1 < "$f" ; \
        done ; \
    done

# Copy config files
COPY install/crontabs/* /etc/crontabs/
COPY install/docker-entrypoint.d/* /docker-entrypoint.d/
COPY install/supervisor.d/* /etc/supervisord.d/
