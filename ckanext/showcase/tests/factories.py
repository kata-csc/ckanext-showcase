import factory
import ckan.model
import ckan.tests.helpers as helpers
from ckanext.showcase.logic.schema import showcase_create_schema 

def _get_action_user_name(kwargs):
    '''Return the name of the user in kwargs, defaulting to the site user

    It can be overriden by explictly setting {'user': None} in the keyword
    arguments. In that case, this method will return None.
    '''

    if 'user' in kwargs:
        user = kwargs['user']
    else:
        user = helpers.call_action('get_site_user')

    if user is None:
        user_name = None
    else:
        user_name = user['name']

    return user_name

class Dataset(factory.Factory):
    '''A factory class for creating CKAN datasets.'''

    FACTORY_FOR = ckan.model.Package

    # These are the default params that will be used to create new groups.
    title = 'Test Dataset'
    notes = 'Just another test dataset.'

    # Generate a different group name param for each user that gets created.
    name = factory.Sequence(lambda n: 'test_dataset_{n}'.format(n=n))

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."

        schema = showcase_create_schema()
        if kwargs.get('id'):
            schema['id'] = []

        context = {'user': _get_action_user_name(kwargs), 'schema':  schema}

        dataset_dict = helpers.call_action('package_create',
                                           context=context,
                                           **kwargs)
        return dataset_dict