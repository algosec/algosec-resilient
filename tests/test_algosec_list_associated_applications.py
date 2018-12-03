import pytest
from mock import patch

from algosec_resilient.components.algosec_list_associated_applications import AlgoSecListAssociatedApplications
from tests.conftest import run_resilient_function


class TestAlgoSecListAssociatedApplications(object):

    @pytest.fixture
    def additional_options(self):
        return {}

    @pytest.fixture
    def tested_class(self):
        return AlgoSecListAssociatedApplications

    @patch(
        'algosec_resilient.components.algosec_client.BusinessFlowAPIClient.get_associated_applications'
    )
    def test_algosec_check_host_internet_connectivity(
            self,
            mock_get_associated_applications,
            tested_function,
    ):
        mock_get_associated_applications.return_value = [
            {'name': 'app1', 'revisionID': 1, 'labels': [{'name': 'Critical'}]},
            {'name': 'app2', 'revisionID': 2},
        ]

        ip = '10.0.0.1'
        result = run_resilient_function(tested_function, ip)

        mock_get_associated_applications.assert_called_once_with(ip)

        assert result == {
            'success': True,
            'entries': [
                {
                    'artifact_ip': ip,
                    'application_name': 'app1',
                    'is_critical': True,
                    'businessflow_dashboard': 'https://algosec.server.net/BusinessFlow/#!application/1/dashboard',
                },
                {
                    'artifact_ip': ip,
                    'application_name': 'app2',
                    'is_critical': False,
                    'businessflow_dashboard': 'https://algosec.server.net/BusinessFlow/#!application/2/dashboard',
                },
            ]
        }
