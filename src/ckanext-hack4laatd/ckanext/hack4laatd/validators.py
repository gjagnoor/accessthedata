import json
import logging
from ckan import model
from ckan.common import config
from ckan.plugins import toolkit
import ckan.lib.uploader as uploader
import ckanext.hack4laatd.helpers as helpers
import ckanext.hack4laatd.harvest.helpers as harvest_helpers
log = logging.getLogger(__name__)


def validate_editable_regions(value):
    # value: the client send us only changed regions as a dict

    # Parse/update/stringify
    try:
        regions = json.loads(value or '{}')
        is_patch = regions.pop('is_patch', False)
        if is_patch:
            old_value = config.get('ckanext.hack4laatd.editable_regions')
            old_regions = json.loads(old_value or '{}')
            regions = dict(list(old_regions.items()) + list(regions.items()))
        value = json.dumps(regions, indent=4)
    except Exception:
        raise toolkit.Invalid('Homepage regions can\'t be parsed/updated/stringified')

    # Validate
    for region_name, region in list(regions.items()):
        # We check if region is set it should contain tags
        if '<' not in region or '>' not in region:
            raise toolkit.Invalid('Homepage region %s is invalid' % region_name)

    return value


def set_default_publisher_title(key, data, errors, context):
    data[('title',)] = data.get(('title',)) or data.get(('display_title',))


def convert_to_list(value, context):
    if not value:
        return None

    if isinstance(value, list):
        value = [v.strip().lower() for v in value]
    else:
        value = [v.strip().lower() for v in value.split('\n')]

    return json.dumps(value)


def convert_from_list(value, context):

    if not value:
        return []
    else:
        if '\n' in value:
            # Legacy format
            return value.split('\n')
        try:
            return json.loads(value)
        except ValueError:
            # Return as single item
            return [value]
