import mock
import pytest
from algosec.models import ChangeRequestAction
from mock import ANY

from algosec_resilient.components.algosec_isolate_host_from_network import AlgoSecIsolateHostFromNetwork
from tests.conftest import run_resilient_function


class TestAlgoSecIsolateHostFromNetwork(object):

    @pytest.fixture
    def additional_options(self):
        return {
            'isolation_request_subject': 'Example Request Subject For {}',
            'isolation_request_requestor': 'Example Requestor',
            'isolation_request_requestor_email': 'resilient@integration.dummy',
            'isolation_request_description': 'Example Change Request Description',
            'isolation_request_template': 'Example Template',
        }

    @pytest.fixture
    def tested_class(self):
        return AlgoSecIsolateHostFromNetwork

    @mock.patch('algosec_resilient.components.algosec_client.FireFlowAPIClient.create_change_request')
    def test_algosec_check_host_internet_connectivity(
            self,
            mock_create_change_request,
            additional_options,
            tested_function,
    ):
        change_request_id = 1234567890
        change_request_url = 'some-change-request-url=1234567890'
        mock_create_change_request.return_value = change_request_url

        ip = '10.0.0.1'

        result = run_resilient_function(tested_function, ip)

        mock_create_change_request.assert_called_once_with(
            subject=additional_options['isolation_request_subject'].format(ip),
            requestor_name=additional_options['isolation_request_requestor'],
            email=additional_options['isolation_request_requestor_email'],
            traffic_lines=ANY,
            description=additional_options['isolation_request_description'],
            template=additional_options.get('isolation_request_template') or None,
        )

        assert result == {
            'id': change_request_id,
            'hostname': ip,
            'url': change_request_url
        }

    @mock.patch('algosec_resilient.components.algosec_client.FireFlowAPIClient.create_change_request')
    def test_algosec_check_host_internet_connectivity__check_traffic_lines(
            self,
            mock_create_change_request,
            additional_options,
            tested_function,
    ):
        ip = '10.0.0.1'

        run_resilient_function(tested_function, ip)

        for traffic_line in mock_create_change_request.call_args[1]['traffic_lines']:
            assert traffic_line.action == ChangeRequestAction.DROP
            assert traffic_line.services == ['*']
            assert (
                    (traffic_line.sources == [ip] and traffic_line.destinations == ['*'])
                    or
                    (traffic_line.sources == ['*'] and traffic_line.destinations == [ip])
            )
