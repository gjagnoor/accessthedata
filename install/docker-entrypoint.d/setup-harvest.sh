#!/bin/bash

# Create DB tables if not there
ckan --config=/etc/ckan/default/ckan.ini harvester initdb
