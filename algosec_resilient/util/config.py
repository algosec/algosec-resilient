# -*- coding: utf-8 -*-

"""Generate a default configuration-file section for algosec"""

from __future__ import print_function

from textwrap import dedent


def config_section_data():
    """Produce the default configuration section for app.config,
       when called by `resilient-circuits config [-c|-u]`
    """
    config_data = dedent(
        u"""
        [algosec]
        server_ip=local.algosec.com
        username=admin
        password=algosec
        ssl_enabled=true
        isolation_request_subject=IBM Resilient Isolation Request for {}
        isolation_request_requestor=IBM Resilient
        isolation_request_requestor_email=resilient@integration.dummy
        isolation_request_description=Isolation Request initiated by the IBM Resilient Integration.
        isolation_request_template=

        internet_connectivity_check_external_ip=8.8.8.8
        internet_connectivity_check_service=*
        """
    )
    return config_data
