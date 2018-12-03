import mock
import pytest
from resilient_circuits import FunctionResult
from resilient_circuits.action_message import FunctionException_


@pytest.fixture
def base_options():
    return {
        'algosec': {
            'server_ip': 'algosec.server.net',
            'username': 'algosec',
            'password': 'admin',
            'ssl_enabled': 'true'
        }
    }


def run_resilient_function(func, *args):
    """
    Run a resilient app function in unit test environment.

    Properly raise exceptions if needed and return the results object.
    :param func:
    :param args:
    :return:
    """
    for message in func(*args):
        if type(message) is FunctionException_:
            raise message
        elif type(message) is FunctionResult:
            return message.value


@pytest.fixture
def options(base_options, additional_options):
    base_options['algosec'].update(additional_options)
    return base_options


@pytest.fixture(scope='session')
def mock_calls_to_resilient_component_class():
    with mock.patch('algosec_resilient.components.algosec_base_component.AlgoSecComponent._call_super'):
        yield


@pytest.fixture
def tested_function(mock_calls_to_resilient_component_class, tested_class, options):
    klass = tested_class(options)
    yield klass._logic
