from bigbytes_integrations.sources.chargebee.streams.base import BaseChargebeeStream


class CustomersStream(BaseChargebeeStream):
    TABLE = 'customers'
    ENTITY = 'customer'
    REPLICATION_METHOD = 'INCREMENTAL'
    REPLICATION_KEY = 'updated_at'
    KEY_PROPERTIES = ['id']
    BOOKMARK_PROPERTIES = ['updated_at']
    SELECTED_BY_DEFAULT = True
    VALID_REPLICATION_KEYS = ['updated_at']
    INCLUSION = 'available'
    API_METHOD = 'GET'
    SCHEMA = 'common/customers'
    SORT_BY = 'updated_at'

    def get_url(self):
        return 'https://{}.chargebee.com/api/v2/customers'.format(self.config.get('site'))
