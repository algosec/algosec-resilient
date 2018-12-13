# -*- coding: utf-8 -*-
# pragma pylint: disable=unused-argument, no-self-use
"""Function implementation"""

import logging

from resilient_circuits import function, FunctionResult, StatusMessage

from algosec_resilient.components.algosec_base_component import AlgoSecComponent

logger = logging.getLogger(__name__)


class AlgoSecListAssociatedApplications(AlgoSecComponent):
    """Component that implements Resilient function 'algosec_list_associated_applications"""

    @function("algosec_list_associated_applications")
    def _algosec_list_associated_applications_function(self, event, *args, **kwargs):
        """
        Function: Given an IP/Host list all associated BusinessFlow applications.

        Provides better assessment the risk of the incident. The results contain whether or not it's a critical
        application and a url link to the application on the AlgoSec BusinessFlow dashboard.
        """
        return self.run_login(kwargs)

    def _logic(self, algosec_hostname):
        """The @function decorator offerend by resilient circuits is impossible to unit test..."""
        client = self.algosec.business_flow()
        logger.info("algosec_hostname: %s", algosec_hostname)

        # PUT YOUR FUNCTION IMPLEMENTATION CODE HERE
        yield StatusMessage("starting...")

        associated_applications = [
            {
                'artifact_ip': algosec_hostname,
                'application_name': app_json['name'],
                'is_critical': client.is_application_critical(app_json),
                'businessflow_dashboard': '<a href="{}">{}</a>'.format(
                    client.get_abf_application_dashboard_url(app_json['revisionID']),
                    app_json['name']
                ),
            }
            for app_json in client.get_associated_applications(algosec_hostname)
        ]

        results = {
            'success': True,
            'entries': associated_applications
        }
        yield StatusMessage("done...")

        # Produce a FunctionResult with the results
        yield FunctionResult(results)
