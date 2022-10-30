import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
from routes.mapper import SubMapper

from ckanext.hack4laatd import helpers, validators, jobs
from ckanext.hack4laatd import helpers, validators, jobs
from ckanext.hack4laatd.logic import actions, auth
import ckan.plugins as p
from flask import Blueprint


def hello_plugin():
    u'''A simple view function'''
    return u'Hello World, this is served from accessthedata extension'

#actions
def faqs():
    return toolkit.render('static/faqs.html')

def aboutus():
    return toolkit.render('static/about.html')

def termsofservice():
    return toolkit.render('static/termsofservice.html')

def privacypolicy():
    return toolkit.render('static/privacypolicy.html')

def resources():
    return toolkit.render('static/resources.html')


class Hack4LaatdPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)
    p.implements(p.IBlueprint)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IGroupController, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IValidators)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'hack4laatd')
        toolkit.add_resource('assets', 'hack4laatd_theme')
    
    def update_config_schema(self, schema):
        schema.update({
            'ckanext.hack4laatd.trending_min': [
                toolkit.get_validator('ignore_missing'),
            ],
            'ckanext.hack4laatd.editable_regions': [
                toolkit.get_validator('ignore_missing'),
                validators.validate_editable_regions,
            ],
            'ckanext.hack4laatd.featured_image': [
                toolkit.get_validator('ignore_missing'),
            ],
        })

        return schema
    
     # ITemplateHelpers

    def get_helpers(self):
        return {
            'get_image_for_group': helpers.get_image_for_group,
            'get_groups_for_form': helpers.get_groups_for_form,
            'get_groups_for_form_using_id': helpers.get_groups_for_form_using_id,
            'get_related_datasets_for_form': helpers.get_related_datasets_for_form,
            'get_related_stories_for_form': helpers.get_related_stories_for_form,
            'get_related_datasets_for_display': helpers.get_related_datasets_for_display,
            'get_related_stories_for_display': helpers.get_related_stories_for_display,
            'get_metadata_completion_rate': helpers.get_metadata_completion_rate,
            'get_recent_data_stories': helpers.get_recent_data_stories,
            'get_featured_data_stories': helpers.get_featured_data_stories,
            'get_featured_datasets': helpers.get_featured_datasets,
            'get_featured_image_url': helpers.get_featured_image_url,
            'get_editable_region': helpers.get_editable_region,
            'get_package_stories': helpers.get_package_stories,
            'get_topics': helpers.get_topics,
            'update_url_query': helpers.update_url_query,
            'get_spatial_value': helpers.get_spatial_value,
            'get_temporal_value': helpers.get_temporal_value,
            'get_story_related_stories': helpers.get_story_related_stories,
            'get_homepage_counts': helpers.get_homepage_counts,
            'sort_facet_items': helpers.sort_facet_items,
            'get_publisher_type': helpers.get_publisher_type,
            'get_organization_display_title': helpers.get_organization_display_title,
            'get_resources_ordered': helpers.get_resources_ordered,
            'get_minimum_views_for_trending': helpers.get_minimum_views_for_trending,
            'get_frequency_period': helpers.get_frequency_period,
            'get_publisher_types': helpers.get_publisher_types,
            'expand_topic_package_count': helpers.expand_topic_package_count,
            'get_author_initials': helpers.get_author_initials,
            'get_gravatar_image_url': helpers.get_gravatar_image_url,
            'list_to_newlines': helpers.list_to_newlines,
            'get_bubble_rows': helpers.get_bubble_rows,
            'get_query_param': helpers.get_query_param,
            'format_iso_date_string': helpers.format_iso_date_string,
            'get_all_working_groups': helpers.get_all_working_groups,
        }

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
            ('/privacy', 'privacy', privacypolicy),
            ('/terms', 'termsofservice', termsofservice),
            ('/faqs', 'faqs', faqs),
            ('/about', 'aboutus', aboutus),
            ('/resources', 'resources', resources)
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)

        return [blueprint]

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        facets_dict.clear()
        facets_dict['type_label'] = _('Type')
        facets_dict['story_type'] = _('Story Type')
        facets_dict['groups'] = _('Topic')
        facets_dict['organization'] = _('Publisher')
        facets_dict['res_format'] = _('Format')

        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        facets_dict.clear()
        facets_dict['type_label'] = _('Type')
        facets_dict['organization'] = _('Publisher')
        facets_dict['res_format'] = _('Format')

        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        facets_dict.clear()
        facets_dict['type_label'] = _('Type')
        facets_dict['groups'] = _('Topic')
        facets_dict['res_format'] = _('Format')

        return facets_dict

    # IPackageController

    def before_index(self, pkg_dict):
        TYPE_LABELS = {'dataset': _('Data'), 'showcase': _('Story')}
        if pkg_dict['type'] in TYPE_LABELS:
            pkg_dict['type_label'] = TYPE_LABELS[pkg_dict['type']]
        return pkg_dict

    # IGroupController

    def create(self, entity):
        if getattr(entity, 'type') == 'topic' and not getattr(toolkit.c, 'job', False):
            toolkit.enqueue_job(jobs.update_groups_for_all_datasets, [])

    def edit(self, entity):
        if getattr(entity, 'type') == 'topic' and not getattr(toolkit.c, 'job', False):
            toolkit.enqueue_job(jobs.update_groups_for_all_datasets, [])

    # IActions

    def get_actions(self):
        return {
            'config_option_update': actions.config_option_update,
            'event_create': actions.event_create,
            'event_update': actions.event_update,
            'event_delete': actions.event_delete,
            'event_show': actions.event_show,
            'event_list': actions.event_list,
            'volunteering_create': actions.volunteering_create,
            'volunteering_update': actions.volunteering_update,
            'volunteering_delete': actions.volunteering_delete,
            'volunteering_show': actions.volunteering_show,
            'volunteering_list': actions.volunteering_list,
            'publishers_list': actions.publishers_list,
            'package_create': actions.package_create,
            'package_update': actions.package_update,
        }

    # IAuthFunctions

    def get_auth_functions(self):
        return {
            'ckanext_hack4laatd_event_create': auth.event_create,
            'ckanext_hack4laatd_event_delete': auth.event_delete,
            'ckanext_hack4laatd_event_show': auth.event_show,
            'ckanext_hack4laatd_volunteering_create': auth.volunteering_create,
            'ckanext_hack4laatd_volunteering_delete': auth.volunteering_delete,
            'ckanext_hack4laatd_volunteering_show': auth.volunteering_show,
            'ckanext_hack4laatd_publishers_show': auth.publishers_show
        }

    # IValidators

    def get_validators(self):
        return {
            'set_default_publisher_title':
                validators.set_default_publisher_title,
            'convert_to_list': validators.convert_to_list,
            'convert_from_list': validators.convert_from_list,
        }


