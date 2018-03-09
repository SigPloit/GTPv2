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


    def __init__(self, teid):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, t = 0x01,
            msg_type = GTPmessageTypeDigit['modify-bearer-request'])
        self.set_teid(teid)

class ModifyBearerResponse(GTPV2MessageBase):
    '''
    classdocs
    '''
    def __init__(self, teid, sqn):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, GTPmessageTypeDigit['modify-bearer-response'])
        self.set_teid(teid)
        self.set_sequence_number(sqn)
    