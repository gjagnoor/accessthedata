import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
from routes.mapper import SubMapper

from ckanext.hack4laatd import helpers, validators, jobs
from ckanext.hack4laatd import helpers, validators, jobs
from ckanext.hack4laatd.logic import actions, auth
from flask import Blueprint

import logging
from ckan import model
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.logic as logic

from ckanext.hack4laatd.admin import create_topics_csv

log = logging.getLogger(__name__)
_ = toolkit._

tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params

def redirect_url(url):
    return toolkit.redirect_to(url)

def hello_plugin():
    u'''A simple view function'''
    return u'Hello World, this is served from accessthedata extension'

#actions
def home():
    return toolkit.render('home/index.html') or redirect_url('/dataset')

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

def search():
    posts = []
    context = {'model': model}
    showcases = toolkit.get_action('ckanext_showcase_list')(context, {})
    for showcase in showcases:
        showcase = \
            toolkit.get_action('package_show')(context,
                                                {'id': showcase['id']})
        if showcase.get('story_type') == 'Blog Post':
            posts.append(showcase)
    return toolkit.render(_search_template('blog'),
                            extra_vars={'posts': posts})

def _search_template(package_type):
    return 'blog/search.html'

def _read_template():
    return 'blog/read.html'

# def index():
#     toolkit.c.events = toolkit.get_action('event_list')(data_dict={})
#     volunteering = \
#         toolkit.get_action('volunteering_list')(data_dict={})
#     toolkit.c.volunteering = [v for v in volunteering
#                                 if not v['is_filled']]
#     return toolkit.render('getinvolved/getinvolved.html')

# def manage_get_involved():
#     '''
#     A ckan-admin page to list and add Get Involved events and volunteering
#     opportunity.
#     '''
#     context = {'model': model, 'session': model.Session,
#                 'user': toolkit.c.user or toolkit.c.author}

#     try:
#         toolkit.check_access('sysadmin', context, {})
#     except toolkit.NotAuthorized:
#         toolkit.abort(401, _('User not authorized to view page'))

#     toolkit.c.events = toolkit.get_action('event_list')(data_dict={})
#     toolkit.c.volunteering = \
#         toolkit.get_action('volunteering_list')(data_dict={})

#     return toolkit.render('getinvolved/manage_get_involved.html')

# # Events

# def remove_event():
#     '''
#     Remove an event.
#     '''
#     context = {'model': model, 'session': model.Session,
#                 'user': toolkit.c.user or toolkit.c.author}

#     try:
#         toolkit.check_access('sysadmin', context, {})
#     except toolkit.NotAuthorized:
#         toolkit.abort(401, _('User not authorized to view page'))

#     if 'cancel' in toolkit.request.params:
#         return toolkit.redirect_to(manage_get_involved)

#     event_id = toolkit.request.params['id']
#     if toolkit.request.method == 'POST' and event_id:
#         try:
#             toolkit.get_action('event_delete')(
#                                 data_dict={'id': event_id})
#         except toolkit.NotAuthorized:
#             toolkit.abort(401, _('Unauthorized to perform that action'))
#         except toolkit.ObjectNotFound:
#             toolkit.h.flash_error(_('The event was not found.'))
#         else:
#             toolkit.h.flash_success(_('The event has been removed.'))
#     elif not event_id:
#         toolkit.h.flash_error(_('The event was not found.'))

#     return toolkit.redirect_to(manage_get_involved)

# def new_event(data=None, errors=None, error_summary=None):

#     context = {'model': model, 'session': model.Session,
#                 'user': toolkit.c.user}
#     try:
#         toolkit.check_access('sysadmin', context)
#     except toolkit.NotAuthorized:
#         toolkit.abort(401, _('User not authorized to create event'))

#     if toolkit.request.method == 'POST' and not data:
#         return _save_event(context)

#     data = data or {}
#     errors = errors or {}
#     error_summary = error_summary or {}
#     vars = {'data': data, 'errors': errors,
#             'error_summary': error_summary}

#     return toolkit.render("getinvolved/event_form.html",
#                             extra_vars=vars)

# def edit_event( data=None, errors=None, error_summary=None):

#     context = {'model': model, 'session': model.Session,
#                 'user': toolkit.c.user}
#     data_dict = {'id': toolkit.request.params['id']}

#     try:
#         toolkit.check_access('sysadmin', context)
#     except toolkit.NotAuthorized:
#         toolkit.abort(403, _('Not authorized to edit event'))

#     if toolkit.request.method == 'POST' and not data:
#         return _save_event(context, 'update')

#     try:
#         old_data = toolkit.get_action('event_show')(context, data_dict)
#         data = data or old_data
#     except (toolkit.ObjectNotFound, toolkit.NotAuthorized):
#         toolkit.abort(404, _('Event not found'))

#     errors = errors or {}
#     vars = {'data': data, 'errors': errors, 'form_style': 'edit',
#             'error_summary': error_summary, 'action': 'edit'}

#     return toolkit.render("getinvolved/event_form.html",
#                             extra_vars=vars)

# def _save_event( context, type="create"):
#     try:
#         data_dict = clean_dict(dict_fns.unflatten(
#             tuplize_dict(parse_params(toolkit.request.params))))

#         # If only one topic, it is a string, so make it a list.
#         if not isinstance(data_dict.get('topic_tags', []), list):
#             data_dict['topic_tags'] = [data_dict['topic_tags'], ]
#         elif data_dict.get('topic_tags') is None:
#             data_dict['topic_tags'] = []

#         context['message'] = data_dict.get('log_message', '')

#         if type == 'create':
#             toolkit.get_action('event_create')(context, data_dict)
#             toolkit.h.flash_success(_('The event has been created.'))
#         elif type == 'update':
#             toolkit.get_action('event_update')(context, data_dict)
#             toolkit.h.flash_success(_('The event has been updated.'))
#     except (toolkit.ObjectNotFound, toolkit.NotAuthorized) as e:
#         toolkit.abort(404, _('Event not found'))
#     except toolkit.ValidationError as e:
#         errors = e.error_dict
#         error_summary = e.error_summary
#         if type == 'create':
#             return new_event(data_dict, errors, error_summary)
#         elif type == 'update':
#             return edit_event(data_dict, errors, error_summary)

#     return toolkit.redirect_to(manage_get_involved)

# # Volunteering Opportunites

# def remove_volunteering(self):
#     '''
#     Remove an volunteering.
#     '''
#     context = {'model': model, 'session': model.Session,
#                 'user': toolkit.c.user or toolkit.c.author}

#     try:
#         toolkit.check_access('sysadmin', context, {})
#     except toolkit.NotAuthorized:
#         toolkit.abort(401, _('User not authorized to view page'))

#     if 'cancel' in toolkit.request.params:
#         return toolkit.redirect_to(manage_get_involved)

#     volunteering_id = toolkit.request.params['id']
#     if toolkit.request.method == 'POST' and volunteering_id:
#         try:
#             toolkit.get_action('volunteering_delete')(
#                                 data_dict={'id': volunteering_id})
#         except toolkit.NotAuthorized:
#             toolkit.abort(401, _('Unauthorized to perform that action'))
#         except toolkit.ObjectNotFound:
#             toolkit.h.flash_error(
#                 _('The volunteering opportunity was not found.'))
#         else:
#             toolkit.h.flash_success(
#                 _('The volunteering opportunity has been removed.'))
#     elif not volunteering_id:
#         toolkit.h.flash_error(
#             _('The volunteering opportunity was not found.'))

#     return toolkit.redirect_to(manage_get_involved)

# def new_volunteering( data=None, errors=None, error_summary=None):

#     context = {'model': model, 'session': model.Session,
#                 'user': toolkit.c.user}
#     try:
#         toolkit.check_access('sysadmin', context)
#     except toolkit.NotAuthorized:
#         toolkit.abort(
#             401,
#             _('User not authorized to create volunteering opportunity'))

#     if toolkit.request.method == 'POST' and not data:
#         return _save_volunteering(context)

#     data = data or {}
#     errors = errors or {}
#     error_summary = error_summary or {}
#     vars = {'data': data, 'errors': errors,
#             'error_summary': error_summary}

#     return toolkit.render("getinvolved/volunteering_form.html",
#                             extra_vars=vars)

# def edit_volunteering( data=None, errors=None, error_summary=None):
#     context = {'model': model, 'session': model.Session,
#                 'user': toolkit.c.user}
#     data_dict = {'id': toolkit.request.params['id']}

#     try:
#         toolkit.check_access('sysadmin', context)
#     except toolkit.NotAuthorized:
#         toolkit.abort(
#             403, _('Not authorized to edit volunteering opportunity'))

#     if toolkit.request.method == 'POST' and not data:
#         return _save_volunteering(context, 'update')

#     try:
#         old_data = toolkit.get_action('volunteering_show')(context,
#                                                             data_dict)
#         data = data or old_data
#     except (toolkit.ObjectNotFound, toolkit.NotAuthorized):
#         toolkit.abort(404, _('Event not found'))

#     errors = errors or {}
#     vars = {'data': data, 'errors': errors, 'form_style': 'edit',
#             'error_summary': error_summary, 'action': 'edit'}

#     return toolkit.render("getinvolved/volunteering_form.html",
#                             extra_vars=vars)

# def _save_volunteering( context, type="create"):
#     try:
#         data_dict = clean_dict(dict_fns.unflatten(
#             tuplize_dict(parse_params(toolkit.request.params))))

#         # If only one topic, it is a string, so make it a list.
#         if not isinstance(data_dict.get('topic_tags', []), list):
#             data_dict['topic_tags'] = [data_dict['topic_tags'], ]
#         elif data_dict.get('topic_tags') is None:
#             data_dict['topic_tags'] = []

#         context['message'] = data_dict.get('log_message', '')

#         if type == 'create':
#             toolkit.get_action('volunteering_create')(context, data_dict)
#             toolkit.h.flash_success(
#                 _('The volunteering opportunity has been created.'))
#         elif type == 'update':
#             toolkit.get_action('volunteering_update')(context, data_dict)
#             toolkit.h.flash_success(
#                 _('The volunteering opportunity has been updated.'))
#     except (toolkit.ObjectNotFound, toolkit.NotAuthorized) as e:
#         toolkit.abort(404, _('Volunteering Opportunity not found'))
#     except toolkit.ValidationError as e:
#         errors = e.error_dict
#         error_summary = e.error_summary
#         if type == 'create':
#             return new_volunteering(data_dict, errors, error_summary)
#         elif type == 'update':
#             return edit_volunteering(data_dict, errors, error_summary)

#     return toolkit.redirect_to(manage_get_involved)

# def download_terms_sources_csv():

#     context = {'model': model, 'session': model.Session,
#                 'user': toolkit.c.user or toolkit.c.author}

#     try:
#         toolkit.check_access('sysadmin', context, {})
#     except toolkit.NotAuthorized:
#         toolkit.abort(401, _('User not authorized to access this resource'))

#     output_csv = create_topics_csv()

#     toolkit.response.headers['Content-type'] = 'text/csv'
#     toolkit.response.headers['Content-disposition'] = 'attachment;filename=topic_terms_sources.csv'

#     return output_csv

class Hack4LaatdPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IGroupController, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IValidators)

    # IConfigurer

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('assets', 'accessthedata')
    
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
            ('/dataset', 'dataset', hello_plugin),
            ('/privacy', 'privacy', privacypolicy),
            ('/terms', 'termsofservice', termsofservice),
            ('/faqs', 'faqs', faqs),
            ('/about', 'about', aboutus),
            ('/resources', 'resources', resources),
            ('/blog', 'blog_search', search),
            ('/blog/{id}', 'blog_read', _read_template),
            # ('/getinvolved', 'getinvolved', index),
            # ('/ckan-admin/get_involved_admin', 'getinvolved_admin', manage_get_involved),
            # ('/ckan-admin/getinvolved_remove_event','getinvolved_event_remove',remove_event),
            # ('/ckan-admin/getinvolved_new_event', 'getinvolved_new_event', new_event),
            # ('/ckan-admin/getinvolved_edit_event', 'getinvolved_edit_event', edit_event),
            # ('/ckan-admin/getinvolved_remove_volunteering', 'getinvolved_volunteering_remove', remove_volunteering),
            # ('/ckan-admin/getinvolved_new_volunteering','getinvolved_new_volunteering',new_volunteering),
            # ('/ckan-admin/getinvolved_edit_volunteering', 'getinvolved_edit_volunteering', edit_volunteering),
            # ('/ckan-admin/terms-sources-csv', 'download_terms_sources_csv', download_terms_sources_csv),
            # ('/catalog/{id}','redirect_catalog', redirect_url, '/dataset')
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


