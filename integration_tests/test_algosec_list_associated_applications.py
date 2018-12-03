# -*- coding: utf-8 -*-
"""Tests using pytest_resilient_circuits"""

from __future__ import print_function

import logging
import re

import pytest
from resilient_circuits.util import get_config_data, get_function_definition
from resilient_circuits import SubmitTestFunction, FunctionResult

PACKAGE_NAME = 'algosec_resilient'
FUNCTION_NAME = 'algosec_list_associated_applications'

# Read the default configuration-data section from the package
config_data = get_config_data(PACKAGE_NAME)


logger = logging.getLogger(__name__)


def call_algosec_list_associated_applications_function(circuits, function_params, timeout=10):
    # Fire a message to the function
    evt = SubmitTestFunction('algosec_list_associated_applications', function_params)
    circuits.manager.fire(evt)
    event = circuits.watcher.wait('algosec_list_associated_applications_result', parent=evt, timeout=timeout)
    assert event
    assert isinstance(event.kwargs['result'], FunctionResult)
    pytest.wait_for(event, 'complete', True)
    return event.kwargs['result'].value


class TestAlgosecListAssociatedApplications(object):
    """ Tests for the algosec_list_associated_applications function"""

    def test_function_definition(self):
        """ Test that the package provides customization_data that defines the function """
        func = get_function_definition(PACKAGE_NAME, FUNCTION_NAME)
        assert func is not None

    def test_success(self, mock_circuits_app_if_needed, circuits_app, resilient_app_config):
        """ Test calling with sample values for the parameters """
        ip = '10.0.0.10'

        function_params = {'algosec_hostname': ip}

        results = call_algosec_list_associated_applications_function(circuits_app, function_params)
        assert results['success'] is True
        assert type(results['entries']) is list

        entries = results['entries']
        application_names = [app['application_name'] for app in entries]
        logger.info('{} Associated applications found: {}'.format(len(application_names), application_names))

        for entry in entries:
            assert entry['artifact_ip'] == ip
            assert type(entry['application_name']) is str
            assert type(entry['is_critical']) is bool
            assert re.match(
                r'https://{}/BusinessFlow/#!application/\d+/dashboard'.format(
                    resilient_app_config.get('algosec', 'server_ip')
                ),
                entry['businessflow_dashboard'],
            )
