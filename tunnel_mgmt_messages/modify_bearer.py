'''
Created on Mar 9, 2018

@author: rosalia
'''

from gtp_v2_core.commons.gtp_v2_msg_base import GTPV2MessageBase
from gtp_v2_core.commons.gtp_v2_commons import GTPmessageTypeDigit
from gtp_v2_core.commons.gtp_v2_information_element_base import *

class ModifyBearerRequest(GTPV2MessageBase):
    '''
    classdocs
    '''


    def __init__(self, teid, sqn = 0x00, ebi = 5, source_ip, interface = 7):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, t = 0x01, sequence = sqn, 
            msg_type = GTPmessageTypeDigit['modify-bearer-request'])
        self.set_teid(teid)
        self.add_ie(BearerContext(ip = source_ip, interface = interface))
        self.add_ie(EPSBearerID(ebi = ebi))

class ModifyBearerResponse(GTPV2MessageBase):
    '''
    classdocs
    '''
    def __init__(self, teid, sqn = 0x00, ebi = 5, source_ip, interface = 7):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, t = 0x01, sequence = sqn,
            msg_type = GTPmessageTypeDigit['modify-bearer-response'])
        self.set_teid(teid)
        self.add_ie(BearerContext(ip = source_ip, interface = interface))
        self.add_ie(EPSBearerID(ebi = ebi))
        self.add_ie(SuccessCause())
        self.add_ie(Recovery())