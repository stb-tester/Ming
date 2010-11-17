import pymongo

from session import Session
from base import Document, Field

# Re-export direction keys
ASCENDING = pymongo.ASCENDING
DESCENDING = pymongo.DESCENDING

def configure(**kwargs):
    """
    Given a dictionary of config values, creates DataStores and saves them by name
    """
    from datastore import DataStore
    from formencode.variabledecode import variable_decode
    from formencode import schema, validators

    class DatastoreSchema(schema.Schema):
        network_timeout=validators.Number(if_missing=None, if_empty=None)
        master=validators.UnicodeString(if_missing=None, if_empty=None)
        slave=validators.UnicodeString(if_missing=None, if_empty=None)
        database=validators.UnicodeString(not_empty=True)

    config = variable_decode(kwargs)
    datastores = {}
    for name, datastore in config['ming'].iteritems():
        args = DatastoreSchema.to_python(datastore)
        datastores[name] = DataStore(**args)
    Session._datastores = datastores
    # bind any existing sessions
    for name, session in Session._registry.iteritems():
        session.bind = datastores.get(name, None)
