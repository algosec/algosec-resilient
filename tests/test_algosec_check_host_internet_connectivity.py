import mock
import pytest
from algosec.models import DeviceAllowanceState

from algosec_resilient.components.algosec_check_host_internet_connectivity import AlgoSecCheckHostInternetConnectivity
from tests.conftest import run_resilient_function


class TestAlgoSecCheckHostInternetConnectivity(object):

    @pytest.fixture
    def additional_options(self):
        return {
            'internet_connectivity_check_external_ip': 'some-ip-that-is-found-in-the-www',
            'internet_connectivity_check_service': 'some-service-like-http',
        }

    @pytest.fixture
    def tested_class(self):
        return AlgoSecCheckHostInternetConnectivity

    @pytest.mark.parametrize('device_allowance,expected_connectivity', [
        (DeviceAllowanceState.PARTIALLY_BLOCKED, 'No'),
        (DeviceAllowanceState.BLOCKED, 'No'),
        (DeviceAllowanceState.ALLOWED, 'Yes'),
        (DeviceAllowanceState.NOT_ROUTED, 'Not Routed'),
    ])
    @mock.patch(
        'algosec_resilient.components.algosec_client.FirewallAnalyzerAPIClient.execute_traffic_simulation_query'
    )
    def test_algosec_check_host_internet_connectivity(
            self,
            mock_execute_traffic_simulation_query,
            device_allowance,
            expected_connectivity,
            additional_options,
            tested_function,
    ):
        query_url = 'some-query-url'
        mock_execute_traffic_simulation_query.return_value = {
            'result': device_allowance,
            'query_url': query_url,
        }

        ip = '10.0.0.1'
        result = run_resilient_function(tested_function, ip)

        mock_execute_traffic_simulation_query.assert_called_once_with(
            ip,
            additional_options['internet_connectivity_check_external_ip'],
            additional_options['internet_connectivity_check_service'],
        )

        assert result == {
            'success': True,
            'artifact_ip': ip,
            'is_it_connected_to_the_internet': expected_connectivity,
            'query_url': query_url
        }
