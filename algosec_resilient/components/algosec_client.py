import logging

from algosec.api_clients.business_flow import BusinessFlowAPIClient
from algosec.api_clients.fire_flow import FireFlowAPIClient
from algosec.api_clients.firewall_analyzer import FirewallAnalyzerAPIClient


def str2bool(s):
    return s.lower() in ("yes", "true", "t", "1")


logger = logging.getLogger(__name__)


class AlgosecClient(object):
    ATTRIBUTE_TO_CLIENT_CLASS = {
        '_business_flow': BusinessFlowAPIClient,
        '_fire_flow': FireFlowAPIClient,
        '_firewall_analyzer': FirewallAnalyzerAPIClient,
    }

    def __init__(self, options):
        """
        :param options: The AlgoSec configuration options (should include server, username, password and ssl_enabled
        """
        super(AlgosecClient, self).__init__()
        self._options = options

        # Setting placeholders and parsing the needed options
        self._server_ip = None
        self._username = None
        self._password = None
        self._ssl_enabled = None
        self._parse_connection_details(options)

    def _parse_connection_details(self, options):
        try:
            self._server_ip = options['server_ip']
            self._username = options['username']
            self._password = options['password']
        except KeyError:
            raise Exception("Error while trying to get required configuration settings")

        if 'ssl_enabled' not in options:
            self._ssl_enabled = True
        else:
            self._ssl_enabled = str2bool(options['ssl_enabled'])

    def business_flow(self):
        """
        :rtype: BusinessFlowAPIClient
        """
        return BusinessFlowAPIClient(self._server_ip, self._username, self._password, self._ssl_enabled)

    def fire_flow(self):
        """
        :rtype: FireFlowAPIClient
        """
        return FireFlowAPIClient(self._server_ip, self._username, self._password, self._ssl_enabled)

    def firewall_analyzer(self):
        """
        :rtype: FirewallAnalyzerAPIClient
        """
        return FirewallAnalyzerAPIClient(self._server_ip, self._username, self._password, self._ssl_enabled)
