import json

"""
    A class defining the cloudflare DNS record returned from the db
"""
class CloudflareDNSRecord:
    id = ""
    zoneId = ""
    name = ""
    dnsType = ""
    content = ""
    ttl = 1

    def __init__(self, id="", zoneId="", name="", dnsType="", content="", ttl=1):
        self.id = id
        self.zoneId = zoneId
        self.name = name
        self.dnsType = dnsType
        self.content = content
        self.ttl = ttl

    """
        Functionality to convert the dns record into a JSON object
        Returns: jsonObject - The JSON object of the DNS record
    """
    def toJSON(self):
        return {
            "zoneId": self.zoneId,
            "name": self.name,
            "type": self.dnsType,
            "content": self.content,
            "ttl": self.ttl,
        }

    """
        Define how to print this class
    """
    def __str__(self):
        return "id: " + str(self.id) + "\nzoneId: " + str(self.zoneId) + "\nName: " + str(self.name) + "\ndnsType: " + str(self.dnsType) + "\nContent: " + str(self.content) + "\nTTL: " + str(self.ttl)
