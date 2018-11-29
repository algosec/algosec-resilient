#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='algosec_resilient',
    version='1.0.0',
    license='MIT',
    author='AlgoSec',
    author_email='support@algosec.com',
    url='https://www.algosec.com/',
    description="Resilient Circuits Components For The AlgoSec Integration",
    long_description="Resilient Circuits Components For The AlgoSec Integration",
    install_requires=[
        'resilient_circuits>=30.0.0',
        'algosec>=1.1.0',
    ],
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
    ],
    entry_points={
        "resilient.circuits.components": [
            "AlgosecIsolateHostFromNetworkFunctionComponent = "
            "algosec_resilient.components.algosec_isolate_host_from_network:FunctionComponent"
        ],
        "resilient.circuits.configsection": ["gen_config = algosec_resilient.util.config:config_section_data"],
        "resilient.circuits.customize": ["customize = algosec_resilient.util.customize:customization_data"],
        "resilient.circuits.selftest": ["selftest = algosec_resilient.util.selftest:selftest_function"]
    }
)
