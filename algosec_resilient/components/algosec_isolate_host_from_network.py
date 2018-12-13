# -*- coding: utf-8 -*-
# pragma pylint: disable=unused-argument, no-self-use
"""Function implementation"""

import logging

from algosec.models import ChangeRequestTrafficLine, ChangeRequestAction
from resilient_circuits import function, FunctionResult, StatusMessage

from algosec_resilient.components.algosec_base_component import AlgoSecComponent

logger = logging.getLogger(__name__)


class AlgoSecIsolateHostFromNetwork(AlgoSecComponent):
    """Component that implements Resilient function 'algosec_isolate_host_from_network"""

    @function("algosec_isolate_host_from_network")
    def _algosec_isolate_host_from_network_function(self, event, *args, **kwargs):
        """
        Function: Create a traffic change request with AlgoSec's FireFlow to isolate a host from the network.

        Then AlgoSec's ActiveChange then automatically implements rule changes across all firewalls
        in the network to isolate the host completely.
        """
        return self.run_login(kwargs)

    def _logic(self, algosec_hostname):
        """The @function decorator offerend by resilient circuits is impossible to unit test..."""
        logger.info("algosec_hostname: %s", algosec_hostname)

        # PUT YOUR FUNCTION IMPLEMENTATION CODE HERE
        yield StatusMessage("starting...")
        isolate_traffic_lines = [
            ChangeRequestTrafficLine(
                action=ChangeRequestAction.DROP,
                sources=[algosec_hostname],
                destinations=['*'],
                services=['*'],
            ),
            ChangeRequestTrafficLine(
                action=ChangeRequestAction.DROP,
                sources=['*'],
                destinations=[algosec_hostname],
                services=['*'],
            )
        ]
        try:
            yield StatusMessage("creating isolation change request...")
            change_request_url = self.algosec.fire_flow().create_change_request(
                subject=self.options['isolation_request_subject'].format(algosec_hostname),
                requestor_name=self.options['isolation_request_requestor'],
                email=self.options['isolation_request_requestor_email'],
                traffic_lines=isolate_traffic_lines,
                description=self.options['isolation_request_description'],
                template=self.options.get('isolation_request_template') or None,
            )
        except Exception:
            raise Exception(
                "Error occured while trying to create the isolation change request for {}".format(algosec_hostname)
            )

        yield StatusMessage("done...")

        change_request_id = int(change_request_url.split('=')[1])
        result = {
            'id': change_request_id,
            'hostname': algosec_hostname,
            'url': '<a href="{}">Change Request #{}</a>'.format(change_request_url, change_request_id),
        }

        # Produce a FunctionResult with the result
        yield FunctionResult(result)
