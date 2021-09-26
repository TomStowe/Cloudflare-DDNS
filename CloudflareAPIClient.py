import requests
from models.CloudflareDNSRecord import CloudflareDNSRecord
from models.CloudflareDNSDetails import CloudflareDNSDetails

"""
    The class that defines the CloudFlare API Client
"""
class CloudflareAPIClient:
    __headers = {}
    """
        Constructor
        apiToken: string - The api token to use for the requests
        apiKey: string - The api key to use for the requests
        email: string - The email address to use for the requests
    """
    def __init__(self, apiToken=None, apiKey=None, email=None):
        if (apiToken != None):
            self.__headers = {
                "Authorization": "Bearer " + apiToken,
                "Content-Type": "application/json",
                }
        elif (apiKey != None and email != None):
            self.__headers = {
                "X-Auth-Email": email,
                "X-Auth-Key": apiKey,
                "Content-Type": "application/json",
                }
        else:
            print("API token or apikey and email have not been provided - quitting")
            quit()
        return

    """
        Create a DNS record
        cloudflareDNSRecord: CloudflareDNSRecord - the DNS record to create in cloudflare
        zoneId: string - the zone id to post to
        Returns: bool - True if successful, false if errored
    """
    def createDNSRecord(self, cloudflareDNSRecord, zoneId):
        response = requests.post("https://api.cloudflare.com/client/v4/zones/" + str(zoneId) + "/dns_records", json=cloudflareDNSRecord.toJSON(), headers=self.__headers)
        return response.ok

    """
        Method to get all DNS records from a specific DNS Detail
        zoneId: string - The zone id to get
        dnsDetail: CloudflareDNSDetails - The dns details to get from
        returns: CloudflareDNSRecord[] - the dns records from the DNS detail

    """
    def getDNSRecordsFromDNSDetail(self, zoneId, dnsDetail):
        response = requests.get("https://api.cloudflare.com/client/v4/zones/" + str(zoneId) + "/dns_records?per_page=100", headers=self.__headers, params=dnsDetail.toJSON())
        
        if (response.ok):
            dnsRecords = []
            for r in response.json()["result"]:
                dnsRecords.append(CloudflareDNSRecord(id=r["id"], zoneId=r["zone_id"], name=r["name"],
                dnsType=r["type"], content=r["content"], ttl=r["ttl"]))
            return dnsRecords
        else:
            print("DNS Records for zoneid '" + str(zoneId) + "' and specific dns detail could not be retrieved")
        return None

    """
        Method to get all DNS records from a simplified DNS Detail
        zoneId: string - The zone id to get
        dnsDetail: CloudflareDNSDetails - The dns details to get from
        returns: CloudflareDNSRecord[] - the dns records from the simplified DNS detail
    """
    def getDNSRecordsFromSimplifiedDNSDetail(self, zoneId, dnsDetail):
        response = requests.get("https://api.cloudflare.com/client/v4/zones/" + str(zoneId) + "/dns_records?per_page=100", headers=self.__headers, params=dnsDetail.toJSONSimple())
        
        if (response.ok):
            dnsRecords = []
            for r in response.json()["result"]:
                dnsRecords.append(CloudflareDNSRecord(id=r["id"], zoneId=r["zone_id"], name=r["name"],
                dnsType=r["type"], content=r["content"], ttl=r["ttl"]))
            return dnsRecords
        else:
            print("DNS Records for zoneid '" + str(zoneId) + "' and specific dns detail could not be retrieved")
        return None

    """
        Get a dns record by it's zoneid and id
        zoneId: string - The zone id to get
        id: string - The id of the dns record to get
        returns: CloudflareDNSRecord - The DNS record
    """
    def getDNSRecordById(self, zoneId, id):
        response = requests.get("https://api.cloudflare.com/client/v4/zones/" + str(zoneId) + "/dns_records/" + str(id), headers=self.__headers)
        
        if (response.ok and len(response.json()["result"]) != 1):
            dnsRecords = []
            r = response.json()["result"]
            dnsRecords.append(CloudflareDNSRecord(id=r["id"], zoneId=r["zone_id"], name=r["name"],
            dnsType=r["type"], content=r["content"], ttl=r["ttl"]))
            return dnsRecords[0]
        else:
            print("DNS Record for zoneid '" + str(zoneId) + "' and id " + str(id) + " could not be retrieved")
        return None

    """
        PUT the contents into the DNS record by id and zone id
        zoneId: string - The zone id to put
        id: string - The id of the dns record to put
        dnsRecordContent: string - The contents of the DNS record to put
        returns: bool - True if successful, false otherwise
    """
    def putDNSRecordContents(self, zoneId, id, dnsRecordContent):
        response = requests.patch("https://api.cloudflare.com/client/v4/zones/" + str(zoneId) + "/dns_records/" + str(id), headers=self.__headers, json={"content": dnsRecordContent})
        return response.ok

    """
        Method to get all DNS records
        zoneId: string - the zone id to get
        returns: CloudflareDNSRecord[] - A list of DNS records from cloudflare
    """
    def getDNSRecords(self, zoneId):
        response = requests.get("https://api.cloudflare.com/client/v4/zones/" + str(zoneId) + "/dns_records?per_page=100", headers=self.__headers)
        if (response.ok):
            dnsRecords = []
            for r in response.json()["result"]:
                dnsRecords.append(CloudflareDNSRecord(id=r["id"], zoneId=r["zone_id"], name=r["name"],
                dnsType=r["type"], content=r["content"], ttl=r["ttl"]))
            return dnsRecords
        else:
            print("DNS Records for zoneid '" + str(zoneId) + "' could not be retrieved")
        return None
