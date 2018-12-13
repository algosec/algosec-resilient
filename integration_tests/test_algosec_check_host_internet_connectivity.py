# -*- coding: utf-8 -*-
"""Tests using pytest_resilient_circuits"""

from __future__ import print_function

import re

import pytest
from resilient_circuits.util import get_config_data, get_function_definition
from resilient_circuits import SubmitTestFunction, FunctionResult

PACKAGE_NAME = 'algosec_resilient'
FUNCTION_NAME = 'algosec_check_host_internet_connectivity'

# Read the default configuration-data section from the package
config_data = get_config_data(PACKAGE_NAME)


def call_algosec_check_host_internet_connectivity_function(circuits, function_params, timeout=15):
    # Fire a message to the function
    evt = SubmitTestFunction('algosec_check_host_internet_connectivity', function_params)
    circuits.manager.fire(evt)
    event = circuits.watcher.wait('algosec_check_host_internet_connectivity_result', parent=evt, timeout=timeout)
    assert event
    assert isinstance(event.kwargs['result'], FunctionResult)
    pytest.wait_for(event, 'complete', True)
    return event.kwargs['result'].value


class TestAlgosecCheckHostInternetConnectivity(object):
    """ Tests for the algosec_check_host_internet_connectivity function"""

    def test_function_definition(self):
        """ Test that the package provides customization_data that defines the function """
        func = get_function_definition(PACKAGE_NAME, FUNCTION_NAME)
        assert func is not None

    def test_success(self, mock_circuits_app_if_needed, circuits_app, resilient_app_config):
        """ Test calling with sample values for the parameters """
        ip = '10.0.0.10'

        function_params = {'algosec_hostname': ip}

        connectivity_result = call_algosec_check_host_internet_connectivity_function(circuits_app, function_params)
        assert connectivity_result['success'] is True
        assert connectivity_result['artifact_ip'] == ip
        assert connectivity_result['is_it_connected_to_the_internet'] in ('Yes', 'Not Routed', 'No')
        # Should be something like 'https://local.algosec/fa/query/results/#/work/ALL_FIREWALLS_query-1543622562206/'
        assert re.match(
            r'<a href="https://.+?/query/results/#/work/ALL_FIREWALLS_query-\d+/">Query Results</a>',
            connectivity_result['query_url']
        )
