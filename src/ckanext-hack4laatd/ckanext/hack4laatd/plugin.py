import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint

import ckan.plugins as p

def hello_plugin():
    u'''A simple view function'''
    return u'Hello World, this is served from accessthedata extension'


class Hack4LaatdPlugin(plugins.SingletonPlugin):
    p.implements(p.IBlueprint)
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'hack4laatd')
    
    # IBlueprint

    def get_blueprint(self):
        '''Return blueprints to be registered by the app.
        This method can return either a Flask Blueprint object or
        a list of Flask Blueprint objects.
        '''

        # Create Blueprint for plugin
        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = 'templates'
        # Add plugin url rules to Blueprint object
        rules = [
            ('/hello_plugin', 'hello_plugin', hello_plugin),
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)

        # Create a second Blueprint for plugin if needed
        blueprint_2 = Blueprint('blueprint_2', self.__module__)
        return [blueprint, blueprint_2]

