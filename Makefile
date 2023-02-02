dev: 
	- docker-compose -f docker-compose.dev.yml up --build -d --remove-orphans

get_involved:
	- docker-compose -f docker-compose.dev.yml run --rm ckan-dev bash -c "cd src_extensions/ckanext-hack4laatd && python3 setup.py develop && paster get_involved init-db -c ../../production.ini"

create: 
	- docker-compose -f docker-compose.dev.yml exec ckan-dev /bin/bash -c "ckan generate extension --output-dir /srv/app/src_extensions"
loadplugin:
	- cd src/ckanext-hack4laatd && sudo python3 setup.py develop