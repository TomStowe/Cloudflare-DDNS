# File for setting up the Cloudflare DDNS JSON config - specifically for dealing with DNS Failover

import requests
from JSONConfig import JSONConfig 
from CloudflareAPIClient import CloudflareAPIClient

# ----- Config -----#
configPath = "config.json"
# ----- Config -----#

"""
    Method to get the id for a specific DNS record
"""
def getIdForDnsRecord(dnsDetail, client):
    records = client.getDNSRecordsFromDNSDetail(account.zoneId, dnsDetail)
    # If no details, try with simplified information
    if (len(records) == 0):
        records = client.getDNSRecordsFromSimplifiedDNSDetail(account.zoneId, dnsDetail)

    # If there are still no dnsRecords, error
    if (len(records) == 0):
        print("There are no records with the type: " + str(dnsDetail.dnsType) + " and name: " + str(dnsDetail.name) + ". Please check your config.json and DNS records.")
        return None
    
    # If there are multiple records, error
    if (len(records) >= 2):
        print("There are multiple records with the type: " + str(dnsDetail.dnsType) + " and name: " + str(dnsDetail.name) + " - Please select the number of the correct detail:")
        i = 1
        for record in records:
            print(str(i) + ": " + str(record))
            i+=1
        print(str(i) + ": Ignore Record")
        
        num = -1
        while (num == -1):
            try:
                num = int(input("Please input the number of the record you wish to assign: "))
            except:
                continue
            if (num <= 0 or num > len(records)+1):
                num = -1

        # If ignore record, ignore it
        if (num == len(records) + 1):
            return None
        
        # Add the id to the record and return it
        dnsDetail.id = records[num-1].id
        return dnsDetail
    
    # Update the dns record if we have 1 record
    print("Found single dns record for detail: " + str(dnsDetail))
    dnsDetail.id = records[0].id
    return dnsDetail

# Load the config
config = JSONConfig(configPath)
cloudflareAccounts = config.getCloudflareAccounts()

# For each account
for account in cloudflareAccounts:
    # Setup the cloudflare client
    client = CloudflareAPIClient(apiToken=account.authentication.token, apiKey=account.authentication.key, email=account.authentication.email)
    
    # For each record
    for dnsDetail in account.dnsDetails:
        # Get the id for the config, even if the id exists to allow for updating
        detail = getIdForDnsRecord(dnsDetail, client)

        # Save the detail if it does not exist
        if (detail != None):
            config.setIdFromDetails(account.zoneId, dnsDetail)

print("Config Updated")