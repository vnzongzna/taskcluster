# coding=utf-8
#####################################################
# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT EDIT #
#####################################################
# noqa: E128,E201
from .client import BaseClient
from .client import createApiClient
from .client import config
from .client import createTemporaryCredentials
from .client import createSession
_defaultConfig = config


class Pulse(BaseClient):
    """
    The taskcluster-pulse service, typically available at `pulse.taskcluster.net`
    manages pulse credentials for taskcluster users.

    A service to manage Pulse credentials for anything using
    Taskcluster credentials. This allows us self-service and
    greater control within the Taskcluster project.
    """

    classOptions = {
        "baseUrl": "https://pulse.taskcluster.net/v1"
    }

    def overview(self, *args, **kwargs):
        """
        Rabbit Overview

        An overview of the Rabbit cluster

        This method takes output: ``http://schemas.taskcluster.net/pulse/v1/rabbit-overview.json``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["overview"], *args, **kwargs)

    def exchanges(self, *args, **kwargs):
        """
        Rabbit Exchanges

        A list of exchanges in the rabbit cluster

        This method takes output: ``http://schemas.taskcluster.net/pulse/v1/exchanges-response.json``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["exchanges"], *args, **kwargs)

    def createNamespace(self, *args, **kwargs):
        """
        Create a namespace

        Creates a namespace, given the taskcluster credentials with scopes.

        This method takes input: ``http://schemas.taskcluster.net/pulse/v1/namespace-request.json``

        This method takes output: ``http://schemas.taskcluster.net/pulse/v1/namespace-response.json``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["createNamespace"], *args, **kwargs)

    def namespace(self, *args, **kwargs):
        """
        Get namespace information

        Gets a namespace, given the taskcluster credentials with scopes.

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["namespace"], *args, **kwargs)

    def ping(self, *args, **kwargs):
        """
        Ping Server

        Respond without doing anything.
        This endpoint is used to check that the service is up.

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["ping"], *args, **kwargs)

    funcinfo = {
        "exchanges": {           'args': [],
            'method': 'get',
            'name': 'exchanges',
            'output': 'http://schemas.taskcluster.net/pulse/v1/exchanges-response.json',
            'route': '/exchanges',
            'stability': 'experimental'},
        "createNamespace": {           'args': ['namespace'],
            'input': 'http://schemas.taskcluster.net/pulse/v1/namespace-request.json',
            'method': 'post',
            'name': 'createNamespace',
            'output': 'http://schemas.taskcluster.net/pulse/v1/namespace-response.json',
            'route': '/namespace/<namespace>',
            'stability': 'experimental'},
        "overview": {           'args': [],
            'method': 'get',
            'name': 'overview',
            'output': 'http://schemas.taskcluster.net/pulse/v1/rabbit-overview.json',
            'route': '/overview',
            'stability': 'experimental'},
        "namespace": {           'args': ['namespace'],
            'method': 'get',
            'name': 'namespace',
            'route': '/namespace/<namespace>',
            'stability': 'experimental'},
        "ping": {           'args': [],
            'method': 'get',
            'name': 'ping',
            'route': '/ping',
            'stability': 'stable'},
    }


__all__ = ['createTemporaryCredentials', 'config', '_defaultConfig', 'createApiClient', 'createSession', 'Pulse']
