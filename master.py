class RFCRecord:
    def __init__(self, rfc_number = -1, rfc_title = 'None', peerHostname ='None', peerid =-1):
        self.rfc_number = rfc_number
        self.rfc_title = rfc_title
        self.peerHostname = peerHostname
        self.peerid=peerid

    def __str__(self):
        return str(self.rfc_number)+' '+str(self.rfc_title)+' '+str(self.peerHostname)+' '+str(self.peerid)



class PeerRecord:
    def __init__(self,peerHostname='None',peerPortNo=10000,peerid=-1):
        self.peerHostname=peerHostname
        self.peerPortNo=peerPortNo
        self.peerid=peerid

    def __str__(self):
        return str(self.peerHostname)+' '+str(self.peerPortNo)+' '+str(self.peerid)