"""
    A class defining the cloudflare DNS details
"""
class CloudflareDNSAccount:
    authentication = None
    zoneId = ""
    dnsDetails = []

    """
        The constructor for the CloudflareDNSAccount
    """
    def __init__(self, authentication=None, zoneId="", dnsDetails=None):
        self.authentication = authentication
        self.zoneId = zoneId
        self.dnsDetails = dnsDetails