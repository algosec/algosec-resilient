# -*- coding: utf-8 -*-
"""Tests using pytest_resilient_circuits"""

from __future__ import print_function

import pytest
from resilient_circuits import SubmitTestFunction, FunctionResult
from resilient_circuits.util import get_config_data, get_function_definition

PACKAGE_NAME = "algosec_resilient"
FUNCTION_NAME = "algosec_isolate_host_from_network"

# Read the default configuration-data section from the package
config_data = get_config_data(PACKAGE_NAME)


def call_algosec_isolate_host_from_network_function(circuits, function_params, timeout=15):
    # Fire a message to the function
    evt = SubmitTestFunction("algosec_isolate_host_from_network", function_params)
    circuits.manager.fire(evt)
    event = circuits.watcher.wait("algosec_isolate_host_from_network_result", parent=evt, timeout=timeout)
    assert event
    assert isinstance(event.kwargs["result"], FunctionResult)
    pytest.wait_for(event, "complete", True)
    return event.kwargs["result"].value


class TestAlgosecIsolateHostFromNetwork(object):
    """ Tests for the algosec_isolate_host_from_network function"""

    def test_function_definition(self):
        """ Test that the package provides customization_data that defines the function """
        func = get_function_definition(PACKAGE_NAME, FUNCTION_NAME)
        assert func is not None

    def test_success(self, mock_circuits_app_if_needed, circuits_app, resilient_app_config):
        """ Test calling with sample values for the parameters """
        ip = '10.0.0.10'

        function_params = {'algosec_hostname': ip}
        result = call_algosec_isolate_host_from_network_function(circuits_app, function_params)

        assert type(result['id']) is int
        assert result['hostname'] == ip
        assert result['url'] == 'https://{}/FireFlow/Ticket/Display.html?id={}'.format(
            resilient_app_config.get('algosec', 'server_ip'),
            result['id'],
        )
