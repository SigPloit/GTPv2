'''
Created on Mar 9, 2018

@author: rosalia
'''
from gtp_v2_core.commons.gtp_v2_msg_base import GTPV2MessageBase
from gtp_v2_core.commons.gtp_v2_commons import GTPmessageTypeDigit
from gtp_v2_core.commons.gtp_v2_information_element_base import *

class CreateBearerRequest(GTPV2MessageBase):
    '''
    classdocs
    '''


    def __init__(self, teid, ebi = 5, source_ip, interface = 7):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, t = 0x01,
            msg_type = GTPmessageTypeDigit['create-bearer-request'])
        self.set_teid(teid)
        self.add_ie(BearerContext(ip = source_ip, interface = interface))
        self.add_ie(EPSBearerID(ebi = ebi))

class CreateBearerResponse(GTPV2MessageBase):
    '''
    classdocs
    '''
    def __init__(self, teid, sqn, source_ip, interface = 7):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, GTPmessageTypeDigit['create-bearer-response'])
        self.set_teid(teid)
        self.set_sequence_number(sqn)
    