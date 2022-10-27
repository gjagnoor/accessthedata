git clone docker-ckan uniquefoldername
create .env file from example
create makefile - copy over from test
make sure docker containers are stopped
run make develop
check if default template is being served without trouble
create extension with make create
add extension to .env plugins
change owner of the src directory so docker can run the setup.py command [don't run the python3 setup.py command. Docker will manage that itself]
make dev again - `sudo chown -R <username here>: src/ckanext-hack4laatd`
make changes in the extension directory. They should appear without your having to restart any containers
