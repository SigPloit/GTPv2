'''
Created on 29 Jan 2018

@author: loay
'''
from gtp_v2_core.commons.gtp_v2_msg_base import GTPV2MessageBase

from gtp_v2_core.commons.gtp_v2_commons import GTPmessageTypeDigit
from gtp_v2_core.commons.gtp_v2_information_element_base import *

class DeleteSessionRequest(GTPV2MessageBase):
    '''
    classdocs
    '''

    def __init__(self, teid, ebi=5, mcc="222",
                 mnc="88", lac=2788, rac=1, tac=0, ecgi=0, sac=0, cgi=0):
        '''
        Constructor
        '''

        GTPV2MessageBase.__init__(self, t=0x01,
            msg_type=GTPmessageTypeDigit['delete-session-request'])

        self.add_ie(EPSBearerID(ebi))
        self.add_ie(UserLocationInformation(mcc=mcc, mnc=mnc, lac=lac,
                                            rac=rac, tac=tac, ecgi=ecgi,
                                            sac=sac, cgi=cgi))
        self.set_teid(teid)


class DeleteSessionResponse(GTPV2MessageBase):
    '''
    classdocs
    '''

    def __init__(self, teid, sqn = 0x00):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, t = 0x01, sequence = sqn,
            msg_type = GTPmessageTypeDigit['delete-session-response'])
        self.set_teid(teid)
        self.add_ie(SuccessCause())
