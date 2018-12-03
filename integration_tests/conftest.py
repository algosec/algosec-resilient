import pytest
from six.moves import configparser


@pytest.fixture
def resilient_app_config(request):
    config_path = request.config.option.resilient_app_config
    parser = configparser.ConfigParser()
    parser.read(config_path)
    return parser


def pytest_addoption(parser):
    parser.addoption(
        '--real-resilient-server',
        action='store_true',
        default=False,
        help='Run integration tests against a mock Resilient server rather than using the '
             'Resilient server defined in the app config.',
    )


@pytest.fixture(scope='module')
def mock_circuits_app_if_needed(request):
    """Set the `resilient_mock` module variable if the `--real-resilient-server` was not set."""
    if not request.config.getoption('--real-resilient-server'):
        setattr(request.module, 'resilient_mock', 'pytest_resilient_circuits.BasicResilientMock')
