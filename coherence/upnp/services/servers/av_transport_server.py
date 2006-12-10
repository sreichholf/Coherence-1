# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2006, Frank Scholz <coherence@beebits.net>

# AVTransport service

from twisted.python import log
from twisted.web import resource, static, soap
from twisted.internet import defer

from elementtree.ElementTree import Element, SubElement, ElementTree, tostring

from coherence.upnp.core.soap_service import UPnPPublisher

from coherence.upnp.core import service

class AVTransportControl(service.ServiceControl,UPnPPublisher):

    def __init__(self, server):
        self.service = server
        self.variables = server.get_variables()
        self.actions = server.get_actions()


class AVTransportServer(service.Server, resource.Resource):

    def __init__(self, device, backend=None):
        self.device = device
        if backend == None:
            backend = self.device.backend
        resource.Resource.__init__(self)
        service.Server.__init__(self, 'AVTransport', self.device.version, backend)

        self.control = AVTransportControl(self)
        self.putChild(self.scpd_url, service.scpdXML(self, self.control))
        self.putChild(self.control_url, self.control)
        
    def listchilds(self, uri):
        cl = ''
        for c in self.children:
                cl += '<li><a href=%s/%s>%s</a></li>' % (uri,c,c)
        return cl
        
    def render(self,request):
        return '<html><p>root of the AVTransport</p><p><ul>%s</ul></p></html>'% self.listchilds(request.uri)
