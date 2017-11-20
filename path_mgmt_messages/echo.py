'''
Created on 20 Nov 2017

@author: lia
'''
from gtp_v2_base.gtp_v2_msg_base import GTPV2MessageBase
from gtp_v2_base.gtp_v2_commons import GTPmessageTypeDigit
from gtp_v2_base.gtp_v2_information_element_base import Recovery

class EchoRequest(GTPV2MessageBase):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, GTPmessageTypeDigit['echo-request'])
        self.add_ie(Recovery(rc = 13))
        
class EchoResponse(GTPV2MessageBase):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, GTPmessageTypeDigit['echo-request']) 
        self.add_ie(Recovery(rc = 0))         