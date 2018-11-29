from algosec.api_clients.base import SoapAPIClient, RESTAPIClient
from algosec.api_clients.business_flow import BusinessFlowAPIClient
from algosec.api_clients.fire_flow import FireFlowAPIClient
from algosec.api_clients.firewall_analyzer import FirewallAnalyzerAPIClient


def str2bool(s):
    return s.lower() in ("yes", "true", "t", "1")


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
            self._server_ip = options['server']
            self._username = options['username']
            self._password = options['password']
        except KeyError:
            raise Exception("Error while trying to get required configuration settings")

        if 'ssl_enabled' not in options:
            self._ssl_enabled = True
        else:
            self._ssl_enabled = str2bool(options['ssl_enabled'])

    def _set_and_return_a_client(self, client_cache_name):
        """
        Create the requested AlgoSec client if it was not initiated yet, and return it

        :return: Logged in API client to the requested AlgoSec service
        """
        current_client_instance = getattr(self, client_cache_name, None)
        if current_client_instance is not None:
            return current_client_instance

        try:
            client_class = self.ATTRIBUTE_TO_CLIENT_CLASS[client_cache_name]
        except KeyError:
            raise Exception('Unable to create AlgoSec client named "{}"'.format(client_cache_name))

        client_instance = client_class(self._server_ip, self._username, self._password, self._ssl_enabled)

        try:
            # Trigger a session creation, thus any exceptions and login errors would be raised here.
            if isinstance(client_instance, SoapAPIClient):
                client_instance.client
            elif isinstance(client_instance, RESTAPIClient):
                client_instance.session
            else:
                raise Exception("Unrecognized AlgoSec API Instance. Its session initation attribute is unknown.")
        except Exception:
            raise Exception("Error while initiating the API connection to AlgoSec")

        # Cache the newly created instance
        setattr(self, client_cache_name, client_instance)
        return client_instance

    def business_flow(self):
        """
        :rtype: BusinessFlowAPIClient
        """
        return self._set_and_return_a_client('_business_flow')

    def fire_flow(self):
        """
        :rtype: FireFlowAPIClient
        """
        return self._set_and_return_a_client('_fire_flow')

    def firewall_analyzer(self):
        """
        :rtype: FirewallAnalyzerAPIClient
        """
        return self._set_and_return_a_client('_firewall_analyzer')
