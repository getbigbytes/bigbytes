from bigbytes_integrations.sources.commercetools.streams.base import BaseStream


class PaymentsStream(BaseStream):
    KEY_PROPERTIES = ['id']

    URL_PATH = '/payments'
