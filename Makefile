dev: 
	- docker-compose -f docker-compose.dev.yml up --build -d
create: 
	- docker-compose -f docker-compose.dev.yml exec ckan-dev /bin/bash -c "ckan generate extension --output-dir /srv/app/src_extensions"

loadplugin:
	- cd src/ckanext-hack4laatd && sudo python3 setup.py develop