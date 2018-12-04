# -*- coding: utf-8 -*-
# pragma pylint: disable=unused-argument, no-self-use
"""Function implementation"""

import logging

from algosec.models import DeviceAllowanceState
from resilient_circuits import function, StatusMessage, FunctionResult

from algosec_resilient.components.algosec_base_component import AlgoSecComponent

logger = logging.getLogger(__name__)


class AlgoSecCheckHostInternetConnectivity(AlgoSecComponent):
    """Component that implements Resilient function 'algosec_check_host_internet_connectivity"""

    @function("algosec_check_host_internet_connectivity")
    def _algosec_check_host_internet_connectivity_function(self, event, *args, **kwargs):
        """
        Function: Given a hostname, return whether or not it has internet access.

        The AlgoSec integration will check if a given host/IP is has access to a public
        known internet node such as 8.8.8.8.
        """
        self.run_login(kwargs)

    def _logic(self, algosec_hostname):
        """The @function decorator offerend by resilient circuits is impossible to unit test..."""
        logger.info("algosec_hostname: %s", algosec_hostname)

        # PUT YOUR FUNCTION IMPLEMENTATION CODE HERE
        yield StatusMessage("starting...")

        query_dict = self.algosec.firewall_analyzer().execute_traffic_simulation_query(
            algosec_hostname,
            self.options['internet_connectivity_check_external_ip'],
            self.options['internet_connectivity_check_service'],
        )

        query_result, query_url = query_dict['result'], query_dict['query_url']

        if query_result in (DeviceAllowanceState.ALLOWED, DeviceAllowanceState.PARTIALLY_BLOCKED):
            is_it_connected_to_the_internet = 'Yes'
        elif query_result == DeviceAllowanceState.NOT_ROUTED:
            is_it_connected_to_the_internet = 'No'
        else:
            is_it_connected_to_the_internet = 'No'

        connectivity_result = {
            'success': True,
            'artifact_ip': algosec_hostname,
            'is_it_connected_to_the_internet': is_it_connected_to_the_internet,
            'query_url': '<a href="{}">Query Results</a>'.format(query_url),
        }

        yield StatusMessage("done...")

        # Produce a FunctionResult with the results
        yield FunctionResult(connectivity_result)
