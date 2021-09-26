"""
    A class defining the CloudflareDNSDetails
"""
class CloudflareDNSDetails:
    id = ""
    dnsType = ""
    name = ""
    ttl = 1
    proxied = True

    """
        The constructor for the CloudflareDNSDetails
    """
    def __init__(self, id=None, dnsType=None, name=None, ttl=None, proxied=None):
        self.id = id
        self.dnsType = dnsType
        self.name = name
        self.ttl = ttl
        self.proxied = proxied


    """
        Functionality to convert the dns detail into a JSON object
        Returns: jsonObject - The JSON object of the DNS record
    """
    def toJSON(self):
        return {
            "type": self.dnsType,
            "name": self.name,
            "ttl": self.ttl,
            "proxied": self.proxied,
        }

    """
        Functionality to convert the dns detail into a simplified JSON object
        Returns: jsonObject - The simplified JSON object of the DNS record
    """
    def toJSONSimple(self):
        return {
            "type": self.dnsType,
            "name": self.name,
        }

    def __eq__(self, other):
        print()
        if (isinstance(other, CloudflareDNSDetails)):
            return self.dnsType == other.dnsType and self.name == other.name and self.ttl == other.ttl and self.proxied == other.proxied
        elif (isinstance(other, dict)):

            return self.dnsType == other["type"] and self.name == other["name"] and self.ttl == other["ttl"] and self.proxied == other["proxied"]

        return False

    def __ne__(self, other):
        if (isinstance(other, CloudflareDNSDetails)):
            return self.dnsType != other.dnsType or self.name != other.name or self.ttl != other.ttl or self.proxied != other.proxied
        return True