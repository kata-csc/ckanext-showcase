import ckan.plugins.toolkit as toolkit
import ckan.model as model

from ckanext.showcase.model import ShowcaseAdmin

import logging
log = logging.getLogger(__name__)


def _is_showcase_admin(context):
    '''
    Determines whether user in context is in the showcase admin list.
    '''
    user = context.get('user', '')
    userobj = model.User.get(user)
    return ShowcaseAdmin.is_user_showcase_admin(userobj)

def _is_showcase_owner(context, data_dict):
    '''
    Determines whether user has created the showcase (i.e. is the owner)
    '''

    if not data_dict:
        return False

    user = context.get('user', None)
    userobj = model.User.get(user)
    pkg_id = data_dict.get('id', None) or data_dict.get('showcase_id', '')
    pkg_obj = model.Package.get(pkg_id)

    if not pkg_obj:
        return False

    if pkg_obj.creator_user_id == userobj.id:
        return True

    return False

def create(context, data_dict):
    '''Create a Showcase.

       Any user (who is logged in) can create a showcase
    '''
    return {'success': True}


def delete(context, data_dict):
    '''Delete a Showcase.

       Only showcase owner can delete a showcase.
    '''
    return {'success': _is_showcase_owner(context, data_dict) or _is_showcase_admin(context)}


def update(context, data_dict):
    '''Update a Showcase.

       Only a showcase owner can edit a showcase.
    '''
    return {'success': _is_showcase_owner(context, data_dict) or _is_showcase_admin(context)}


@toolkit.auth_allow_anonymous_access
def show(context, data_dict):
    '''All users can access a showcase show'''
    return {'success': True}


@toolkit.auth_allow_anonymous_access
def list(context, data_dict):
    '''All users can access a showcase list'''
    return {'success': True}


def package_association_create(context, data_dict):
    '''Create a package showcase association.

       Only showcase owner can add packages to the showcase
    '''
    return {'success': _is_showcase_owner(context, data_dict) or _is_showcase_admin(context)}


def package_association_delete(context, data_dict):
    '''Delete a package showcase association.

       Only showcase owner can add packages to the showcase
    '''
    return {'success': _is_showcase_owner(context, data_dict) or _is_showcase_admin(context)}


@toolkit.auth_allow_anonymous_access
def showcase_package_list(context, data_dict):
    '''All users can access a showcase's package list'''
    return {'success': True}


@toolkit.auth_allow_anonymous_access
def package_showcase_list(context, data_dict):
    '''All users can access a packages's showcase list'''
    return {'success': True}


def add_showcase_admin(context, data_dict):
    '''Only sysadmins can add users to showcase admin list.'''
    return {'success': False}


def remove_showcase_admin(context, data_dict):
    '''Only sysadmins can remove users from showcase admin list.'''
    return {'success': False}


def showcase_admin_list(context, data_dict):
    '''Only sysadmins can list showcase admin users.'''
    return {'success': False}
