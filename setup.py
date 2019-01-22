#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# Declare the Resilient Function components. Dict from Class name to module name in the components directory.
FUNCTION_COMPONENTS = {
    'AlgoSecIsolateHostFromNetwork': 'algosec_isolate_host_from_network',
    'AlgoSecCheckHostInternetConnectivity': 'algosec_check_host_internet_connectivity',
    'AlgoSecListAssociatedApplications': 'algosec_list_associated_applications',

}

setup(
    name='algosec_resilient',
    version='1.2.0',
    license='MIT',
    author='AlgoSec',
    author_email='support@algosec.com',
    url='https://www.algosec.com/',
    description="Resilient Circuits Components For The AlgoSec Integration",
    long_description="Resilient Circuits Components For The AlgoSec Integration",
    install_requires=[
        'resilient>=31.0.0',
        'resilient_circuits>=31.0.0',
        'algosec>=1.3.0',
    ],
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
    ],
    entry_points={
        "resilient.circuits.components": [
            '{}FunctionComponent = algosec_resilient.components.{}:{}'.format(klass, module, klass)
            for klass, module in FUNCTION_COMPONENTS.items()
        ],
        "resilient.circuits.configsection": ["gen_config = algosec_resilient.util.config:config_section_data"],
        "resilient.circuits.customize": ["customize = algosec_resilient.util.customize:customization_data"],
        "resilient.circuits.selftest": ["selftest = algosec_resilient.util.selftest:selftest_function"]
    }
)
