# -*- coding: utf-8 -*-
"""Abstract base class component for all AlgoSec components"""

from resilient_circuits import ResilientComponent, handler

import algosec_resilient.util.selftest as selftest
from algosec_resilient.components.algosec_client import AlgosecClient


class AlgoSecComponent(ResilientComponent):
    """Abstract base class component for all AlgoSec components"""

    def __init__(self, opts):
        """constructor provides access to the configuration options"""
        self._call_super(opts)
        self.options = opts.get("algosec", {})
        selftest.selftest_function(opts)
        self._setup_algosec_client()

    def _call_super(self, opts):
        """
        Allow patching of the super call in unit tests....

        The original ResilientComponent component is super complicated to simply unit test...
        """
        super(AlgoSecComponent, self).__init__(opts)

    def _setup_algosec_client(self):
        self.algosec = AlgosecClient(self.options)

    @handler("reload")
    def _reload(self, event, opts):
        """Configuration options have changed, save new values"""
        self.options = opts.get("algosec", {})
        self._setup_algosec_client()
